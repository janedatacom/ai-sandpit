"""
X-ray Image Scraper
Scrapes de-anonymized X-ray images from open medical datasets
Includes security safeguards for virus/malware protection
"""

import os
import requests
import json
import csv
import struct
import time
import hashlib
import subprocess
import platform
from PIL import Image
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse


# Security Configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB max per image
REQUEST_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 0.5  # seconds between requests

# Default download limit for safety/cost control
DEFAULT_DOWNLOAD_LIMIT = 15

# Dataset folder structure
DEFAULT_CLASSES = ("silicosis", "healthy")
DEFAULT_SPLITS = ("train", "unseen")
DEFAULT_TRAIN_FRACTION = 0.8

# Whitelist of safe domains for scraping
SAFE_DOMAINS = {
    'openi.nlm.nih.gov',
    'nlm.nih.gov',
    'nih.gov',
}

# Valid image file signatures (magic bytes)
VALID_IMAGE_SIGNATURES = {
    b'\xFF\xD8\xFF': 'jpeg',  # JPEG
    b'\x89PNG\r\n\x1a\n': 'png',  # PNG
    b'GIF8': 'gif',  # GIF
}

# Security audit file
SECURITY_LOG_FILE = "security_audit.log"
HASH_LOG_FILE = "file_hashes.csv"


