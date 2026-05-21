# Project Structure Documentation

This document explains the organization of the File Encryptor project.

## Directory Layout

```
file-encryptor/
├── src/                       # Source code (main application)
├── tests/                     # Test files and test suite
├── examples/                  # Sample files for testing
├── docs/                      # Additional documentation
├── logs/                      # Activity logs (auto-generated)
├── venv/                      # Virtual environment (not in git)
├── run_gui.py                 # GUI launcher
├── run_cli.py                 # CLI launcher
├── requirements.txt           # Dependencies
├── README.md                  # Main documentation
└── .gitignore                 # Git ignore rules
```

## Source Code (`src/`)

Contains all the main application code:

### Core Modules

- **`__init__.py`** - Package initialization with version info
- **`crypto_utils.py`** - Core encryption/decryption functions
  - Key generation and management
  - File encryption/decryption (key-based)
  - Password-based encryption/decryption
  - PBKDF2 key derivation

- **`logger.py`** - Activity logging system
  - Log setup and configuration
  - Operation logging (encrypt/decrypt)
  - Log rotation (5MB max, 3 backups)
  - Log summary statistics

- **`batch_operations.py`** - Batch file processing
  - Glob pattern matching
  - Batch encryption/decryption
  - Progress tracking
  - Result summaries

### User Interfaces

- **`encryptor.py`** - Command-line interface (CLI)
  - Argument parsing with argparse
  - Single file operations
  - Batch operations
  - Key generation
  - Log viewing

- **`gui.py`** - Graphical user interface (GUI)
  - Tkinter-based interface
  - Tabbed layout (Single File, Batch, Key Management, About)
  - File browsing dialogs
  - Threaded operations (non-blocking)
  - Real-time output logs

## Tests (`tests/`)

Contains test files and test suite:

- **`run_all_tests.py`** - Comprehensive test suite
  - Tests all core functionality
  - Automated verification
  - Cleanup after tests
  - Summary report

- **`test_password.py`** - Password encryption demonstration
  - Shows password-based encryption flow
  - Demonstrates salt usage
  - Tests wrong password rejection

### Running Tests

```bash
# Run all tests
python tests/run_all_tests.py

# Run specific test
python tests/test_password.py
```

## Examples (`examples/`)

Sample files for testing the encryptor:

- **`README.md`** - Usage instructions for examples
- **`sample.txt`** - Basic text file
- **`doc1.txt, doc2.txt, doc3.txt`** - Multiple files for batch testing
- **`batch_test*.txt`** - Files created by batch tests

### Using Examples

```bash
# Encrypt a single example
python run_cli.py encrypt examples/sample.txt

# Batch encrypt examples
python run_cli.py batch-encrypt "examples/doc*.txt"
```

## Documentation (`docs/`)

Additional project documentation:

- **`PROJECT_STRUCTURE.md`** - This file
- Future: API documentation, architecture diagrams, etc.

## Launcher Scripts

### `run_gui.py`

Launches the graphical interface:
```bash
python run_gui.py
```

- Easy to use for beginners
- Visual file selection
- No command-line knowledge needed

### `run_cli.py`

Launches the command-line interface:
```bash
python run_cli.py --help
```

- Powerful for advanced users
- Scriptable and automatable
- Batch operations support

## Auto-Generated Directories

### `logs/`

Created automatically when logging is first used:
- **`encryption.log`** - Main activity log
- **`encryption.log.1, .2, .3`** - Rotated backups

### `__pycache__/`

Python bytecode cache (ignored by git):
- Speeds up module loading
- Automatically managed by Python

## Configuration Files

### `requirements.txt`

Python package dependencies:
```
cryptography>=41.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

### `.gitignore`

Prevents committing sensitive/generated files:
- `*.key` - Encryption keys
- `*.enc` - Encrypted files
- `logs/` - Log files
- `venv/` - Virtual environment
- `__pycache__/` - Python cache

## Import Structure

The project uses relative imports within the `src/` package:

```python
# In src/encryptor.py
from src.crypto_utils import encrypt_file
from src.logger import setup_logger
from src.batch_operations import batch_encrypt_with_key
```

Launcher scripts add the parent directory to the path:
```python
# In run_gui.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from src.gui import main
```

## Development Workflow

### Adding New Features

1. Add code to appropriate module in `src/`
2. Update imports if needed
3. Add tests to `tests/`
4. Update documentation
5. Test thoroughly
6. Commit and push

### Testing Changes

```bash
# Test specific module
python src/crypto_utils.py

# Test full suite
python tests/run_all_tests.py

# Test GUI
python run_gui.py

# Test CLI
python run_cli.py --help
```

### Git Workflow

```bash
# Check status
git status

# Stage changes
git add src/module.py tests/test_module.py

# Commit with message
git commit -m "Add feature X"

# Push to remote
git push origin main
```

## Best Practices

### Code Organization

- Keep related functionality together
- One module = one responsibility
- Clear, descriptive names
- Comprehensive docstrings

### Testing

- Test after every change
- Run full test suite before committing
- Add tests for new features
- Keep tests independent

### Documentation

- Update README for user-facing changes
- Document complex algorithms
- Keep examples up to date
- Comment non-obvious code

### Security

- Never commit `.key` files
- Never commit encrypted files with real data
- Keep `requirements.txt` updated
- Review security implications of changes

## Future Enhancements

Potential additions to the structure:

- `docs/api/` - API documentation
- `docs/architecture/` - System design docs
- `tests/unit/` - Unit tests
- `tests/integration/` - Integration tests
- `scripts/` - Utility scripts
- `config/` - Configuration files

## Questions?

Refer to:
- Main README.md for usage
- examples/README.md for testing
- Code docstrings for API details
- This file for structure questions
