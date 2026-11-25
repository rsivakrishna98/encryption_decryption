
import argparse
import json
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description="Clear Key video encryption")
parser.add_argument("--input", required=True)
args = parser.parse_args()

key_data = json.loads(Path("keys/clear_key.json").read_text())

kid = key_data["kid"]
key = key_data["key"]

source = Path(args.input)
output = Path("output/encrypted")
output.mkdir(parents=True, exist_ok=True)

encrypted_file = output / f"{source.stem}_encrypted.mp4"

command = [
    "packager",
    f"in={source},stream=video,output={encrypted_file}",
    "--enable_raw_key_encryption",
    "--keys",
    f"label=:key_id={kid}:key={key}",
    "--protection_scheme",
    "cenc",
    "--clear_lead",
    "0"
]

print("Starting Clear Key encryption...")

subprocess.run(command, check=True)

print("Encryption completed!")
print("Encrypted video:", encrypted_file)
