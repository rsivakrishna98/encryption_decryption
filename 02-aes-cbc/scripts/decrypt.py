import argparse
import json
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7


parser = argparse.ArgumentParser(description="AES-128-CBC video decryption")

parser.add_argument("--input", required=True, help="Encrypted file")

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
    raise FileNotFoundError(f"Encrypted file not found: {source}")

if source.stat().st_size == 0 or source.stat().st_size % 16 != 0:
    raise ValueError("Invalid AES-CBC encrypted file size")

output_dir = Path("output/decrypted")
output_dir.mkdir(parents=True, exist_ok=True)

decrypted_file = output_dir / "sample_decrypted.mp4"

# Initialize AES-CBC
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
decryptor = cipher.decryptor()

# PKCS7 unpadding
unpadder = PKCS7(algorithms.AES.block_size).unpadder()

print("Starting AES-128-CBC decryption...")

with source.open("rb") as input_file, decrypted_file.open("wb") as output_file:

    while True:
        chunk = input_file.read(64 * 1024)

        if not chunk:
            break

        decrypted_data = decryptor.update(chunk)

        unpadded_data = unpadder.update(decrypted_data)

        output_file.write(unpadded_data)

    # Finalize decryption
    final_decrypted_data = decryptor.finalize()

    output_file.write(unpadder.update(final_decrypted_data))

    # Remove PKCS7 padding
    output_file.write(unpadder.finalize())

print("Decryption completed successfully!")
print("Decrypted video:", decrypted_file)