#!/usr/bin/env python3
"""
File Encryptor CLI
Command-line interface for encrypting and decrypting files.
"""

import argparse
import sys
import os
import getpass

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.crypto_utils import (
    generate_key, save_key, load_key, encrypt_file, decrypt_file,
    encrypt_file_with_password, decrypt_file_with_password
)
from src.logger import get_log_summary
from src.batch_operations import (
    batch_encrypt_with_key, batch_decrypt_with_key,
    batch_encrypt_with_password, batch_decrypt_with_password,
    print_batch_summary
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
  
  # Batch encrypt multiple files
  python encryptor.py batch-encrypt "*.txt"
  
  # Batch decrypt multiple files
  python encryptor.py batch-decrypt "*.enc"
  
  # View activity logs
  python encryptor.py logs
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
    
    # Logs command
    logs_parser = subparsers.add_parser("logs", help="View encryption activity logs")
    
    # Batch encrypt command
    batch_encrypt_parser = subparsers.add_parser("batch-encrypt", help="Encrypt multiple files")
    batch_encrypt_parser.add_argument("pattern", help="File pattern (e.g., '*.txt', 'docs/*.pdf')")
    batch_encrypt_parser.add_argument(
        "--key", "-k",
        default="secret.key",
        help="Key file to use (default: secret.key)"
    )
    batch_encrypt_parser.add_argument(
        "--password", "-p",
        action="store_true",
        help="Use password-based encryption instead of key file"
    )
    
    # Batch decrypt command
    batch_decrypt_parser = subparsers.add_parser("batch-decrypt", help="Decrypt multiple files")
    batch_decrypt_parser.add_argument("pattern", help="File pattern (e.g., '*.enc')")
    batch_decrypt_parser.add_argument(
        "--key", "-k",
        default="secret.key",
        help="Key file to use (default: secret.key)"
    )
    batch_decrypt_parser.add_argument(
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
    
    elif args.command == "logs":
        print("=" * 60)
        print("ENCRYPTION ACTIVITY LOGS")
        print("=" * 60)
        
        summary = get_log_summary()
        
        if summary["total_entries"] == 0:
            print("\nNo activity logged yet.")
            print("Logs will appear here after you encrypt or decrypt files.")
        else:
            print(f"\n📊 Summary:")
            print(f"   Total operations: {summary['total_entries']}")
            print(f"   ✓ Encryptions: {summary['encryptions']}")
            print(f"   ✓ Decryptions: {summary['decryptions']}")
            print(f"   ✗ Errors: {summary['errors']}")
            
            print(f"\n📁 Full log file: logs/encryption.log")
            print(f"   View with: type logs\\encryption.log")
        
        print("=" * 60)
    
    elif args.command == "batch-encrypt":
        print("=" * 60)
        print("BATCH ENCRYPTION")
        print("=" * 60)
        
        # Password-based encryption
        if args.password:
            password = getpass.getpass("Enter password: ")
            password_confirm = getpass.getpass("Confirm password: ")
            
            if password != password_confirm:
                print("✗ Error: Passwords don't match")
                sys.exit(1)
            
            if len(password) < 8:
                print("✗ Error: Password must be at least 8 characters")
                sys.exit(1)
            
            results = batch_encrypt_with_password(args.pattern, password)
            print_batch_summary(results)
        
        # Key-based encryption
        else:
            if not os.path.exists(args.key):
                print(f"✗ Error: Key file '{args.key}' not found")
                print(f"   Generate a key first: python encryptor.py generate-key")
                sys.exit(1)
            
            results = batch_encrypt_with_key(args.pattern, args.key)
            print_batch_summary(results)
    
    elif args.command == "batch-decrypt":
        print("=" * 60)
        print("BATCH DECRYPTION")
        print("=" * 60)
        
        # Password-based decryption
        if args.password:
            password = getpass.getpass("Enter password: ")
            results = batch_decrypt_with_password(args.pattern, password)
            print_batch_summary(results)
        
        # Key-based decryption
        else:
            if not os.path.exists(args.key):
                print(f"✗ Error: Key file '{args.key}' not found")
                sys.exit(1)
            
            results = batch_decrypt_with_key(args.pattern, args.key)
            print_batch_summary(results)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