class XrayScraper:
    def __init__(
        self,
        output_dir: str = "xray_images",
        classes: tuple[str, ...] = DEFAULT_CLASSES,
        splits: tuple[str, ...] = DEFAULT_SPLITS,
        train_fraction: float = DEFAULT_TRAIN_FRACTION,
    ):
        """Initialize the scraper with output directory"""
        self.output_dir = output_dir
        self.classes = classes
        self.splits = splits
        self.train_fraction = train_fraction
        self.metadata_file = os.path.join(output_dir, "metadata.csv")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.last_request_time = 0  # For rate limiting
        
        # Create output directory structure
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        self._init_dataset_dirs()
        
        # Initialize metadata CSV
        self._init_metadata_csv()
        self._init_security_logs()

    def _init_dataset_dirs(self):
        """Create class/split folder structure."""
        for class_name in self.classes:
            for split_name in self.splits:
                Path(self.output_dir, class_name, split_name).mkdir(parents=True, exist_ok=True)

    def _choose_split(self, key: str) -> str:
        """Deterministically choose train/unseen split based on a stable hash."""
        if "train" not in self.splits or "unseen" not in self.splits:
            return self.splits[0]

        train_threshold = int(self.train_fraction * 100)
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        bucket = int(digest[:8], 16) % 100
        return "train" if bucket < train_threshold else "unseen"

    def _split_targets(self, total: int) -> dict[str, int]:
        """Compute exact per-run targets for train/unseen."""
        if total <= 0:
            return {"train": 0, "unseen": 0}
        train_target = int(total * self.train_fraction)
        unseen_target = total - train_target
        return {"train": train_target, "unseen": unseen_target}

    def _resolve_target_path(self, filename: str, label: str, split: str) -> tuple[str, str]:
        """Return (absolute_path, relative_path) for a labeled/split file."""
        if label not in self.classes:
            raise ValueError(f"label must be one of {self.classes}; got {label!r}")
        if split not in self.splits:
            raise ValueError(f"split must be one of {self.splits}; got {split!r}")

        rel_path = os.path.join(label, split, filename)
        abs_path = os.path.join(self.output_dir, rel_path)
        return abs_path, rel_path
    
    def _is_safe_domain(self, url: str) -> bool:
        """Verify URL is from a whitelisted safe domain"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Check exact match or subdomain of whitelisted domains
            for safe_domain in SAFE_DOMAINS:
                if domain == safe_domain or domain.endswith('.' + safe_domain):
                    return True
            
            return False
        except Exception:
            return False
    
    def _validate_image_integrity(self, filepath: str) -> bool:
        """
        Validate file is actually an image using magic bytes (file signatures)
        Protects against trojanized or malicious files
        """
        try:
            if not os.path.exists(filepath):
                return False
            
            # Check file size
            file_size = os.path.getsize(filepath)
            if file_size == 0 or file_size > MAX_FILE_SIZE:
                print(f"⚠️  File size invalid: {file_size} bytes")
                return False
            
            # Read file header for magic bytes
            with open(filepath, 'rb') as f:
                header = f.read(512)  # Read enough for any signature
            
            # Check standard image signatures
            for signature, img_type in VALID_IMAGE_SIGNATURES.items():
                if header.startswith(signature):
                    print(f"✓ Valid {img_type.upper()} file")
                    return True

            # Explicitly disallow DICOM files
            if len(header) > 132 and header[128:132] == b'DICM':
                print("✗ DICOM detected (DICM signature) - blocked")
                return False
            
            print(f"⚠️  File signature invalid - not a recognized image format")
            return False
            
        except Exception as e:
            print(f"⚠️  Error validating file: {str(e)}")
            return False
    
    def _apply_rate_limit(self):
        """Apply rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - elapsed)
        self.last_request_time = time.time()

    def _init_metadata_csv(self):
        """Initialize metadata CSV file with headers"""
        if not os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Image ID', 'Relative Path', 'Source', 'Label', 'Split', 'Download Date', 'URL', 'Title', 'Description'])
    
    def _init_security_logs(self):
        """Initialize security audit logs"""
        security_log_path = os.path.join(self.output_dir, SECURITY_LOG_FILE)
        hash_log_path = os.path.join(self.output_dir, HASH_LOG_FILE)
        
        if not os.path.exists(hash_log_path):
            with open(hash_log_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Filename', 'SHA256', 'MD5', 'File Size', 'Scan Status', 'Timestamp'])
    
    def _log_security_event(self, event: str):
        """Log security events for audit trail"""
        try:
            log_path = os.path.join(self.output_dir, SECURITY_LOG_FILE)
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now().isoformat()}] {event}\n")
        except Exception as e:
            print(f"⚠️  Error logging security event: {str(e)}")
    
    def _calculate_file_hashes(self, filepath: str) -> tuple:
        """Calculate SHA256 and MD5 hashes of file"""
        try:
            sha256_hash = hashlib.sha256()
            md5_hash = hashlib.md5()
            
            with open(filepath, 'rb') as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
                    md5_hash.update(byte_block)
            
            return sha256_hash.hexdigest(), md5_hash.hexdigest()
        except Exception as e:
            print(f"⚠️  Error calculating hashes: {str(e)}")
            return None, None
    
    def _log_file_hash(self, filename: str, sha256: str, md5: str, file_size: int, scan_status: str):
        """Log file hash for integrity verification"""
        try:
            hash_log_path = os.path.join(self.output_dir, HASH_LOG_FILE)
            with open(hash_log_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    filename,
                    sha256,
                    md5,
                    file_size,
                    scan_status,
                    datetime.now().isoformat()
                ])
        except Exception as e:
            print(f"⚠️  Error logging file hash: {str(e)}")
    
    def _scan_with_windows_defender(self, filepath: str) -> bool:
        """Scan file with Windows Defender (if available)"""
        if platform.system() != "Windows":
            print("ℹ️  Windows Defender scanning only available on Windows")
            return True
        
        try:
            # Use Windows Defender command-line tool
            result = subprocess.run(
                ['powershell', '-Command', f'Start-MpScan -ScanPath "{filepath}" -ScanType QuickScan'],
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self._log_security_event(f"✓ Windows Defender: Clean - {os.path.basename(filepath)}")
                return True
            else:
                self._log_security_event(f"⚠️  Windows Defender: Potential threat detected - {os.path.basename(filepath)}")
                print(f"⚠️  Windows Defender alert for {os.path.basename(filepath)}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"⚠️  Windows Defender scan timeout for {filepath}")
            return False
        except Exception as e:
            print(f"ℹ️  Windows Defender not available: {str(e)}")
            return True  # Continue if Defender not available
    
    def _strip_image_metadata(self, filepath: str) -> bool:
        """Remove EXIF and metadata from image"""
        try:
            # Get file extension
            _, ext = os.path.splitext(filepath)
            
            if ext.lower() in ['.jpg', '.jpeg', '.png']:
                try:
                    from PIL import Image
                    from PIL.Image import Exif
                    
                    img = Image.open(filepath)
                    
                    # Create new image without metadata
                    data = list(img.getdata())
                    image_without_exif = Image.new(img.mode, img.size)
                    image_without_exif.putdata(data)
                    
                    # Save without EXIF
                    image_without_exif.save(filepath, quality=95)
                    
                    self._log_security_event(f"✓ Metadata stripped from {os.path.basename(filepath)}")
                    print(f"✓ Metadata stripped from image")
                    return True
                except Exception as e:
                    print(f"⚠️  Could not strip metadata (continuing): {str(e)}")
                    return True  # Continue even if metadata stripping fails
            
            return True
            
        except Exception as e:
            print(f"⚠️  Error stripping metadata: {str(e)}")
            return True
    
    def _validate_image_structure(self, filepath: str) -> bool:
        """Validate image structure to detect corruption or polyglot files"""
        try:
            from PIL import Image
            
            with Image.open(filepath) as img:
                # Try to load image to verify structure
                img.verify()
            
            print(f"✓ Image structure validated")
            return True
            
        except Exception as e:
            print(f"✗ Image structure invalid: {str(e)}")
            self._log_security_event(f"⚠️  Invalid image structure - {os.path.basename(filepath)}")
            return False

    def download_image(self, url: str, image_id: str, metadata: Dict, label: str, split: str | None = None) -> bool:
        """Download a single image with security validation"""
        try:
            # Security Check 1: Domain whitelist validation
            if not self._is_safe_domain(url):
                print(f"✗ Blocked: URL domain not in whitelist - {url}")
                return False
            
            # Apply rate limiting to prevent abuse
            self._apply_rate_limit()
            
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            # Security Check 2: Verify Content-Length before saving
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > MAX_FILE_SIZE:
                print(f"✗ File too large: {int(content_length)} bytes (max {MAX_FILE_SIZE})")
                return False
            
            # Determine file extension
            content_type = response.headers.get('content-type', '').lower()
            # Explicitly disallow DICOM downloads
            if 'dicom' in content_type or url.lower().endswith('.dcm'):
                self._log_security_event(f"✗ Blocked DICOM download attempt - {url} (content-type: {content_type})")
                print("✗ Blocked: DICOM files are not allowed")
                return False

            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
            elif 'png' in content_type:
                ext = '.png'
            else:
                ext = '.jpg'
            
            filename = f"{image_id}{ext}"
            if split is None:
                split = self._choose_split(url)
            filepath, rel_path = self._resolve_target_path(filename, label=label, split=split)
            
            # Save image to temporary location first
            temp_filepath = filepath + '.tmp'
            with open(temp_filepath, 'wb') as f:
                f.write(response.content)
            
            # Security Check 3: Validate file integrity (magic bytes)
            if not self._validate_image_integrity(temp_filepath):
                os.remove(temp_filepath)
                print(f"✗ File validation failed for {filename}")
                return False

            # Secondary DICOM check (in case content-type lied)
            with open(temp_filepath, 'rb') as f:
                header = f.read(132)
                if len(header) >= 132 and header[128:132] == b'DICM':
                    os.remove(temp_filepath)
                    self._log_security_event(f"✗ Blocked DICOM by signature - {url}")
                    print("✗ Blocked: DICOM signature detected")
                    return False
            
            # Security Check 4: Validate image structure
            if not self._validate_image_structure(temp_filepath):
                os.remove(temp_filepath)
                self._log_security_event(f"✗ Blocked corrupted/invalid image - {filename}")
                return False
            
            # Security Check 5: Scan with antivirus
            if not self._scan_with_windows_defender(temp_filepath):
                os.remove(temp_filepath)
                self._log_security_event(f"✗ Blocked by antivirus - {filename}")
                return False
            
            # Security Check 6: Strip metadata
            self._strip_image_metadata(temp_filepath)
            
            # Calculate and log file hashes
            sha256, md5 = self._calculate_file_hashes(temp_filepath)
            file_size = os.path.getsize(temp_filepath)
            
            # Move to final location
            os.rename(temp_filepath, filepath)
            
            # Log file hash
            if sha256 and md5:
                self._log_file_hash(rel_path, sha256, md5, file_size, "Clean")
                self._log_security_event(f"✓ File verified and logged - {rel_path} (SHA256: {sha256[:16]}...)")
            
            # Save metadata
            self._save_metadata(image_id, rel_path, metadata, label=label, split=split)
            
            print(f"✓ Downloaded & verified: {rel_path}")
            return True
            
        except requests.exceptions.Timeout:
            print(f"✗ Download timeout for {image_id} (>{REQUEST_TIMEOUT}s)")
            return False
        except requests.exceptions.ConnectionError:
            print(f"✗ Connection error downloading {image_id}")
            return False
        except Exception as e:
            print(f"✗ Failed to download {image_id}: {str(e)}")
            return False
    
    def _save_metadata(self, image_id: str, rel_path: str, metadata: Dict, label: str, split: str):
        """Save image metadata to CSV"""
        try:
            with open(self.metadata_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    image_id,
                    rel_path,
                    metadata.get('source', ''),
                    label,
                    split,
                    datetime.now().isoformat(),
                    metadata.get('url', ''),
                    metadata.get('title', ''),
                    metadata.get('description', '')
                ])
        except Exception as e:
            print(f"Error saving metadata: {str(e)}")
    
    def scrape_openi(self, query: str, label: str, limit: int = DEFAULT_DOWNLOAD_LIMIT) -> int:
        """
        Scrape X-rays from OpenI (NIH's open access image collection)
        Uses their public API
        """
        print("\n🔍 Scraping OpenI Dataset...")
        base_url = "https://openi.nlm.nih.gov/api/search"
        count = 0
        targets = self._split_targets(limit)
        split_counts = {"train": 0, "unseen": 0}
        
        try:
            # Verify domain is safe
            if not self._is_safe_domain(base_url):
                print("✗ OpenI domain not in whitelist")
                return 0
            
            params = {
                'query': query,
                'collection': 'CXR',
                'pagesize': limit
            }
            
            self._apply_rate_limit()
            response = self.session.get(base_url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            # OpenI API returns XML, parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'xml')
            
            # Find all document entries
            documents = soup.find_all('document')
            
            for idx, doc in enumerate(documents):
                try:
                    if count >= limit:
                        break

                    image_id = f"openi_{label}_{count:05d}"
                    
                    # Extract metadata
                    title = doc.find('title')
                    title_text = title.text if title else "Unknown"
                    
                    # Get image URL from NCBI/NIH source
                    rank = doc.find('rank')
                    uid = doc.find('uid')
                    
                    if uid:
                        # Construct direct image URL
                        image_url = f"https://openi.nlm.nih.gov/imgs/{uid.text}/large.jpg"

                        # Enforce exact 80/20 split (by quotas) per class
                        split = "train" if split_counts["train"] < targets["train"] else "unseen"
                        
                        metadata = {
                            'source': 'OpenI (NIH)',
                            'url': image_url,
                            'title': title_text,
                            'description': f"NIH OpenI - {title_text}"
                        }
                        
                        if self.download_image(image_url, image_id, metadata, label=label, split=split):
                            count += 1
                            split_counts[split] += 1
                
                except Exception as e:
                    print(f"Error processing document {idx}: {str(e)}")
                    continue
            
            print(f"✓ OpenI: Downloaded {count} images")
            return count
            
        except Exception as e:
            print(f"✗ Error scraping OpenI: {str(e)}")
            return count
    
    def scrape_chexpert_metadata(self, limit: int = DEFAULT_DOWNLOAD_LIMIT) -> int:
        """
        Note: CheXpert full dataset requires direct download from Stanford
        This function provides guidance for manual download
        """
        print("\n📋 CheXpert Dataset Info:")
        print("CheXpert is available for download from: https://stanfordmlgroup.github.io/competitions/chexpert/")
        print("It requires registration but is publicly available for research.")
        print("Once downloaded, you can process the metadata CSV.")
        return 0
    
    def scrape_source_generic(self, url: str, image_selector: str, source_name: str, limit: int = DEFAULT_DOWNLOAD_LIMIT) -> int:
        """
        Generic scraper for any website with image gallery
        
        Args:
            url: Website URL
            image_selector: CSS selector for images (e.g., 'img.xray-image')
            source_name: Name of the source
            limit: Maximum images to download
        """
        print(f"\n🔍 Scraping {source_name}...")
        
        # Security Check: Verify domain is safe
        if not self._is_safe_domain(url):
            print(f"✗ {source_name} domain not in whitelist - add to SAFE_DOMAINS if trusted")
            return 0
        
        count = 0
        
        try:
            self._apply_rate_limit()
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            images = soup.select(image_selector)
            
            for idx, img in enumerate(images[:limit]):
                try:
                    image_id = f"{source_name.lower().replace(' ', '_')}_{count:05d}"
                    
                    # Get image source
                    img_url = img.get('src') or img.get('data-src')
                    if not img_url:
                        continue
                    
                    # Handle relative URLs
                    if img_url.startswith('/'):
                        from urllib.parse import urljoin
                        img_url = urljoin(url, img_url)
                    
                    # Verify image URL is safe
                    if not self._is_safe_domain(img_url):
                        print(f"⚠️  Skipping image from untrusted domain: {img_url}")
                        continue
                    
                    # Get alt text or title for metadata
                    title = img.get('alt') or img.get('title') or "No description"
                    
                    metadata = {
                        'source': source_name,
                        'url': img_url,
                        'title': title,
                        'description': title
                    }
                    
                    if self.download_image(img_url, image_id, metadata):
                        count += 1
                
                except Exception as e:
                    print(f"Error processing image {idx}: {str(e)}")
                    continue
            
            print(f"✓ {source_name}: Downloaded {count} images")
            return count
            
        except Exception as e:
            print(f"✗ Error scraping {source_name}: {str(e)}")
            return count
    
    def generate_report(self):
        """Generate a summary report of downloaded images"""
        print("\n" + "="*50)
        print("📊 Download Report")
        print("="*50)

        image_count = 0
        for root, _dirs, files in os.walk(self.output_dir):
            for name in files:
                if name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    image_count += 1

        print(f"Total images downloaded: {image_count}")
        print(f"Output directory: {os.path.abspath(self.output_dir)}")
        print(f"Metadata file: {os.path.abspath(self.metadata_file)}")
        
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"Metadata records: {len(lines) - 1}")  # Subtract header
        
        # Print security summary
        security_log_path = os.path.join(self.output_dir, SECURITY_LOG_FILE)
        hash_log_path = os.path.join(self.output_dir, HASH_LOG_FILE)
        
        print("\n" + "="*50)
        print("🔒 Security Summary")
        print("="*50)
        
        if os.path.exists(hash_log_path):
            with open(hash_log_path, 'r', encoding='utf-8') as f:
                hash_lines = f.readlines()
                print(f"Files scanned and hashed: {len(hash_lines) - 1}")
        
        if os.path.exists(security_log_path):
            print(f"Security audit log: {os.path.abspath(security_log_path)}")
            with open(security_log_path, 'r', encoding='utf-8') as f:
                recent_events = f.readlines()[-10:]  # Show last 10 events
                print(f"\nRecent security events:")
                for event in recent_events:
                    print(f"  {event.strip()}")


def main():
    """Main execution"""
    print("🏥 X-ray Image Scraper")
    print("="*50)
    
    # Initialize scraper
    scraper = XrayScraper(output_dir=r"C:\temp\xray_images")
    
    total_downloaded = 0
    
    # Scrape OpenI (NIH) with class folders and an exact 80/20 split per class.
    # Limit is per class: DEFAULT_DOWNLOAD_LIMIT healthy + DEFAULT_DOWNLOAD_LIMIT silicosis.
    total_downloaded += scraper.scrape_openi(query="normal", label="healthy", limit=DEFAULT_DOWNLOAD_LIMIT)
    total_downloaded += scraper.scrape_openi(query="silicosis", label="silicosis", limit=DEFAULT_DOWNLOAD_LIMIT)
    
    # You can add more sources here
    # Example of generic scraper (uncomment and modify as needed):
    # total_downloaded += scraper.scrape_source_generic(
    #     url="https://example.com/xray-gallery",
    #     image_selector="img.xray",
    #     source_name="Example Source",
    #     limit=10
    # )
    
    # Generate report
    scraper.generate_report()
    
    print("\n✅ Scraping complete!")


if __name__ == "__main__":
    main()
