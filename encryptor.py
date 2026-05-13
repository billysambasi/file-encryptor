#!/usr/bin/env python3
"""
File Encryptor CLI
Command-line interface for encrypting and decrypting files.
"""

import argparse
import sys
import os
from crypto_utils import generate_key, save_key, load_key, encrypt_file, decrypt_file


def main():
    parser = argparse.ArgumentParser(
        description="Encrypt and decrypt files securely",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a new encryption key
  python encryptor.py generate-key
  
  # Encrypt a file
  python encryptor.py encrypt myfile.txt
  
  # Decrypt a file
  python encryptor.py decrypt myfile.txt.enc
  
  # Use a custom key file
  python encryptor.py encrypt myfile.txt --key custom.key
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Generate key command
    gen_parser = subparsers.add_parser("generate-key", help="Generate a new encryption key")
    gen_parser.add_argument(
        "--output", "-o",
        default="secret.key",
        help="Output filename for the key (default: secret.key)"
    )
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a file")
    encrypt_parser.add_argument("file", help="File to encrypt")
    encrypt_parser.add_argument(
        "--key", "-k",
        default="secret.key",
        help="Key file to use (default: secret.key)"
    )
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a file")
    decrypt_parser.add_argument("file", help="File to decrypt (.enc)")
    decrypt_parser.add_argument(
        "--key", "-k",
        default="secret.key",
        help="Key file to use (default: secret.key)"
    )
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "generate-key":
        print(f"Generating new encryption key...")
        key = generate_key()
        save_key(key, args.output)
        print(f"\n⚠️  IMPORTANT: Keep {args.output} safe and secret!")
        print(f"   Without this key, you cannot decrypt your files.")
        
    elif args.command == "encrypt":
        # Check if file exists
        if not os.path.exists(args.file):
            print(f"✗ Error: File '{args.file}' not found")
            sys.exit(1)
        
        # Check if key exists
        if not os.path.exists(args.key):
            print(f"✗ Error: Key file '{args.key}' not found")
            print(f"   Generate a key first: python encryptor.py generate-key")
            sys.exit(1)
        
        # Load key and encrypt
        print(f"Loading key from {args.key}...")
        key = load_key(args.key)
        print(f"Encrypting {args.file}...")
        encrypt_file(args.file, key)
        print(f"\n✓ Success! Original file is still intact.")
        
    elif args.command == "decrypt":
        # Check if file exists
        if not os.path.exists(args.file):
            print(f"✗ Error: File '{args.file}' not found")
            sys.exit(1)
        
        # Check if key exists
        if not os.path.exists(args.key):
            print(f"✗ Error: Key file '{args.key}' not found")
            sys.exit(1)
        
        # Load key and decrypt
        print(f"Loading key from {args.key}...")
        key = load_key(args.key)
        print(f"Decrypting {args.file}...")
        result = decrypt_file(args.file, key)
        
        if result:
            print(f"\n✓ Success! File decrypted.")
        else:
            print(f"\n✗ Decryption failed. Wrong key?")
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
