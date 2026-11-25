import argparse
import json
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7


parser = argparse.ArgumentParser(description="AES-128-CBC video encryption")

parser.add_argument("--input", required=True, help="Input video file")

args = parser.parse_args()

# Load KEY and IV
key_data = json.loads(Path("keys/aes_key.json").read_text())

key = bytes.fromhex(key_data["key"])
iv = bytes.fromhex(key_data["iv"])

# Validate KEY and IV lengths
if len(key) != 16 or len(iv) != 16:
    raise ValueError("AES-128-CBC requires a 16-byte KEY and IV")

source = Path(args.input)

if not source.is_file():
    raise FileNotFoundError(f"Input file not found: {source}")

output_dir = Path("output/encrypted")
output_dir.mkdir(parents=True, exist_ok=True)

encrypted_file = output_dir / f"{source.stem}_encrypted.enc"

# Initialize AES-CBC
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
encryptor = cipher.encryptor()

# PKCS7 padding
padder = PKCS7(algorithms.AES.block_size).padder()

print("Starting AES-128-CBC encryption...")

with source.open("rb") as input_file, encrypted_file.open("wb") as output_file:

    while True:
        chunk = input_file.read(64 * 1024)

        if not chunk:
            break

        padded_data = padder.update(chunk)

        encrypted_data = encryptor.update(padded_data)

        output_file.write(encrypted_data)

    # Add final padding
    final_padded_data = padder.finalize()

    output_file.write(encryptor.update(final_padded_data))

    # Finalize encryption
    output_file.write(encryptor.finalize())

print("Encryption completed successfully!")
print("Encrypted file:", encrypted_file)