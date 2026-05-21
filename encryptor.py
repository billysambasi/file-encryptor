#!/usr/bin/env python3
"""
File Encryptor CLI
Command-line interface for encrypting and decrypting files.
"""

import argparse
import sys
import os
import getpass
from crypto_utils import (
    generate_key, save_key, load_key, encrypt_file, decrypt_file,
    encrypt_file_with_password, decrypt_file_with_password
)


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
    encrypt_parser.add_argument(
        "--password", "-p",
        action="store_true",
        help="Use password-based encryption instead of key file"
    )
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a file")
    decrypt_parser.add_argument("file", help="File to decrypt (.enc)")
    decrypt_parser.add_argument(
        "--key", "-k",
        default="secret.key",
        help="Key file to use (default: secret.key)"
    )
    decrypt_parser.add_argument(
        "--password", "-p",
        action="store_true",
        help="Use password-based decryption instead of key file"
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
        
        # Password-based encryption
        if args.password:
            print(f"Encrypting {args.file} with password...")
            password = getpass.getpass("Enter password: ")
            password_confirm = getpass.getpass("Confirm password: ")
            
            if password != password_confirm:
                print("✗ Error: Passwords don't match")
                sys.exit(1)
            
            if len(password) < 8:
                print("✗ Error: Password must be at least 8 characters")
                sys.exit(1)
            
            encrypt_file_with_password(args.file, password)
            print(f"\n✓ Success! Original file is still intact.")
            print(f"⚠️  Remember your password - you'll need it to decrypt!")
        
        # Key-based encryption
        else:
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
        
        # Password-based decryption
        if args.password:
            print(f"Decrypting {args.file} with password...")
            password = getpass.getpass("Enter password: ")
            
            result = decrypt_file_with_password(args.file, password)
            
            if result:
                print(f"\n✓ Success! File decrypted.")
            else:
                print(f"\n✗ Decryption failed. Wrong password?")
                sys.exit(1)
        
        # Key-based decryption
        else:
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
