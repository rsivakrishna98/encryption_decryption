1. Clear Key (Cleartext method) – video is encrypted using AES, but the encryption key is kept in clear/readable form.
2. AES-CBC – video is encrypted using AES in Cipher Block Chaining mode.


    Original video ---> Generate AES KEY and IV ---> AES-128-CBC encryption + PKCS7 padding ---> Encrypted file
                        
                        ---> AES-128-CBC decryption + PKCS7 unpadding ---> Decrypted video ---> Play video using FFplay


1. Install the Python dependency
    cd ~/work/encryption_decryption/02-aes-cbc

    python3 -m venv venv
    source venv/bin/activate

    pip install cryptography

        # Verify:
            python -c "import cryptography; print(cryptography.__version__)"

2. File: scripts/generate_key.py
    -> KEY: The secret 128-bit value used for encryption and decryption.
    -> IV: The 128-bit initialization vector used to initialize the CBC encryption process.
    -> Both are required to decrypt the encrypted file correctly.

3. File: scripts/encrypt.py
    What happens during encryption?
        1. Python reads the original MP4 file.
        2. It loads the KEY and IV from aes_key.json.
        3. PKCS7 padding makes the input compatible with AES''s 16-byte block size.
        4. AES-CBC encrypts the data.
        5. Encrypted bytes are written to a .enc file.

4. File: scripts/decrypt.py
    What happens during decryption?
        1. Python reads the encrypted .enc file.
        2. It loads the KEY and IV from aes_key.json.
        3. AES-CBC decrypts the data.
        4. PKCS7 unpadding removes the padding added during encryption.
        5. Decrypted bytes are written to a new MP4 file.

5. Execute each step separately
    cd ~/work/encryption_decryption/02-aes-cbc

    # Step 1 — Generate KEY and IV
        python3 scripts/generate_key.py
    
            # Inspect generated file
                cat aes_key.json
                    It will contain hexadecimal representations of the KEY and IV. Keep this file secret.

    # Step 2 — Encrypt the original video
        python3 scripts/encrypt.py --input input/sample.mp4
    
    # Step 3 — Inspect the encrypted file
        file output/encrypted/sample_encrypted.enc

        # Check its size:
            ls -lh input/sample.mp4 output/encrypted/sample_encrypted.enc
                The encrypted file should not be treated as an MP4 video. It contains ciphertext.
    
    # Step 4 — Decrypt the encrypted file
        python3 scripts/decrypt.py --input output/encrypted/sample_encrypted.enc
    
    # Step 5 — Verify the decrypted video
        ffprobe -v error \
        -show_entries stream=codec_name \
        -of default=noprint_wrappers=1 \
        output/decrypted/sample_decrypted.mp4

        Expected Output:
            codec_name=h264
            code_name=aac
    
    # Step 6 — Play the decrypted video
        ffplay output/decrypted/sample_decrypted.mp4
    
    # Verify original and decrypted file integrity
        sha256sum \
        input/sample.mp4 \
        output/decrypted/sample_decrypted.mp4

            # Expected Output:
                Both SHA256 hashes should be identical because this workflow encrypts and decrypts the complete file without remuxing it.
                    71944d7430c461f0cd6e7fd10cee7eb72786352a3678fc7bc0ae3d410f72aece  input/sample.mp4
                    71944d7430c461f0cd6e7fd10cee7eb72786352a3678fc7bc0ae3d410f72aece  output/decrypted/sample_decrypted.mp4




# Remember this simple sequence
Original block	     XOR with	  Output
    M0	                IV	        C0
    M1	                C0	        C1
    M2	                C1	        C2
    M3	                C2	        C3

Your understanding should be:
1. IV helps encrypt the first block.
2. First encrypted block C0 helps encrypt the second block.
3. Second encrypted block C1 helps encrypt the third block.
4. This continues until the entire video is encrypted.



BLOCK | ORIGINAL DATA | XOR WITH | ENCRYPT USING | OUTPUT
M0    | M0            | IV       | KEY           | C0
M1    | M1            | C0       | KEY           | C1
M2    | M2            | C1       | KEY           | C2
M3    | M3            | C2       | KEY           | C3
M4    | M4            | C3       | KEY           | C4
M5    | M5            | C4       | KEY           | C5
M6    | M6            | C5       | KEY           | C6
M7    | M7            | C6       | KEY           | C7
M8    | M8            | C7       | KEY           | C8
M9    | M9            | C8       | KEY           | C9
M10   | M10           | C9       | KEY           | C10
M11   | M11           | C10      | KEY           | C11
M12   | M12           | C11      | KEY           | C12
M13   | M13           | C12      | KEY           | C13
M14   | M14           | C13      | KEY           | C14
M15   | M15           | C14      | KEY           | C15


# Actual first-block calculation
KEY:
5f1ef79b5aae392653793bdd5ad2dd53

IV:
a3e38b586253c3d61a6ecfa88f925fa1

M0 (original data):
000000206674797069736f6d00000200

XOR (M0 with IV):
a3e38b780427baa6731da0c58f925da1

AES encryption using KEY:

C0 (encrypted data):
f13e9b20859f75b44d562fe0266cc40e

# 2nd block calculation:
KEY:
5f1ef79b5aae392653793bdd5ad2dd53

M1 (Original second block):
0000001866726565000000016d646174

C0 (Previous encrypted block):
f13e9b20859f75b44d562fe0266cc40e

XOR (M1 with C0):
f13e9b38e3ed10d14d562fe14b08a57a

AES encryption using KEY:

C1 (Second encrypted block):
9e287e3e81eb038d09e21fc5568b6d4b


########################3
KEY  = 5f1ef79b5aae392653793bdd5ad2dd53
IV   = a3e38b586253c3d61a6ecfa88f925fa1

BLOCK | ORIGINAL DATA (M)                  | XOR WITH | ENCRYPTED OUTPUT (C)

M0    | 000000206674797069736f6d00000200  | IV       | f13e9b20859f75b44d562fe0266cc40e -> c0
M1    | 0000001866726565000000016d646174  | C0       | 9e287e3e81eb038d09e21fc5568b6d4b -> c1
M2    | Sample M2                         | C1       | C2
M3    | Sample M3                         | C2       | C3
M4    | Sample M4                         | C3       | C4
M5    | Sample M5                         | C4       | C5
M6    | Sample M6                         | C5       | C6
M7    | Sample M7                         | C6       | C7
M8    | Sample M8                         | C7       | C8
M9    | Sample M9                         | C8       | C9
M10   | Sample M10                        | C9       | C10
M11   | Sample M11                        | C10      | C11
M12   | Sample M12                        | C11      | C12
M13   | Sample M13                        | C12      | C13
M14   | Sample M14                        | C13      | C14
M15   | Sample M15                        | C14      | C15