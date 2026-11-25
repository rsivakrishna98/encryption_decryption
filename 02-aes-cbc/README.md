# AES-128-CBC Video File Encryption and Decryption

## 1. Project Overview

This project demonstrates complete MP4 file encryption and decryption using AES-128-CBC (Advanced Encryption Standard - Cipher Block Chaining).

Unlike CENC, AES-CBC does not understand the MP4 file structure. It encrypts the complete file as binary data.

The implementation uses Python and the Cryptography library.

### Technologies

- Linux / Ubuntu
- Python 3
- Python Cryptography
- AES-128-CBC
- PKCS7 Padding
- FFmpeg
- FFprobe
- FFplay
- SHA256

## 2. Project Structure

```text
02-aes-cbc/
├── input/
│   └── sample.mp4
├── keys/
│   └── aes_key.json
├── output/
│   ├── encrypted/
│   │   └── sample_encrypted.enc
│   └── decrypted/
│       └── sample_decrypted.mp4
├── scripts/
│   ├── generate_key.py
│   ├── encrypt.py
│   └── decrypt.py
├── venv/
└── README.md
```

## 3. Understanding AES-128-CBC

AES is a symmetric encryption algorithm.

Symmetric encryption means the same secret KEY is used for both encryption and decryption.

AES supports three key lengths:

| AES Algorithm | KEY Size | Block Size |
|---|---:|---:|
| AES-128 | 128 bits (16 bytes) | 128 bits |
| AES-192 | 192 bits (24 bytes) | 128 bits |
| AES-256 | 256 bits (32 bytes) | 128 bits |

This project uses AES-128-CBC.

Important components:

| Component | Description |
|---|---|
| AES | Advanced Encryption Standard |
| CBC | Cipher Block Chaining |
| KEY | Secret encryption key |
| IV | Initialization Vector |
| XOR | Exclusive OR operation |
| PKCS7 | Padding scheme |
| Plaintext | Original unencrypted data |
| Ciphertext | Encrypted data |

## 4. AES-CBC Encryption Architecture

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
             Python Script
                   |
                   v
             AES-128-CBC
                   |
                   v
           Encrypted .enc File
                   |
                   v
             Python Script
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

## 5. Understanding Your Actual KEY and IV

The project generates a random AES KEY and IV.

Example from the demonstration:

```json
{
    "algorithm": "AES-128-CBC",
    "key": "5f1ef79b5aae392653793bdd5ad2dd53",
    "iv": "a3e38b586253c3d61a6ecfa88f925fa1"
}
```

These are the example values used to explain the encryption process. They should not be reused for production encryption.

### KEY

```text
5f1ef79b5aae392653793bdd5ad2dd53
```

- 32 hexadecimal characters.
- Each pair of hexadecimal characters represents one byte.
- Total size: 16 bytes.
- 16 bytes × 8 = 128 bits.

### IV

```text
a3e38b586253c3d61a6ecfa88f925fa1
```

- 32 hexadecimal characters.
- Total size: 16 bytes.
- AES-CBC requires a 16-byte IV.

### Convert HEX to bytes

```text
KEY = 5f 1e f7 9b 5a ae 39 26
      53 79 3b dd 5a d2 dd 53

IV  = a3 e3 8b 58 62 53 c3 d6
      1a 6e cf a8 8f 92 5f a1
```

## 6. Understanding AES-CBC Block Processing

AES has a fixed block size of 128 bits, which equals 16 bytes.

Therefore, the complete MP4 file is processed as a sequence of 16-byte plaintext blocks.

For explanation, we use:

```text
M₀ = First plaintext block
M₁ = Second plaintext block
M₂ = Third plaintext block

C₀ = First ciphertext block
C₁ = Second ciphertext block
C₂ = Third ciphertext block
```

Where:

- M represents plaintext.
- C represents ciphertext.
- K represents the AES KEY.
- IV represents the Initialization Vector.
- XOR represents Exclusive OR.

## 7. AES-CBC Encryption Formula

The first block:

\[
C_0 = E_K(M_0 \oplus IV)
\]

The second block:

\[
C_1 = E_K(M_1 \oplus C_0)
\]

The third block:

\[
C_2 = E_K(M_2 \oplus C_1)
\]

General formula:

\[
C_i = E_K(M_i \oplus C_{i-1})
\]

For the first block, the IV is used instead of previous ciphertext.

Here, \(E_K\) means AES encryption using KEY K.

## 8. Practical Encryption Example Using Your KEY and IV

We will calculate the first encryption block using the example KEY and IV above.

### Step 1: Define KEY and IV

```text
KEY = 5f1ef79b5aae392653793bdd5ad2dd53

IV  = a3e38b586253c3d61a6ecfa88f925fa1
```

