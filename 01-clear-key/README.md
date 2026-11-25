# Clear Key Encryption and Decryption Using CENC

## 1. Project Overview

This project demonstrates video encryption and decryption using **Clear Key with Common Encryption (CENC)** using Shaka Packager.

The implementation generates a Key ID (KID) and content encryption KEY, encrypts video samples, and decrypts the protected MP4 file using the same content KEY.

### Technologies

- Linux / Ubuntu
- Python 3
- Shaka Packager
- FFmpeg / FFprobe / FFplay
- Clear Key
- Common Encryption (CENC)
- AES-CTR

## 2. Project Structure

```text
01-clear-key/
├── input/
│   └── sample.mp4
├── keys/
│   └── clear_key.json
├── output/
│   ├── encrypted/
│   └── decrypted/
├── scripts/
│   ├── generate_key.py
│   ├── encrypt.py
│   └── decrypt.py
└── README.md
```

## 3. Understanding Clear Key and CENC

Before implementing encryption, understand these components.

| Component | Description |
|---|---|
| Clear Key | An EME key system that provides content keys directly |
| EME | Browser API for encrypted media playback |
| CENC | Common Encryption specification for media samples |
| KID | Key ID used to identify a content encryption key |
| KEY | Secret content encryption key |
| PSSH | Protection System Specific Header |
| AES-CTR | Encryption mode used by the `cenc` protection scheme |

**Important distinction:**

Clear Key is a key system, not an encryption algorithm.

CENC defines how media samples are encrypted and how encryption information is represented in the MP4 container.

The `cenc` protection scheme uses AES-CTR.

## 4. Encryption Architecture

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
            Decryption
                  |
                  v
           Decrypted MP4
```

## 5. Understanding KID and KEY

The key-generation script creates two random 128-bit values.

Example:

```json
{
    "kid": "0123456789abcdef0123456789abcdef",
    "key": "abcdef0123456789abcdef0123456789"
}
```

These are illustrative hexadecimal values.

### KID

KID means Key ID.

It identifies which content KEY should be used to decrypt the protected media.

### Content KEY

The content KEY is the actual secret used by the encryption algorithm.

Both values are 16 bytes long in this project.

**Remember:**

- KID identifies the key.
- KEY performs encryption and decryption.
- KID is not the encryption key itself.

## 6. Step 1: Generate KID and KEY

Navigate to the project:

```bash
cd ~/work/encryption_decryption/01-clear-key
```

Run:

```bash
python3 scripts/generate_key.py
```

The script generates:

```text
keys/clear_key.json
```

The generated KEY and KID should be kept private.

## 7. Step 2: Encrypt the Video

Run:

```bash
python3 scripts/encrypt.py --input input/sample.mp4
```

The script invokes Shaka Packager with:

```bash
--enable_raw_key_encryption
--protection_scheme cenc
```

For complete encryption without an initial clear lead, configure:

```bash
--clear_lead 0
```

Expected output:

```text
output/encrypted/sample_encrypted.mp4
```

### What happens internally?

1. Shaka Packager reads the input MP4.
2. It identifies the selected video stream.
3. It divides the media into encryption units/samples.
4. It uses the content KEY to encrypt media data using AES-CTR.
5. It adds the required protection metadata to the MP4.
6. It writes the encrypted MP4.

## 8. Understanding AES-CTR in CENC

The `cenc` scheme uses AES Counter Mode.

AES-CTR works differently from AES-CBC.

For each encryption block:

\[
S_i = AES_K(CTR_i)
\]

\[
C_i = M_i \oplus S_i
\]

Where:

- \(M_i\) = Plaintext data block
- \(K\) = Content KEY
- \(CTR_i\) = Counter input
- \(S_i\) = AES-generated keystream
- \(C_i\) = Ciphertext

The counter value is encrypted using AES, and the resulting keystream is XORed with plaintext.

### AES-CTR example

```text
Plaintext block (M₀)
        |
        |
Counter value (CTR₀)
        |
        v
AES encryption using KEY
        |
        v
Keystream (S₀)
        |
        v
M₀ XOR S₀
        |
        v
