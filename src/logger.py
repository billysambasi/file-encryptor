"""
Logging utility for file encryption operations
Tracks all encryption/decryption activities with timestamps
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


def setup_logger(log_dir="logs", log_file="encryption.log"):
    """
    Set up the logging system.
    
    Args:
        log_dir (str): Directory to store log files
        log_file (str): Name of the log file
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_path = os.path.join(log_dir, log_file)
    
    # Create logger
    logger = logging.getLogger("FileEncryptor")
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create rotating file handler (max 5MB per file, keep 3 backups)
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3
    )
    file_handler.setLevel(logging.INFO)
    
    # Create console handler for errors
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def log_key_generation(logger, key_file):
    """Log key generation event."""
    logger.info(f"Key generated and saved to: {key_file}")


def log_encryption(logger, filename, method="key", success=True):
    """
    Log file encryption event.
    
    Args:
        logger: Logger instance
        filename (str): Name of file encrypted
        method (str): "key" or "password"
        success (bool): Whether encryption succeeded
    """
    if success:
        logger.info(f"File encrypted: {filename} (method: {method})")
    else:
        logger.error(f"Encryption failed: {filename} (method: {method})")


def log_decryption(logger, filename, method="key", success=True):
    """
    Log file decryption event.
    
    Args:
        logger: Logger instance
        filename (str): Name of file decrypted
        method (str): "key" or "password"
        success (bool): Whether decryption succeeded
    """
    if success:
        logger.info(f"File decrypted: {filename} (method: {method})")
    else:
        logger.error(f"Decryption failed: {filename} (method: {method})")


def log_error(logger, operation, error_message):
    """
    Log an error event.
    
    Args:
        logger: Logger instance
        operation (str): What operation was being performed
        error_message (str): Error details
    """
    logger.error(f"{operation} - Error: {error_message}")


def get_log_summary(log_dir="logs", log_file="encryption.log"):
    """
    Get a summary of recent log entries.
    
    Args:
        log_dir (str): Directory containing log files
        log_file (str): Name of the log file
        
    Returns:
        dict: Summary statistics
    """
    log_path = os.path.join(log_dir, log_file)
    
    if not os.path.exists(log_path):
        return {
            "total_entries": 0,
            "encryptions": 0,
            "decryptions": 0,
            "errors": 0
        }
    
    total = 0
    encryptions = 0
    decryptions = 0
    errors = 0
    
    with open(log_path, "r") as f:
        for line in f:
            total += 1
            if "File encrypted:" in line:
                encryptions += 1
            elif "File decrypted:" in line:
                decryptions += 1
            elif "ERROR" in line:
                errors += 1
    
    return {
        "total_entries": total,
        "encryptions": encryptions,
        "decryptions": decryptions,
        "errors": errors
    }


if __name__ == "__main__":
    # Test the logging system
    print("Testing logging system...")
    
    logger = setup_logger()
    
    print("\n1. Testing key generation log...")
    log_key_generation(logger, "test.key")
    
    print("2. Testing encryption logs...")
    log_encryption(logger, "test.txt", method="key", success=True)
    log_encryption(logger, "secret.pdf", method="password", success=True)
    
    print("3. Testing decryption logs...")
    log_decryption(logger, "test.txt.enc", method="key", success=True)
    log_decryption(logger, "wrong.enc", method="password", success=False)
    
    print("4. Testing error log...")
    log_error(logger, "File encryption", "File not found: missing.txt")
    
    print("\n5. Getting log summary...")
    summary = get_log_summary()
    print(f"   Total entries: {summary['total_entries']}")
    print(f"   Encryptions: {summary['encryptions']}")
    print(f"   Decryptions: {summary['decryptions']}")
    print(f"   Errors: {summary['errors']}")
    
    print("\n✓ Logging test complete!")
    print(f"✓ Check the 'logs/encryption.log' file to see the logs")
