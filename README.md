# Video Encryption and Decryption Lab

A hands-on Linux project demonstrating two independent video encryption and decryption workflows using Python, Shaka Packager, and FFmpeg.

This project explores:

1. **Clear Key + CENC** – Encrypting video samples using Common Encryption (CENC) with Shaka Packager.
2. **AES-128-CBC** – Encrypting an entire MP4 file using standard AES-CBC file encryption with Python.

Both workflows have separate scripts, key-generation processes, encryption commands, decryption commands, and output directories.

---

## Project Architecture

```text
encryption_decryption/
│
├── 01-clear-key/
│   ├── input/
│   │   └── sample.mp4
│   ├── keys/
│   │   └── clear_key.json
│   ├── output/
│   │   ├── encrypted/
│   │   └── decrypted/
│   ├── scripts/
│   │   ├── generate_key.py
│   │   ├── encrypt.py
│   │   └── decrypt.py
│   └── player/
│       └── index.html
│
├── 02-aes-cbc/
│   ├── input/
│   │   └── sample.mp4
│   ├── keys/
│   │   └── aes_key.json
│   ├── output/
│   │   ├── encrypted/
│   │   │   └── sample_encrypted.enc
│   │   └── decrypted/
│   │       └── sample_decrypted.mp4
│   ├── scripts/
│   │   ├── generate_key.py
│   │   ├── encrypt.py
│   │   └── decrypt.py
│   └── venv/
│
└── README.md
```

---

# 1. Clear Key + CENC Encryption

## Overview

Clear Key is a DRM key system used with the Encrypted Media Extensions (EME) API in supported browsers.

Common Encryption (CENC) defines how media samples are encrypted and how encryption information is stored in the media container.

This project uses:

- **Shaka Packager** – Media packaging and encryption.
- **Clear Key** – Content key management for the demonstration.
- **CENC (`cenc`)** – Common Encryption using AES-CTR.
- **KID** – Key ID that identifies the content key.
- **PSSH** – Protection System Specific Header metadata.

### Encryption Flow

```text
             Original MP4
                  |
                  v
          Generate KID + KEY
                  |
                  v
           clear_key.json
                  |
                  v
          Shaka Packager
                  |
                  v
          CENC Encryption
                  |
                  v
          Encrypted MP4
                  |
                  v
          Shaka Packager
                  |
                  v
           CENC Decryption
                  |
                  v
          Decrypted MP4
```

## Important Concepts

| Component | Description |
|---|---|
| Clear Key | A simple EME key system |
| CENC | Common Encryption media format |
| AES-CTR | Encryption mode used by the `cenc` protection scheme |
| KID | Identifies the content encryption key |
| KEY | Secret key used to encrypt and decrypt media samples |
| PSSH | Stores protection-system-specific metadata |

**Note:** Clear Key is a key system, not an encryption algorithm. CENC is the media encryption scheme. The `cenc` scheme uses AES-CTR.

## Prerequisites

- Linux
- Python 3
- Shaka Packager
- FFmpeg
- FFprobe
- FFplay

Check installations:

```bash
python3 --version
packager --version
ffmpeg -version
ffprobe -version
ffplay -version
```

## Step 1: Generate KID and Content KEY

Navigate to the project:

```bash
cd ~/work/encryption_decryption/01-clear-key
```

Generate the Clear Key:

```bash
python3 scripts/generate_key.py
```

This generates:

```text
keys/clear_key.json
```

Example structure:

```json
{
    "kid": "generated-128-bit-key-id",
    "key": "generated-128-bit-content-key"
}
```

Both KID and content KEY are generated as 16-byte random values.

## Step 2: Encrypt the Video

```bash
python3 scripts/encrypt.py --input input/sample.mp4
```

Expected output:

```text
output/encrypted/sample_encrypted.mp4
```

The script uses Shaka Packager with:

```bash
--enable_raw_key_encryption
--protection_scheme cenc
```

For complete encryption without a clear lead, configure the Packager command with:

```bash
--clear_lead 0
```

## Step 3: Decrypt the Video

```bash
python3 scripts/decrypt.py \
    --input output/encrypted/sample_encrypted.mp4
```

Expected output:

```text
output/decrypted/sample_encrypted_decrypted.mp4
```

The decryption script uses:

```bash
--enable_raw_key_decryption
```

and the same KID and content KEY generated earlier.

## Step 4: Inspect Encryption Metadata

Inspect the encrypted MP4:

```bash
ffprobe -v trace \
output/encrypted/sample_encrypted.mp4 2>&1 \
| grep -Ei 'sinf|schm|tenc|encv|cenc|senc|saiz|saio|pssh'
```

Relevant MP4 encryption metadata includes:

