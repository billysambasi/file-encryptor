"""
File Encryption/Decryption Utility
Provides functions for generating keys and encrypting/decrypting files.
"""

from cryptography.fernet import Fernet
import os


def generate_key():
    """
    Generate a new encryption key.
    
    Returns:
        bytes: A URL-safe base64-encoded 32-byte key
    """
    key = Fernet.generate_key()
    return key


def save_key(key, filename="secret.key"):
    """
    Save the encryption key to a file.
    
    Args:
        key (bytes): The encryption key to save
        filename (str): Name of the file to save the key to
    """
    with open(filename, "wb") as key_file:
        key_file.write(key)
    print(f"✓ Key saved to {filename}")


def load_key(filename="secret.key"):
    """
    Load an encryption key from a file.
    
    Args:
        filename (str): Name of the file containing the key
        
    Returns:
        bytes: The encryption key
    """
    with open(filename, "rb") as key_file:
        key = key_file.read()
    return key


if __name__ == "__main__":
    # Test the key generation
    print("Testing key generation...")
    test_key = generate_key()
    print(f"Generated key: {test_key}")
    print(f"Key length: {len(test_key)} bytes")