### Step 2: Define the first plaintext block M₀

For this demonstration, assume the first 16 bytes of the MP4 file are:

```text
M₀ = 000000206674797069736f6d00000200
```

This is an illustrative MP4 header block, not necessarily the actual first 16 bytes of your sample file.

Split into bytes:

```text
M₀ = 00 00 00 20 66 74 79 70
     69 73 6f 6d 00 00 02 00
```

### Step 3: Perform XOR between M₀ and IV

Formula:

\[
X_0 = M_0 \oplus IV
\]

XOR rules:

| A | B | A XOR B |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

Calculate each byte:

| M₀ | IV | XOR |
|---|---|---|
| 00 | a3 | a3 |
| 00 | e3 | e3 |
| 00 | 8b | 8b |
| 20 | 58 | 78 |
| 66 | 62 | 04 |
| 74 | 53 | 27 |
| 79 | c3 | ba |
| 70 | d6 | a6 |
| 69 | 1a | 73 |
| 73 | 6e | 1d |
| 6f | cf | a0 |
| 6d | a8 | c5 |
| 00 | 8f | 8f |
| 00 | 92 | 92 |
| 02 | 5f | 5d |
| 00 | a1 | a1 |

Result:

```text
X₀ = a3e38b780427baa6731da0c58f925da1
```

This is the intermediate 16-byte value before AES encryption.

### Step 4: Apply AES encryption using KEY

Formula:

\[
C_0 = AES_K(X_0)
\]

Inputs:

```text
KEY:
5f1ef79b5aae392653793bdd5ad2dd53

AES INPUT:
a3e38b780427baa6731da0c58f925da1
```

AES encrypts the 16-byte input using the 128-bit KEY.

Output:

```text
C₀ = AES encryption output
```

The exact ciphertext value is calculated by the AES algorithm.

Important: XOR is not the AES encryption algorithm. XOR is one operation used by CBC before the AES block encryption.

### Step 5: Encrypt the second block M₁

Take the next 16 bytes of the MP4:

```text
M₁ = Next 16 bytes of the original MP4
```

Now XOR the plaintext block with the previous ciphertext block:

\[
X_1 = M_1 \oplus C_0
\]

Then encrypt:

\[
C_1 = AES_K(X_1)
\]

For the third block:

\[
C_2 = AES_K(M_2 \oplus C_1)
\]

This process continues until all file data has been encrypted.

## 9. AES-CBC Encryption Flow

```text
                 M₀
                  |
                  v
                 XOR <----- IV
                  |
                  v
           AES Encryption
              using KEY
                  |
                  v
                 C₀
                  |
                  v
                 XOR <----- M₁
                  |
                  v
           AES Encryption
              using KEY
                  |
                  v
                 C₁
                  |
                  v
                 XOR <----- M₂
                  |
                  v
           AES Encryption
              using KEY
                  |
                  v
                 C₂
                  |
                  v
                ...
```

**Important:** Each previous ciphertext block is used as the chaining input for the next plaintext block.

## 10. AES-CBC Decryption Formula

Decryption reverses the encryption process.

For the first block:

\[
M_0 = D_K(C_0) \oplus IV
\]

For the second block:

\[
M_1 = D_K(C_1) \oplus C_0
\]

For the third block:

\[
M_2 = D_K(C_2) \oplus C_1
\]

Where \(D_K\) represents AES decryption using the same KEY.

### Encryption vs Decryption

| Encryption | Decryption |
|---|---|
| Start with plaintext | Start with ciphertext |
| XOR with IV or previous ciphertext | AES decrypt first |
| AES encrypt | XOR with IV or previous ciphertext |
| Generate ciphertext | Recover plaintext |

The same KEY and IV are required to recover the original data.

## 11. PKCS7 Padding

AES operates on 16-byte blocks.

What happens if the file size is not divisible by 16?

For example:

```text
Original data size = 20 bytes
AES block size = 16 bytes
```

The first block contains 16 bytes.

The remaining block contains 4 bytes.

PKCS7 adds padding bytes to complete the second block.

In this example:

```text
Remaining data = 4 bytes

Required padding = 12 bytes

Padding value = 0c
```

The padded second block ends with twelve bytes of `0c`.

PKCS7 also adds a complete padding block when the original data size is already divisible by 16.

During decryption, the padding is removed to reconstruct the original data.

## 12. Step 1: Create Python Virtual Environment

Navigate to the project:

```bash
cd ~/work/encryption_decryption/02-aes-cbc
```

Create virtual environment:

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

Install the cryptography library:

```bash
pip install cryptography
```

Verify installation:

```bash
pip show cryptography
```

## 13. Step 2: Generate KEY and IV

Run:

```bash
python3 scripts/generate_key.py
```