| Box | Purpose |
|---|---|
| `sinf` | Protection information container |
| `frma` | Original media format |
| `schm` | Protection scheme |
| `schi` | Scheme-specific information |
| `tenc` | Track encryption defaults |
| `pssh` | Protection System Specific Header |
| `senc` | Sample encryption information |
| `saiz` | Auxiliary information sizes |
| `saio` | Auxiliary information offsets |

These boxes indicate that the MP4 contains CENC protection metadata.

## Step 5: Inspect Decrypted Video

```bash
ffprobe -v error \
-show_entries stream=codec_name \
-of default=noprint_wrappers=1 \
output/decrypted/sample_encrypted_decrypted.mp4
```

Expected output for the video-only workflow:

```text
h264
```

Play the decrypted video:

```bash
ffplay output/decrypted/sample_encrypted_decrypted.mp4
```

**Current implementation scope:** The encryption and decryption scripts select the video stream. The original sample also contains AAC audio, which is not included in this video-only workflow. Browser-based EME playback and complete audio/video DASH packaging are separate follow-up tasks.

---

# 2. AES-128-CBC File Encryption

## Overview

AES-128-CBC is a symmetric encryption algorithm used to encrypt the complete contents of a file.

Unlike CENC, this implementation does not understand MP4 tracks, video samples, or DRM metadata. It treats the MP4 as binary data and encrypts the entire file.

This project uses:

- **Python** – Encryption and decryption implementation.
- **Cryptography library** – AES implementation.
- **AES-128** – 128-bit symmetric encryption key.
- **CBC** – Cipher Block Chaining mode.
- **IV** – Initialization Vector.
- **PKCS7** – Padding scheme for AES block alignment.

### Encryption Flow

```text
              Original MP4
                   |
                   v
             Generate KEY
                   |
                   v
              Generate IV
                   |
                   v
              aes_key.json
                   |
                   v
            Python Encryption
                   |
                   v
              AES-128-CBC
                   |
                   v
           Encrypted .enc File
                   |
                   v
            Python Decryption
                   |
                   v
              AES-128-CBC
                   |
                   v
           Decrypted MP4 File
                   |
                   v
              Video Playback
```

## Important Concepts

| Component | Description |
|---|---|
| AES | Advanced Encryption Standard |
| AES-128 | AES using a 128-bit key |
| CBC | Cipher Block Chaining mode |
| KEY | Secret encryption key |
| IV | Initialization Vector |
| PKCS7 | Adds padding to align data with AES block size |

AES has a block size of 128 bits (16 bytes), regardless of whether the key is 128, 192, or 256 bits.

This implementation uses a 16-byte KEY and a 16-byte IV.

## Prerequisites

- Linux
- Python 3
- FFmpeg
- FFprobe
- FFplay

## Step 1: Create Python Virtual Environment

Navigate to the AES-CBC project:

```bash
cd ~/work/encryption_decryption/02-aes-cbc
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install the dependency:

```bash
pip install cryptography
```

Verify:

```bash
pip show cryptography
```

## Step 2: Generate AES KEY and IV

```bash
python3 scripts/generate_key.py
```

This generates:

```text
keys/aes_key.json
```

Example structure:

```json
{
    "algorithm": "AES-128-CBC",
    "key": "generated-128-bit-secret-key",
    "iv": "generated-128-bit-initialization-vector"
}
```

The actual values are hexadecimal representations of 16-byte random values.

## Step 3: Encrypt the MP4 File

```bash
python3 scripts/encrypt.py --input input/sample.mp4
```

Expected output:

```text
output/encrypted/sample_encrypted.enc
```

The script:

1. Loads the AES KEY and IV.
2. Initializes AES-128-CBC.
3. Reads the input MP4 in chunks.
4. Applies PKCS7 padding.
5. Encrypts the data.
6. Writes the encrypted binary output.

Check the encrypted file:

```bash
file output/encrypted/sample_encrypted.enc
```

Expected:

```text
output/encrypted/sample_encrypted.enc: data
```

The encrypted output is no longer a playable MP4 file.

## Step 4: Decrypt the Encrypted File

```bash
python3 scripts/decrypt.py \
    --input output/encrypted/sample_encrypted.enc
```

Expected output:

```text
output/decrypted/sample_decrypted.mp4
```

The script:

1. Loads the same AES KEY and IV.
2. Initializes AES-128-CBC decryption.
3. Reads the encrypted data in chunks.
4. Decrypts the ciphertext.
5. Removes PKCS7 padding.
6. Reconstructs the original MP4 file.

## Step 5: Validate the Decrypted Video

Inspect the streams:

```bash
ffprobe -v error \
-show_entries stream=codec_name \
-of default=noprint_wrappers=1 \
output/decrypted/sample_decrypted.mp4
```

Expected output:

```text
h264
aac
```

Play the decrypted video:

```bash
ffplay output/decrypted/sample_decrypted.mp4
```

The decrypted video should contain both video and audio.

## Step 6: Verify File Integrity Using SHA256

Compare the original and decrypted files:

```bash
sha256sum input/sample.mp4 \
output/decrypted/sample_decrypted.mp4
```

Expected result:

```text
71944d7430c461f0cd6e7fd10cee7eb72786352a3678fc7bc0ae3d410f72aece  input/sample.mp4

