"""
Test script for password-based encryption
Demonstrates how password encryption works
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.crypto_utils import encrypt_file_with_password, decrypt_file_with_password

print("=" * 60)
print("TESTING PASSWORD-BASED ENCRYPTION")
print("=" * 60)

# Create a test file
print("\n1. Creating test file...")
test_file = "secret_message.txt"
with open(test_file, "w") as f:
    f.write("This is a secret message protected by a password!\n")
    f.write("Password-based encryption is more user-friendly.\n")
    f.write("No need to manage key files!")
print(f"✓ Created {test_file}")

# Encrypt with password
print("\n2. Encrypting with password...")
password = "MySecurePassword123"
print(f"   Using password: {password}")
encrypted_file = encrypt_file_with_password(test_file, password)

# Show encrypted content
print("\n3. Encrypted file content (first 100 bytes):")
with open(encrypted_file, "rb") as f:
    content = f.read()
    print(f"   Salt (first 16 bytes): {content[:16].hex()}")
    print(f"   Encrypted data: {content[16:100]}...")

# Decrypt with correct password
print("\n4. Decrypting with CORRECT password...")
decrypted_file = decrypt_file_with_password(encrypted_file, password)

if decrypted_file:
    print("\n5. Decrypted content:")
    with open(decrypted_file, "r") as f:
        print(f"   {f.read()}")

# Try with wrong password
print("\n6. Testing with WRONG password...")
wrong_password = "WrongPassword456"
print(f"   Using password: {wrong_password}")
result = decrypt_file_with_password(encrypted_file, wrong_password)

if not result:
    print("   ✓ Correctly rejected wrong password!")

print("\n" + "=" * 60)
print("✓ Password-based encryption test complete!")
print("=" * 60)

print("\n📚 Key Concepts Demonstrated:")
print("   • Salt: Random data stored with encrypted file")
print("   • PBKDF2: Converts password to encryption key")
print("   • 480,000 iterations: Slows down brute-force attacks")
print("   • SHA-256: Hash algorithm used in key derivation")
