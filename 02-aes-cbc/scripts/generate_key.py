import json
import secrets
from pathlib import Path

KEY_FILE = Path("keys/aes_key.json")

# Generate a 128-bit AES key (16 bytes).
key = secrets.token_bytes(16)

# Generate a 128-bit initialization vector (16 bytes).
iv = secrets.token_bytes(16)

KEY_FILE.parent.mkdir(parents=True, exist_ok=True)

key_data = {
    "algorithm": "AES-128-CBC",
    "key": key.hex(),
    "iv": iv.hex()
}

KEY_FILE.write_text(json.dumps(key_data, indent=4))
KEY_FILE.chmod(0o600)

print("AES KEY and IV generated successfully!")
print("Algorithm: AES-128-CBC")
print("Key length: 16 bytes")
print("IV length: 16 bytes")
print("Saved to:", KEY_FILE)