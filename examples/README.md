# Examples

This folder contains sample files for testing the File Encryptor.

## Files

- **sample.txt** - Basic text file for testing single file encryption
- **doc1.txt, doc2.txt, doc3.txt** - Multiple files for testing batch operations
- **batch_test1.txt, batch_test2.txt, batch_test3.txt** - Files created by batch operation tests

## How to Use

### Test Single File Encryption

Using GUI:
1. Run `python run_gui.py` from the root directory
2. Go to "Single File" tab
3. Browse and select `examples/sample.txt`
4. Click "Encrypt File"

Using CLI:
```bash
python run_cli.py encrypt examples/sample.txt
```

### Test Batch Operations

Using GUI:
1. Run `python run_gui.py`
2. Go to "Batch Operations" tab
3. Enter pattern: `examples/doc*.txt`
4. Click "Batch Encrypt"

Using CLI:
```bash
python run_cli.py batch-encrypt "examples/doc*.txt"
```

## Creating Your Own Test Files

Feel free to add your own files to this folder for testing:
- Text files (.txt)
- Images (.jpg, .png)
- Documents (.pdf, .docx)
- Any file type you want to encrypt!

## Note

Encrypted files (.enc) are automatically excluded from git via .gitignore.
