
import argparse
import json
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description="Clear Key video decryption")
parser.add_argument("--input", required=True)
args = parser.parse_args()

key_data = json.loads(Path("keys/clear_key.json").read_text())

kid = key_data["kid"]
key = key_data["key"]

source = Path(args.input)
output = Path("output/decrypted")
output.mkdir(parents=True, exist_ok=True)

decrypted_file = output / f"{source.stem}_decrypted.mp4"

command = [
    "packager",
    f"in={source},stream=video,output={decrypted_file}",
    "--enable_raw_key_decryption",
    "--keys",
    f"key_id={kid}:key={key}"
]

print("Starting Clear Key decryption...")

subprocess.run(command, check=True)

print("Decryption completed!")
print("Decrypted video:", decrypted_file)