This creates:

```text
keys/aes_key.json
```

The script generates:

- 16-byte AES KEY.
- 16-byte IV.
- Hexadecimal representations of both values.

The generated key file is protected with restrictive file permissions.

## 14. Step 3: Encrypt the MP4

Run:

```bash
python3 scripts/encrypt.py --input input/sample.mp4
```

The script performs:

1. Load KEY and IV from JSON.
2. Validate their lengths.
3. Initialize AES-128-CBC.
4. Read the MP4 file in 64 KB chunks.
5. Apply PKCS7 padding.
6. Perform AES-CBC encryption.
7. Write the encrypted binary output.

Expected output:

```text
output/encrypted/sample_encrypted.enc
```

### Python implementation concept

```python
cipher = Cipher(
    algorithms.AES(key),
    modes.CBC(iv)
)

encryptor = cipher.encryptor()

encrypted_data = encryptor.update(padded_data)
```

The cryptography library internally handles:

- Splitting the data into 16-byte AES blocks.
- CBC XOR chaining.
- AES encryption.
- Producing ciphertext.

You do not need to manually implement XOR in the actual encryption script.

## 15. Step 4: Decrypt the Encrypted File

Run:

```bash
python3 scripts/decrypt.py \
    --input output/encrypted/sample_encrypted.enc
```

The script performs:

1. Load the same KEY and IV.
2. Initialize AES-128-CBC decryption.
3. Read encrypted data in chunks.
4. Decrypt ciphertext blocks.
5. Remove PKCS7 padding.
6. Write the original MP4 data.

Expected output:

```text
output/decrypted/sample_decrypted.mp4
```

### Python implementation concept

```python
cipher = Cipher(
    algorithms.AES(key),
    modes.CBC(iv)
)

decryptor = cipher.decryptor()

decrypted_data = decryptor.update(chunk)
```

The cryptography library internally performs AES decryption and CBC XOR chaining.

## 16. Step 5: Validate the Decrypted MP4

Check the original video:

```bash
ffprobe -v error \
-show_entries stream=codec_name \
-of default=noprint_wrappers=1 input/sample.mp4
```

Check the decrypted video:

```bash
ffprobe -v error \
-show_entries stream=codec_name \
-of default=noprint_wrappers=1 \
output/decrypted/sample_decrypted.mp4
```

Expected:

```text
h264
aac
```

Play the decrypted video:

```bash
ffplay output/decrypted/sample_decrypted.mp4
```

## 17. Step 6: Verify SHA256 Integrity

Run:

```bash
sha256sum input/sample.mp4 \
output/decrypted/sample_decrypted.mp4
```

The expected test result from this project was:

```text
71944d7430c461f0cd6e7fd10cee7eb72786352a3678fc7bc0ae3d410f72aece  input/sample.mp4

71944d7430c461f0cd6e7fd10cee7eb72786352a3678fc7bc0ae3d410f72aece  output/decrypted/sample_decrypted.mp4
```

Both hashes match.

This confirms that the decrypted MP4 is byte-for-byte identical to the original file.

## 18. Important Security Considerations

- Never publish the AES KEY.
- Protect the KEY and IV configuration file.
- Use a fresh unpredictable IV for each encryption operation with a given key.
- Never reuse a KEY/IV pair for different messages.
- Store encryption keys securely.
- AES-CBC does not authenticate ciphertext.
- Use authenticated encryption such as AES-GCM for production systems, or correctly implement Encrypt-then-MAC with HMAC-SHA256.

This project uses AES-CBC for educational purposes and to demonstrate the requested encryption mode.

## 19. Validation Results

| Test | Result |
|---|---|
| AES KEY generation | Passed |
| IV generation | Passed |
| KEY length validation | Passed |
| IV length validation | Passed |
| AES-128-CBC encryption | Passed |
| Encrypted `.enc` generation | Passed |
| AES-128-CBC decryption | Passed |
| H.264 stream validation | Passed |
| AAC stream validation | Passed |
| Decrypted video playback | Passed |
| SHA256 comparison | Passed |

## 20. Project Summary

This project demonstrates complete file-level video encryption and decryption using AES-128-CBC.

The major concepts covered:

1. Symmetric encryption.
2. AES-128 block cipher.
3. KEY and IV generation.
4. XOR operation.
5. CBC chaining.
6. AES encryption and decryption.
7. PKCS7 padding and unpadding.
8. Python Cryptography implementation.
9. File-level encryption.
10. SHA256 integrity verification.

**Final takeaway:**

AES-CBC encrypts the complete MP4 file as binary data. Each 16-byte plaintext block is XORed with the IV or previous ciphertext block before AES encryption. During decryption, AES decryption is followed by XOR to recover the original plaintext.
