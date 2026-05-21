# File Encryptor 🔐

A Python-based file encryption and decryption tool using symmetric encryption (AES-128). Encrypt any file type securely with a simple command-line interface.

## Features

✅ **Universal File Support** - Encrypt any file type (text, images, PDFs, videos, etc.)  
✅ **Strong Encryption** - Uses Fernet (AES-128 in CBC mode with HMAC authentication)  
✅ **Dual Interface** - Both GUI and CLI available  
✅ **Password & Key-Based** - Choose between password or key file encryption  
✅ **Batch Operations** - Encrypt/decrypt multiple files at once with glob patterns  
✅ **Activity Logging** - Track all encryption/decryption operations  
✅ **Safe by Default** - Original files remain untouched during encryption  
✅ **Error Handling** - Clear error messages and validation  

## Project Status

- [x] Setup Python environment
- [x] Install cryptography library
- [x] Key generation functions
- [x] Encrypt function
- [x] Decrypt function
- [x] CLI interface
- [x] Password-based encryption
- [x] Logging system
- [x] Batch operations
- [x] GUI interface
- [x] Testing
- [x] Documentation

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/billysambasi/file-encryptor.git
   cd file-encryptor
   ```

2. **Create and activate virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

## Usage

### GUI Interface (Recommended for Beginners)

Launch the graphical interface:

```powershell
python gui.py
```

The GUI provides:
- **Single File Tab** - Encrypt/decrypt individual files with browse buttons
- **Batch Operations Tab** - Process multiple files using patterns (*.txt, *.pdf)
- **Key Management Tab** - Generate new encryption keys
- **About Tab** - Information about the tool

Simply click buttons, browse for files, and let the interface guide you!

### Command-Line Interface (CLI)

### 1. Generate an Encryption Key

First, generate a secret key (only do this once):

```powershell
python encryptor.py generate-key
```

This creates a `secret.key` file. **Keep this safe!** Without it, you cannot decrypt your files.

### 2. Encrypt a File

Encrypt any file:

```powershell
python encryptor.py encrypt myfile.txt
```

This creates `myfile.txt.enc` (encrypted version). Your original file stays intact.

**Encrypt other file types:**
```powershell
python encryptor.py encrypt photo.jpg
python encryptor.py encrypt document.pdf
python encryptor.py encrypt video.mp4
```

### 3. Decrypt a File

Decrypt an encrypted file:

```powershell
python encryptor.py decrypt myfile.txt.enc
```

This restores the original `myfile.txt`.

### Advanced Options

**Use a custom key file:**
```powershell
python encryptor.py generate-key --output mykey.key
python encryptor.py encrypt file.txt --key mykey.key
python encryptor.py decrypt file.txt.enc --key mykey.key
```

**Get help:**
```powershell
python encryptor.py --help
python encryptor.py encrypt --help
```

**Batch operations:**
```powershell
# Encrypt all text files
python encryptor.py batch-encrypt "*.txt"

# Decrypt all encrypted files
python encryptor.py batch-decrypt "*.enc"

# Use password for batch operations
python encryptor.py batch-encrypt "*.pdf" --password
```

**View activity logs:**
```powershell
python encryptor.py logs
```

## How It Works

1. **Key Generation**: Creates a random 32-byte key using cryptographically secure methods
2. **Encryption**: Uses Fernet (symmetric encryption) to encrypt file contents
   - AES-128 in CBC mode
   - HMAC for authentication (prevents tampering)
   - Timestamp included (optional expiration)
3. **Decryption**: Reverses the process using the same key

## File Structure

```
file-encryptor/
├── gui.py                 # Graphical user interface
├── encryptor.py           # CLI interface
├── crypto_utils.py        # Core encryption functions
├── batch_operations.py    # Batch processing functions
├── logger.py              # Activity logging system
├── sample.txt             # Sample file for testing
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── .gitignore             # Prevents committing keys/encrypted files
└── venv/                  # Virtual environment (not in git)
```

## Security Notes

⚠️ **IMPORTANT:**
- **Never share your `.key` files** - Anyone with the key can decrypt your files
- **Backup your keys** - Store them securely (password manager, encrypted USB, etc.)
- **No key = No decryption** - If you lose the key, your files are permanently encrypted
- **This uses symmetric encryption** - Same key encrypts and decrypts (simpler but requires secure key storage)

🔒 **What This Tool Provides:**
- Strong encryption (AES-128)
- Authentication (HMAC prevents tampering)
- Protection against unauthorized access

❌ **What This Tool Does NOT Provide:**
- Password-based encryption (coming in extensions)
- Key management system
- Cloud backup
- Multi-user access control

## Testing

**Test the GUI:**
```powershell
python gui.py
```

**Test the CLI encryption system:**
```powershell
python crypto_utils.py
```

**Test batch operations:**
```powershell
python batch_operations.py
```

**Test logging system:**
```powershell
python logger.py
```

These automated tests show:
- Key generation
- File encryption
- File decryption
- Content verification
- Batch processing
- Activity logging

## Troubleshooting

**"Key file not found"**
- Generate a key first: `python encryptor.py generate-key`

**"Decryption failed"**
- Make sure you're using the correct key file
- Verify the file is actually encrypted (has `.enc` extension)

**"File not found"**
- Check the file path and spelling
- Use quotes for filenames with spaces: `"my file.txt"`

## Future Extensions

Potential enhancements:

- [ ] **File compression** - Compress before encrypting to save space
- [ ] **Cloud integration** - Direct upload to cloud storage
- [ ] **Key rotation** - Re-encrypt files with new keys
- [ ] **Secure file deletion** - Overwrite original files securely
- [ ] **Multi-language support** - Internationalization
- [ ] **Mobile app** - iOS/Android version

## Contributing

This is a learning project, but suggestions and improvements are welcome!

## License

MIT License - Feel free to use and modify for your own learning.

## Author

Built as a portfolio project to demonstrate:
- Python programming
- Cryptography concepts
- CLI development
- GUI development with Tkinter
- Batch processing
- Logging and error handling
- Security best practices