Ciphertext (C₀)
```

Unlike CBC, CTR does not XOR plaintext with the previous ciphertext block.

It generates a keystream from counter values and XORs that stream with plaintext.

## 9. Understanding MP4 Encryption Metadata

CENC adds protection information to the MP4 container.

Important MP4 boxes include:

| Box | Description |
|---|---|
| `sinf` | Protection information |
| `frma` | Original media format |
| `schm` | Protection scheme information |
| `schi` | Scheme-specific information |
| `tenc` | Track encryption defaults |
| `pssh` | Protection System Specific Header |
| `senc` | Sample encryption information |
| `saiz` | Auxiliary information sizes |
| `saio` | Auxiliary information offsets |

Inspect encryption metadata:

```bash
ffprobe -v trace \
output/encrypted/sample_encrypted.mp4 2>&1 \
| grep -Ei 'sinf|schm|tenc|encv|cenc|senc|saiz|saio|pssh'
```

These metadata boxes indicate that the MP4 contains CENC protection information.

## 10. Step 3: Decrypt the Video

Run:

```bash
python3 scripts/decrypt.py \
    --input output/encrypted/sample_encrypted.mp4
```

The decryption script uses:

```bash
--enable_raw_key_decryption
```

and supplies the same KID and content KEY.

Expected output:

```text
output/decrypted/sample_encrypted_decrypted.mp4
```

### What happens internally?

1. Shaka Packager reads the encrypted MP4.
2. It identifies the protected stream and its KID.
3. It uses the supplied content KEY.
4. It decrypts the protected media samples.
5. It reconstructs a clear MP4 output.

## 11. Step 4: Validate the Decrypted Video

Inspect the decrypted stream:

```bash
ffprobe -v error \
-show_entries stream=codec_name \
-of default=noprint_wrappers=1 \
output/decrypted/sample_encrypted_decrypted.mp4
```

Play the video:

```bash
ffplay output/decrypted/sample_encrypted_decrypted.mp4
```

Inspect whether encryption metadata remains:

```bash
ffprobe -v trace \
output/decrypted/sample_encrypted_decrypted.mp4 2>&1 \
| grep -Ei 'encv|sinf|schm|schi|tenc|senc|saiz|saio|pssh'
```

For the decrypted output, the encryption-specific boxes should no longer be present.

## 12. Browser EME Playback

Clear Key can also be used in browser-based EME playback workflows.

A typical architecture is:

```text
Encrypted DASH Media
        |
        v
    Shaka Player
        |
        v
 Browser EME API
        |
        v
  Clear Key System
        |
        v
 Content KEY
        |
        v
 Decrypted Playback
```

The current Python scripts demonstrate CLI-level encryption and decryption. A complete browser playback implementation additionally requires compatible encrypted DASH media, a manifest, and Shaka Player EME configuration.

## 13. Current Implementation Scope

| Test | Status |
|---|---|
| KID generation | Passed |
| Content KEY generation | Passed |
| CENC encryption | Passed |
| Encrypted MP4 generation | Passed |
| Encryption metadata inspection | Passed |
| CENC decryption | Passed |
| Decrypted video playback | Passed |
| Audio/video packaging | Pending |
| Browser EME playback | Pending |
| Full sample encryption verification | Pending |

**Note:** The current scripts select the video stream only. The original sample also contains AAC audio, so the present workflow is a video-only demonstration.

## 14. Security Considerations

- Keep the content KEY secret.
- Do not publish generated keys in GitHub.
- Restrict key-file permissions.
- Do not confuse KID with the secret KEY.
- Use secure key delivery and storage in production.
- Clear Key is useful for demonstrations and interoperability testing, but is not a replacement for a production DRM key-management system.

## 15. Summary

This project demonstrates:

1. Generation of KID and content KEY.
2. Encryption of video samples using AES-CTR through CENC.
3. Storage of encryption information in MP4 metadata.
4. Decryption using the same content KEY.
5. Validation of decrypted media using FFprobe and FFplay.

The key takeaway is that Clear Key and CENC provide a media-aware encryption workflow, unlike ordinary whole-file AES-CBC encryption.
