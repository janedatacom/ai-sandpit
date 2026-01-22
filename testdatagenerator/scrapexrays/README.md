# X-ray Image Scraper

A Python-based web scraper for collecting de-anonymized X-ray images from open medical datasets.

## Features

- **BeautifulSoup Integration**: Uses BeautifulSoup for HTML/XML parsing
- **Multiple Data Sources**: 
  - OpenI (NIH's open medical image collection)
  - Generic website scraper for custom sources
- **Metadata Collection**: Stores image metadata (source, URL, title, description) in CSV
- **Batch Processing**: Download multiple images with proper error handling
- **Organized Output**: Images saved with metadata tracking

## 🔒 Security Features

### Advanced Malware Protection:

1. **Magic Byte Validation** - Verifies files are actual images using file signatures
2. **Windows Defender Integration** - Real-time antivirus scanning
3. **File Hash Logging** - SHA256 & MD5 hashes for integrity verification
4. **Image Structure Validation** - Detects corrupted or polyglot files
5. **Metadata Stripping** - Removes EXIF and embedded data
6. **Domain Whitelist** - Only downloads from trusted sources
7. **File Size Limits** - Max 50MB per image
8. **Request Timeouts** - 10-second limit per download
9. **Rate Limiting** - Prevents abuse and suspicious activity
10. **Security Audit Logs** - Complete audit trail of all operations

## Open Medical Datasets

### 1. **OpenI (NIH) - Integrated Search of Open Medical Images**
- **URL**: https://openi.nlm.nih.gov/
- **De-anonymized**: Yes ✓
- **Free**: Yes ✓
- **No permission needed**: Yes ✓
- **API Available**: Yes ✓

### 2. **CheXpert - Stanford**
- **URL**: https://stanfordmlgroup.github.io/competitions/chexpert/
- **De-anonymized**: Yes ✓
- **Free**: Yes (requires registration) ✓
- **Metadata**: Excellent labeling

### 3. **MICCAI Data Portal**
- **URL**: https://www.miccai.org/
- **Various open datasets available**

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from xray_scraper import XrayScraper

# Create scraper instance
scraper = XrayScraper(output_dir="xray_images")

# Scrape from OpenI
scraper.scrape_openi(limit=10)

# Generate report
scraper.generate_report()
```

### Running the Script

```bash
python xray_scraper.py
```

### Custom Source Scraping

```python
scraper.scrape_source_generic(
    url="https://example.com/xray-gallery",
    image_selector="img.xray-image",
    source_name="Custom Source",
    limit=20
)
```

## Output Structure

```
xray_images/
├── xray_00001.jpg
├── xray_00002.jpg
├── xray_00003.png
├── metadata.csv
├── security_audit.log
└── file_hashes.csv
```

## Security Files

### security_audit.log
Complete audit trail with timestamps of all security events:
- File validations
- Antivirus scan results
- Metadata stripping operations
- Blocked files

### file_hashes.csv
Integrity verification with cryptographic hashes:
- SHA256 hash (for primary integrity verification)
- MD5 hash (for secondary verification)
- File size
- Scan status
- Timestamp

## Metadata CSV Format

| Image ID | Filename | Source | Download Date | URL | Title | Description |
|----------|----------|--------|---------------|----|-------|-------------|
| openi_00000 | openi_00000.jpg | OpenI (NIH) | 2024-01-09T... | https://... | Chest X-ray | NIH OpenI - Chest X-ray |

## Ethical Guidelines

- ✓ Only scrapes open, de-anonymized datasets
- ✓ Respects robots.txt and terms of service
- ✓ Uses appropriate User-Agent headers
- ✓ Implements rate limiting (configurable)
- ✓ Maintains metadata for attribution

## Requirements

- Python 3.8+
- requests
- beautifulsoup4
- lxml
- Pillow
- pandas

## Notes

- OpenI API returns XML, processed with BeautifulSoup's XML parser
- Some datasets require manual registration (CheXpert)
- Always verify you have appropriate rights to use downloaded images
- Respect bandwidth - use reasonable limits when scraping

## License & Attribution

Images downloaded from these sources should be attributed according to their respective licenses.
