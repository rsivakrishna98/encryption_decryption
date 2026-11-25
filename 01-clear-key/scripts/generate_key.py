
import secrets
import json
from pathlib import Path

KEY_FILE = Path("keys/clear_key.json")

# Generate a 128-bit Key ID and 128-bit content key
kid = secrets.token_bytes(16)
key = secrets.token_bytes(16)

KEY_FILE.parent.mkdir(parents=True, exist_ok=True)

data = {
    "kid": kid.hex(),
    "key": key.hex()
}

KEY_FILE.write_text(json.dumps(data, indent=4))
KEY_FILE.chmod(0o600)

print("Clear Key generated successfully!")
print("KID:", kid.hex())
print("Content Key:", key.hex())
print("Saved:", KEY_FILE)
