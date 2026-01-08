import os
import subprocess
import sys

email = "jane.roughan@datacom.com"
home = os.path.expanduser("~")
ssh_dir = os.path.join(home, ".ssh")
key_path = os.path.join(ssh_dir, "id_ed25519")

os.makedirs(ssh_dir, exist_ok=True)

if os.path.exists(key_path) or os.path.exists(key_path + ".pub"):
    print(f"Key already exists at {key_path} or {key_path}.pub")
    print("If you want to overwrite, delete those files first.")
    sys.exit(1)

cmd = ["ssh-keygen", "-t", "ed25519", "-C", email, "-f", key_path, "-N", ""]
proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

print(proc.stdout)
print(proc.stderr, file=sys.stderr)

if proc.returncode != 0:
    print(f"ssh-keygen failed with exit code {proc.returncode}")
    sys.exit(proc.returncode)

pub_path = key_path + ".pub"
try:
    with open(pub_path, "r", encoding="utf-8") as f:
        pub = f.read().strip()
    print("\n-----PUBLIC KEY-----")
    print(pub)
    print("-----END PUBLIC KEY-----\n")
    print("Add the above public key to your GitHub account (Settings → SSH and GPG keys).")
except Exception as e:
    print("Failed to read public key:", e)
    sys.exit(1)
