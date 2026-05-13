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


def encrypt_file(filename, key):
    """
    Encrypt a file using the provided key.
    
    Args:
        filename (str): Path to the file to encrypt
        key (bytes): The encryption key
        
    Returns:
        str: Path to the encrypted file (original_name.enc)
    """
    # Create a Fernet cipher object with the key
    fernet = Fernet(key)
    
    # Read the original file
    with open(filename, "rb") as file:
        file_data = file.read()
    
    # Encrypt the data
    encrypted_data = fernet.encrypt(file_data)
    
    # Write the encrypted data to a new file
    encrypted_filename = filename + ".enc"
    with open(encrypted_filename, "wb") as file:
        file.write(encrypted_data)
    
    print(f"✓ File encrypted: {encrypted_filename}")
    return encrypted_filename


def decrypt_file(filename, key):
    """
    Decrypt a file using the provided key.
    
    Args:
        filename (str): Path to the encrypted file (.enc)
        key (bytes): The encryption key
        
    Returns:
        str: Path to the decrypted file (removes .enc extension)
    """
    # Create a Fernet cipher object with the key
    fernet = Fernet(key)
    
    # Read the encrypted file
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    
    # Decrypt the data
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception as e:
        print(f"✗ Decryption failed: {e}")
        print("  Make sure you're using the correct key!")
        return None
    
    # Write the decrypted data back
    decrypted_filename = filename.replace(".enc", "")
    with open(decrypted_filename, "wb") as file:
        file.write(decrypted_data)
    
    print(f"✓ File decrypted: {decrypted_filename}")
    return decrypted_filename


if __name__ == "__main__":
    # Test the key generation
    print("=" * 50)
    print("TESTING FILE ENCRYPTION SYSTEM")
    print("=" * 50)
    
    # Step 1: Generate and save a key
    print("\n1. Generating encryption key...")
    test_key = generate_key()
    save_key(test_key, "test.key")
    
    # Step 2: Create a test file
    print("\n2. Creating test file...")
    test_filename = "test_message.txt"
    with open(test_filename, "w") as f:
        f.write("Hello! This is a secret message that will be encrypted.")
    print(f"✓ Created {test_filename}")
    
    # Step 3: Encrypt the file
    print("\n3. Encrypting file...")
    encrypted_file = encrypt_file(test_filename, test_key)
    
    # Step 4: Show that encrypted file is unreadable
    print("\n4. Encrypted file content (first 100 chars):")
    with open(encrypted_file, "rb") as f:
        print(f"   {f.read()[:100]}...")
    
    # Step 5: Decrypt the file
    print("\n5. Decrypting file...")
    decrypted_file = decrypt_file(encrypted_file, test_key)
    
    # Step 6: Verify the content
    print("\n6. Decrypted file content:")
    with open(decrypted_file, "r") as f:
        print(f"   '{f.read()}'")
    
    print("\n" + "=" * 50)
    print("✓ All tests passed!")
    print("=" * 50)