71944d7430c461f0cd6e7fd10cee7eb72786352a3678fc7bc0ae3d410f72aece  output/decrypted/sample_decrypted.mp4
```

Both SHA256 hashes match.

This confirms that the decrypted MP4 is byte-for-byte identical to the original MP4 used in the test.

---

# 3. Clear Key/CENC vs AES-128-CBC

| Feature | Clear Key + CENC | AES-128-CBC |
|---|---|---|
| Encryption scope | Media samples | Entire file |
| Encryption standard | AES-CTR with `cenc` | AES-128-CBC |
| Key management | KID + content KEY | KEY + IV |
| Media awareness | Yes | No |
| MP4 encryption metadata | Yes | No |
| DRM/EME integration | Supported through Clear Key EME workflows | No |
| Encryption tool | Shaka Packager | Python Cryptography |
| Output | Encrypted MP4 | Binary `.enc` file |
| Direct playback | Requires decryption or compatible EME player | Requires decryption first |
| Audio/video handling | Depends on selected packaged streams | Encrypts all file contents |
| Integrity authentication | Not provided by this workflow | Not provided by CBC alone |

## Key Difference

**Clear Key + CENC:**

The encryption process understands the media container and encrypts media samples. The MP4 retains the necessary protection metadata, including key identification and sample encryption information.

**AES-128-CBC:**

The encryption process treats the complete MP4 as binary data. It encrypts every byte of the file, including MP4 headers, video data, audio data, and metadata.

---

# 4. Validation Results

## Clear Key + CENC

| Test | Result |
|---|---|
| KID generation | Passed |
| Content KEY generation | Passed |
| Shaka Packager encryption | Passed |
| Encrypted MP4 generation | Passed |
| CENC metadata inspection | Passed |
| Shaka Packager decryption | Passed |
| Decrypted video playback | Passed |
| Full audio/video packaging | Pending |
| Browser EME playback | Pending |
| Full sample encryption verification | Pending |

## AES-128-CBC

| Test | Result |
|---|---|
| AES KEY generation | Passed |
| IV generation | Passed |
| AES-128-CBC encryption | Passed |
| Encrypted `.enc` generation | Passed |
| AES-128-CBC decryption | Passed |
| H.264 stream validation | Passed |
| AAC audio stream validation | Passed |
| Decrypted video playback | Passed |
| SHA256 comparison | Passed |

---

# 5. Security Considerations

- Keep encryption keys and IVs private.
- Do not commit `clear_key.json` or `aes_key.json` to a public Git repository.
- Restrict key-file permissions.
- Use separate keys for separate encryption operations in production.
- Never hardcode production encryption keys in source code.
- Securely manage and distribute decryption keys.

**Important AES-CBC limitation:** CBC provides confidentiality but does not authenticate encrypted data. A modified ciphertext may decrypt into corrupted data without necessarily producing a reliable error.

For production systems, consider authenticated encryption such as AES-GCM, or use a correctly implemented Encrypt-then-MAC construction with HMAC-SHA256.

This project uses AES-CBC for learning and demonstrating the requested encryption mode.

---

# 6. Useful Commands

### Inspect MP4 streams

```bash
ffprobe -v error \
-show_entries stream=codec_name \
-of default=noprint_wrappers=1 input/sample.mp4
```

### Play a video

```bash
ffplay input/sample.mp4
```

### Check file type

```bash
file output/encrypted/sample_encrypted.enc
```

### Compare file hashes

```bash
sha256sum input/sample.mp4 output/decrypted/sample_decrypted.mp4
```

### Check output file sizes

```bash
ls -lh input/ output/encrypted/ output/decrypted/
```

### Check key-file permissions

```bash
ls -l keys/
```

---

# 7. Technologies Used

- Linux / Ubuntu
- Python 3
- Shaka Packager
- FFmpeg / FFprobe / FFplay
- Python Cryptography
- AES-128-CBC
- AES-CTR
- Common Encryption (CENC)
- Clear Key / EME concepts
- SHA256

---

# 8. Project Summary

This project demonstrates two different approaches to video encryption and decryption.

1. **Clear Key + CENC:** Demonstrates media-aware encryption using Shaka Packager, with KID and content KEY management and CENC protection metadata.
2. **AES-128-CBC:** Demonstrates complete MP4 file encryption using Python, with separate KEY and IV generation, encryption, decryption, playback, and SHA256 integrity comparison.

The AES-128-CBC workflow has been validated with an exact SHA256 match between the original and decrypted files.

The Clear Key workflow has completed CLI-level encryption and decryption testing. Full audio/video packaging and browser-based EME playback remain future enhancements.
