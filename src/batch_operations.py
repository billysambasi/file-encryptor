"""
Batch operations for encrypting/decrypting multiple files
Supports glob patterns and directory processing
"""

import os
import glob
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.crypto_utils import (
    encrypt_file, decrypt_file,
    encrypt_file_with_password, decrypt_file_with_password,
    load_key
)


def find_files(pattern):
    """
    Find files matching a pattern.
    
    Args:
        pattern (str): Glob pattern (e.g., "*.txt", "docs/*.pdf")
        
    Returns:
        list: List of matching file paths
    """
    files = glob.glob(pattern, recursive=True)
    # Filter out directories, only return files
    return [f for f in files if os.path.isfile(f)]


def batch_encrypt_with_key(pattern, key_file="secret.key"):
    """
    Encrypt multiple files using a key file.
    
    Args:
        pattern (str): Glob pattern to match files
        key_file (str): Path to the key file
        
    Returns:
        dict: Results with success/failure counts
    """
    # Find matching files
    files = find_files(pattern)
    
    if not files:
        print(f"✗ No files found matching pattern: {pattern}")
        return {"total": 0, "success": 0, "failed": 0, "files": []}
    
    # Load the key
    try:
        key = load_key(key_file)
    except FileNotFoundError:
        print(f"✗ Key file not found: {key_file}")
        return {"total": 0, "success": 0, "failed": 0, "files": []}
    
    print(f"Found {len(files)} file(s) to encrypt")
    print("=" * 60)
    
    results = {"total": len(files), "success": 0, "failed": 0, "files": []}
    
    for i, file in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing: {file}")
        try:
            encrypt_file(file, key)
            results["success"] += 1
            results["files"].append({"file": file, "status": "success"})
        except Exception as e:
            print(f"✗ Failed: {e}")
            results["failed"] += 1
            results["files"].append({"file": file, "status": "failed", "error": str(e)})
    
    return results


def batch_decrypt_with_key(pattern, key_file="secret.key"):
    """
    Decrypt multiple files using a key file.
    
    Args:
        pattern (str): Glob pattern to match files
        key_file (str): Path to the key file
        
    Returns:
        dict: Results with success/failure counts
    """
    # Find matching files
    files = find_files(pattern)
    
    if not files:
        print(f"✗ No files found matching pattern: {pattern}")
        return {"total": 0, "success": 0, "failed": 0, "files": []}
    
    # Load the key
    try:
        key = load_key(key_file)
    except FileNotFoundError:
        print(f"✗ Key file not found: {key_file}")
        return {"total": 0, "success": 0, "failed": 0, "files": []}
    
    print(f"Found {len(files)} file(s) to decrypt")
    print("=" * 60)
    
    results = {"total": len(files), "success": 0, "failed": 0, "files": []}
    
    for i, file in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing: {file}")
        result = decrypt_file(file, key)
        if result:
            results["success"] += 1
            results["files"].append({"file": file, "status": "success"})
        else:
            results["failed"] += 1
            results["files"].append({"file": file, "status": "failed"})
    
    return results


def batch_encrypt_with_password(pattern, password):
    """
    Encrypt multiple files using a password.
    
    Args:
        pattern (str): Glob pattern to match files
        password (str): Password for encryption
        
    Returns:
        dict: Results with success/failure counts
    """
    # Find matching files
    files = find_files(pattern)
    
    if not files:
        print(f"✗ No files found matching pattern: {pattern}")
        return {"total": 0, "success": 0, "failed": 0, "files": []}
    
    print(f"Found {len(files)} file(s) to encrypt")
    print("=" * 60)
    
    results = {"total": len(files), "success": 0, "failed": 0, "files": []}
    
    for i, file in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing: {file}")
        try:
            encrypt_file_with_password(file, password)
            results["success"] += 1
            results["files"].append({"file": file, "status": "success"})
        except Exception as e:
            print(f"✗ Failed: {e}")
            results["failed"] += 1
            results["files"].append({"file": file, "status": "failed", "error": str(e)})
    
    return results


def batch_decrypt_with_password(pattern, password):
    """
    Decrypt multiple files using a password.
    
    Args:
        pattern (str): Glob pattern to match files
        password (str): Password for decryption
        
    Returns:
        dict: Results with success/failure counts
    """
    # Find matching files
    files = find_files(pattern)
    
    if not files:
        print(f"✗ No files found matching pattern: {pattern}")
        return {"total": 0, "success": 0, "failed": 0, "files": []}
    
    print(f"Found {len(files)} file(s) to decrypt")
    print("=" * 60)
    
    results = {"total": len(files), "success": 0, "failed": 0, "files": []}
    
    for i, file in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing: {file}")
        result = decrypt_file_with_password(file, password)
        if result:
            results["success"] += 1
            results["files"].append({"file": file, "status": "success"})
        else:
            results["failed"] += 1
            results["files"].append({"file": file, "status": "failed"})
    
    return results


def print_batch_summary(results):
    """
    Print a summary of batch operation results.
    
    Args:
        results (dict): Results dictionary from batch operation
    """
    print("\n" + "=" * 60)
    print("BATCH OPERATION SUMMARY")
    print("=" * 60)
    print(f"Total files: {results['total']}")
    print(f"✓ Successful: {results['success']}")
    print(f"✗ Failed: {results['failed']}")
    
    if results['failed'] > 0:
        print("\nFailed files:")
        for item in results['files']:
            if item['status'] == 'failed':
                error = item.get('error', 'Unknown error')
                print(f"  • {item['file']} - {error}")
    
    print("=" * 60)


if __name__ == "__main__":
    # Test batch operations
    print("Testing batch operations...")
    
    # Create test files
    print("\n1. Creating test files...")
    test_files = ["batch_test1.txt", "batch_test2.txt", "batch_test3.txt"]
    for i, filename in enumerate(test_files, 1):
        with open(filename, "w") as f:
            f.write(f"This is test file #{i} for batch encryption.\n")
        print(f"   Created: {filename}")
    
    # Generate a key
    print("\n2. Generating test key...")
    from src.crypto_utils import generate_key, save_key
    key = generate_key()
    save_key(key, "batch_test.key")
    
    # Batch encrypt
    print("\n3. Batch encrypting files...")
    results = batch_encrypt_with_key("batch_test*.txt", "batch_test.key")
    print_batch_summary(results)
    
    # Batch decrypt
    print("\n4. Batch decrypting files...")
    results = batch_decrypt_with_key("batch_test*.txt.enc", "batch_test.key")
    print_batch_summary(results)
    
    print("\n✓ Batch operations test complete!")
