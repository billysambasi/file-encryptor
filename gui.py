#!/usr/bin/env python3
"""
Graphical User Interface for File Encryptor
User-friendly interface for encrypting and decrypting files
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from crypto_utils import (
    generate_key, save_key, load_key,
    encrypt_file, decrypt_file,
    encrypt_file_with_password, decrypt_file_with_password
)
from batch_operations import (
    batch_encrypt_with_key, batch_decrypt_with_key,
    batch_encrypt_with_password, batch_decrypt_with_password
)


class FileEncryptorGUI:
    """Main GUI application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("File Encryptor 🔐")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Variables
        self.key_file = tk.StringVar(value="secret.key")
        self.use_password = tk.BooleanVar(value=False)
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Title
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            title_frame,
            text="🔐 File Encryptor",
            font=("Arial", 20, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Secure your files with encryption",
            font=("Arial", 10)
        )
        subtitle_label.pack()
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_single_file_tab()
        self.create_batch_tab()
        self.create_key_management_tab()
        self.create_about_tab()
        
        # Status bar
        self.status_bar = ttk.Label(
            self.root,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_single_file_tab(self):
        """Create the single file encryption/decryption tab"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="Single File")
        
        # File selection
        file_frame = ttk.LabelFrame(tab, text="File Selection", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        self.file_path = tk.StringVar()
        ttk.Label(file_frame, text="Selected file:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="Browse...", command=self.browse_file).grid(row=0, column=2)
        
        # Encryption method
        method_frame = ttk.LabelFrame(tab, text="Encryption Method", padding="10")
        method_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(
            method_frame,
            text="Use Key File",
            variable=self.use_password,
            value=False,
            command=self.toggle_method
        ).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Radiobutton(
            method_frame,
            text="Use Password",
            variable=self.use_password,
            value=True,
            command=self.toggle_method
        ).grid(row=1, column=0, sticky=tk.W)
        
        # Key file selection (shown when using key file)
        self.key_frame = ttk.Frame(method_frame)
        self.key_frame.grid(row=0, column=1, padx=20, sticky=tk.W)
        
        ttk.Label(self.key_frame, text="Key file:").pack(side=tk.LEFT)
        ttk.Entry(self.key_frame, textvariable=self.key_file, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.key_frame, text="Browse...", command=self.browse_key).pack(side=tk.LEFT)
        
        # Password entry (shown when using password)
        self.password_frame = ttk.Frame(method_frame)
        self.password_frame.grid(row=1, column=1, padx=20, sticky=tk.W)
        
        ttk.Label(self.password_frame, text="Password:").pack(side=tk.LEFT)
        self.password_entry = ttk.Entry(self.password_frame, show="*", width=30)
        self.password_entry.pack(side=tk.LEFT, padx=5)
        
        self.password_frame.grid_remove()  # Hide initially
        
        # Action buttons
        button_frame = ttk.Frame(tab, padding="10")
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame,
            text="🔒 Encrypt File",
            command=self.encrypt_single_file,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="🔓 Decrypt File",
            command=self.decrypt_single_file,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        # Output log
        log_frame = ttk.LabelFrame(tab, text="Output", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.single_log = scrolledtext.ScrolledText(log_frame, height=10, width=70)
        self.single_log.pack(fill=tk.BOTH, expand=True)
    
    def create_batch_tab(self):
        """Create the batch operations tab"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="Batch Operations")
        
        # Pattern selection
        pattern_frame = ttk.LabelFrame(tab, text="File Pattern", padding="10")
        pattern_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(pattern_frame, text="Pattern (e.g., *.txt, *.pdf):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.batch_pattern = tk.StringVar(value="*.txt")
        ttk.Entry(pattern_frame, textvariable=self.batch_pattern, width=40).grid(row=0, column=1, padx=5)
        
        ttk.Label(pattern_frame, text="Examples: *.txt, *.enc, docs/*.pdf").grid(row=1, column=0, columnspan=2, sticky=tk.W)
        
        # Encryption method for batch
        batch_method_frame = ttk.LabelFrame(tab, text="Encryption Method", padding="10")
        batch_method_frame.pack(fill=tk.X, pady=5)
        
        self.batch_use_password = tk.BooleanVar(value=False)
        
        ttk.Radiobutton(
            batch_method_frame,
            text="Use Key File",
            variable=self.batch_use_password,
            value=False,
            command=self.toggle_batch_method
        ).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Radiobutton(
            batch_method_frame,
            text="Use Password",
            variable=self.batch_use_password,
            value=True,
            command=self.toggle_batch_method
        ).grid(row=1, column=0, sticky=tk.W)
        
        # Key file for batch
        self.batch_key_frame = ttk.Frame(batch_method_frame)
        self.batch_key_frame.grid(row=0, column=1, padx=20, sticky=tk.W)
        
        ttk.Label(self.batch_key_frame, text="Key file:").pack(side=tk.LEFT)
        self.batch_key_file = tk.StringVar(value="secret.key")
        ttk.Entry(self.batch_key_frame, textvariable=self.batch_key_file, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.batch_key_frame, text="Browse...", command=self.browse_batch_key).pack(side=tk.LEFT)
        
        # Password for batch
        self.batch_password_frame = ttk.Frame(batch_method_frame)
        self.batch_password_frame.grid(row=1, column=1, padx=20, sticky=tk.W)
        
        ttk.Label(self.batch_password_frame, text="Password:").pack(side=tk.LEFT)
        self.batch_password_entry = ttk.Entry(self.batch_password_frame, show="*", width=30)
        self.batch_password_entry.pack(side=tk.LEFT, padx=5)
        
        self.batch_password_frame.grid_remove()  # Hide initially
        
        # Action buttons
        button_frame = ttk.Frame(tab, padding="10")
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame,
            text="🔒 Batch Encrypt",
            command=self.batch_encrypt_files,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="🔓 Batch Decrypt",
            command=self.batch_decrypt_files,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        # Output log
        log_frame = ttk.LabelFrame(tab, text="Output", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.batch_log = scrolledtext.ScrolledText(log_frame, height=10, width=70)
        self.batch_log.pack(fill=tk.BOTH, expand=True)
    
    def create_key_management_tab(self):
        """Create the key management tab"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="Key Management")
        
        # Generate key
        gen_frame = ttk.LabelFrame(tab, text="Generate New Key", padding="10")
        gen_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(gen_frame, text="Key filename:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.new_key_name = tk.StringVar(value="secret.key")
        ttk.Entry(gen_frame, textvariable=self.new_key_name, width=40).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            gen_frame,
            text="🔑 Generate Key",
            command=self.generate_new_key,
            width=20
        ).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Info
        info_frame = ttk.LabelFrame(tab, text="Important Information", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        info_text = """
🔐 Key Management Tips:

• Keep your key files safe and secure
• Never share your key files with anyone
• Backup your keys in a secure location
• Without the key, you cannot decrypt your files
• Use strong passwords (at least 8 characters)

⚠️ Security Notes:

• This tool uses AES-128 encryption (Fernet)
• Password-based encryption uses PBKDF2 with 480,000 iterations
• Each encrypted file is independent
• Original files are never modified during encryption
        """
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack()
    
    def create_about_tab(self):
        """Create the about tab"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="About")
        
        about_text = """
🔐 File Encryptor
Version 1.0

A secure file encryption tool built with Python.

Features:
✓ Single file encryption/decryption
✓ Batch operations with glob patterns
✓ Key-based and password-based encryption
✓ Activity logging
✓ User-friendly GUI

Technology:
• Python 3
• Cryptography library (Fernet/AES-128)
• Tkinter GUI
• PBKDF2 key derivation

Security:
• AES-128 encryption in CBC mode
• HMAC authentication
• 480,000 PBKDF2 iterations
• Cryptographically secure random keys

Built as a portfolio project to demonstrate:
• Python programming
• Cryptography concepts
• GUI development
• Security best practices

© 2026 - MIT License
        """
        
        about_label = ttk.Label(tab, text=about_text, justify=tk.LEFT, font=("Arial", 10))
        about_label.pack(pady=20)
    
    # Helper methods
    
    def toggle_method(self):
        """Toggle between key file and password method"""
        if self.use_password.get():
            self.key_frame.grid_remove()
            self.password_frame.grid()
        else:
            self.password_frame.grid_remove()
            self.key_frame.grid()
    
    def toggle_batch_method(self):
        """Toggle between key file and password method for batch"""
        if self.batch_use_password.get():
            self.batch_key_frame.grid_remove()
            self.batch_password_frame.grid()
        else:
            self.batch_password_frame.grid_remove()
            self.batch_key_frame.grid()
    
    def browse_file(self):
        """Browse for a file to encrypt/decrypt"""
        filename = filedialog.askopenfilename(title="Select a file")
        if filename:
            self.file_path.set(filename)
    
    def browse_key(self):
        """Browse for a key file"""
        filename = filedialog.askopenfilename(
            title="Select key file",
            filetypes=[("Key files", "*.key"), ("All files", "*.*")]
        )
        if filename:
            self.key_file.set(filename)
    
    def browse_batch_key(self):
        """Browse for a key file for batch operations"""
        filename = filedialog.askopenfilename(
            title="Select key file",
            filetypes=[("Key files", "*.key"), ("All files", "*.*")]
        )
        if filename:
            self.batch_key_file.set(filename)
    
    def log_message(self, log_widget, message):
        """Add a message to a log widget"""
        log_widget.insert(tk.END, message + "\n")
        log_widget.see(tk.END)
        self.root.update()
    
    def clear_log(self, log_widget):
        """Clear a log widget"""
        log_widget.delete(1.0, tk.END)
    
    def set_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
        self.root.update()
    
    # Action methods
    
    def encrypt_single_file(self):
        """Encrypt a single file"""
        file_path = self.file_path.get()
        
        if not file_path:
            messagebox.showerror("Error", "Please select a file to encrypt")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"File not found: {file_path}")
            return
        
        self.clear_log(self.single_log)
        self.set_status("Encrypting...")
        
        def encrypt_thread():
            try:
                if self.use_password.get():
                    password = self.password_entry.get()
                    if len(password) < 8:
                        messagebox.showerror("Error", "Password must be at least 8 characters")
                        return
                    
                    self.log_message(self.single_log, f"Encrypting: {file_path}")
                    self.log_message(self.single_log, "Method: Password-based")
                    result = encrypt_file_with_password(file_path, password)
                    self.log_message(self.single_log, f"✓ Success: {result}")
                else:
                    key_file = self.key_file.get()
                    if not os.path.exists(key_file):
                        messagebox.showerror("Error", f"Key file not found: {key_file}")
                        return
                    
                    self.log_message(self.single_log, f"Encrypting: {file_path}")
                    self.log_message(self.single_log, f"Key file: {key_file}")
                    key = load_key(key_file)
                    result = encrypt_file(file_path, key)
                    self.log_message(self.single_log, f"✓ Success: {result}")
                
                self.set_status("Encryption complete")
                messagebox.showinfo("Success", "File encrypted successfully!")
            except Exception as e:
                self.log_message(self.single_log, f"✗ Error: {e}")
                self.set_status("Encryption failed")
                messagebox.showerror("Error", f"Encryption failed: {e}")
        
        threading.Thread(target=encrypt_thread, daemon=True).start()
    
    def decrypt_single_file(self):
        """Decrypt a single file"""
        file_path = self.file_path.get()
        
        if not file_path:
            messagebox.showerror("Error", "Please select a file to decrypt")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"File not found: {file_path}")
            return
        
        self.clear_log(self.single_log)
        self.set_status("Decrypting...")
        
        def decrypt_thread():
            try:
                if self.use_password.get():
                    password = self.password_entry.get()
                    
                    self.log_message(self.single_log, f"Decrypting: {file_path}")
                    self.log_message(self.single_log, "Method: Password-based")
                    result = decrypt_file_with_password(file_path, password)
                    
                    if result:
                        self.log_message(self.single_log, f"✓ Success: {result}")
                        self.set_status("Decryption complete")
                        messagebox.showinfo("Success", "File decrypted successfully!")
                    else:
                        self.log_message(self.single_log, "✗ Decryption failed")
                        self.set_status("Decryption failed")
                        messagebox.showerror("Error", "Decryption failed. Wrong password?")
                else:
                    key_file = self.key_file.get()
                    if not os.path.exists(key_file):
                        messagebox.showerror("Error", f"Key file not found: {key_file}")
                        return
                    
                    self.log_message(self.single_log, f"Decrypting: {file_path}")
                    self.log_message(self.single_log, f"Key file: {key_file}")
                    key = load_key(key_file)
                    result = decrypt_file(file_path, key)
                    
                    if result:
                        self.log_message(self.single_log, f"✓ Success: {result}")
                        self.set_status("Decryption complete")
                        messagebox.showinfo("Success", "File decrypted successfully!")
                    else:
                        self.log_message(self.single_log, "✗ Decryption failed")
                        self.set_status("Decryption failed")
                        messagebox.showerror("Error", "Decryption failed. Wrong key?")
            except Exception as e:
                self.log_message(self.single_log, f"✗ Error: {e}")
                self.set_status("Decryption failed")
                messagebox.showerror("Error", f"Decryption failed: {e}")
        
        threading.Thread(target=decrypt_thread, daemon=True).start()
    
    def batch_encrypt_files(self):
        """Batch encrypt files"""
        pattern = self.batch_pattern.get()
        
        if not pattern:
            messagebox.showerror("Error", "Please enter a file pattern")
            return
        
        self.clear_log(self.batch_log)
        self.set_status("Batch encrypting...")
        
        def batch_encrypt_thread():
            try:
                if self.batch_use_password.get():
                    password = self.batch_password_entry.get()
                    if len(password) < 8:
                        messagebox.showerror("Error", "Password must be at least 8 characters")
                        return
                    
                    self.log_message(self.batch_log, f"Pattern: {pattern}")
                    self.log_message(self.batch_log, "Method: Password-based")
                    self.log_message(self.batch_log, "=" * 50)
                    
                    # Redirect output to log
                    import sys
                    from io import StringIO
                    old_stdout = sys.stdout
                    sys.stdout = StringIO()
                    
                    results = batch_encrypt_with_password(pattern, password)
                    
                    output = sys.stdout.getvalue()
                    sys.stdout = old_stdout
                    
                    self.log_message(self.batch_log, output)
                    self.log_message(self.batch_log, f"\n✓ Encrypted: {results['success']}")
                    self.log_message(self.batch_log, f"✗ Failed: {results['failed']}")
                else:
                    key_file = self.batch_key_file.get()
                    if not os.path.exists(key_file):
                        messagebox.showerror("Error", f"Key file not found: {key_file}")
                        return
                    
                    self.log_message(self.batch_log, f"Pattern: {pattern}")
                    self.log_message(self.batch_log, f"Key file: {key_file}")
                    self.log_message(self.batch_log, "=" * 50)
                    
                    # Redirect output to log
                    import sys
                    from io import StringIO
                    old_stdout = sys.stdout
                    sys.stdout = StringIO()
                    
                    results = batch_encrypt_with_key(pattern, key_file)
                    
                    output = sys.stdout.getvalue()
                    sys.stdout = old_stdout
                    
                    self.log_message(self.batch_log, output)
                    self.log_message(self.batch_log, f"\n✓ Encrypted: {results['success']}")
                    self.log_message(self.batch_log, f"✗ Failed: {results['failed']}")
                
                self.set_status("Batch encryption complete")
                messagebox.showinfo("Success", f"Encrypted {results['success']} file(s)")
            except Exception as e:
                self.log_message(self.batch_log, f"✗ Error: {e}")
                self.set_status("Batch encryption failed")
                messagebox.showerror("Error", f"Batch encryption failed: {e}")
        
        threading.Thread(target=batch_encrypt_thread, daemon=True).start()
    
    def batch_decrypt_files(self):
        """Batch decrypt files"""
        pattern = self.batch_pattern.get()
        
        if not pattern:
            messagebox.showerror("Error", "Please enter a file pattern")
            return
        
        self.clear_log(self.batch_log)
        self.set_status("Batch decrypting...")
        
        def batch_decrypt_thread():
            try:
                if self.batch_use_password.get():
                    password = self.batch_password_entry.get()
                    
                    self.log_message(self.batch_log, f"Pattern: {pattern}")
                    self.log_message(self.batch_log, "Method: Password-based")
                    self.log_message(self.batch_log, "=" * 50)
                    
                    # Redirect output to log
                    import sys
                    from io import StringIO
                    old_stdout = sys.stdout
                    sys.stdout = StringIO()
                    
                    results = batch_decrypt_with_password(pattern, password)
                    
                    output = sys.stdout.getvalue()
                    sys.stdout = old_stdout
                    
                    self.log_message(self.batch_log, output)
                    self.log_message(self.batch_log, f"\n✓ Decrypted: {results['success']}")
                    self.log_message(self.batch_log, f"✗ Failed: {results['failed']}")
                else:
                    key_file = self.batch_key_file.get()
                    if not os.path.exists(key_file):
                        messagebox.showerror("Error", f"Key file not found: {key_file}")
                        return
                    
                    self.log_message(self.batch_log, f"Pattern: {pattern}")
                    self.log_message(self.batch_log, f"Key file: {key_file}")
                    self.log_message(self.batch_log, "=" * 50)
                    
                    # Redirect output to log
                    import sys
                    from io import StringIO
                    old_stdout = sys.stdout
                    sys.stdout = StringIO()
                    
                    results = batch_decrypt_with_key(pattern, key_file)
                    
                    output = sys.stdout.getvalue()
                    sys.stdout = old_stdout
                    
                    self.log_message(self.batch_log, output)
                    self.log_message(self.batch_log, f"\n✓ Decrypted: {results['success']}")
                    self.log_message(self.batch_log, f"✗ Failed: {results['failed']}")
                
                self.set_status("Batch decryption complete")
                messagebox.showinfo("Success", f"Decrypted {results['success']} file(s)")
            except Exception as e:
                self.log_message(self.batch_log, f"✗ Error: {e}")
                self.set_status("Batch decryption failed")
                messagebox.showerror("Error", f"Batch decryption failed: {e}")
        
        threading.Thread(target=batch_decrypt_thread, daemon=True).start()
    
    def generate_new_key(self):
        """Generate a new encryption key"""
        key_name = self.new_key_name.get()
        
        if not key_name:
            messagebox.showerror("Error", "Please enter a key filename")
            return
        
        if os.path.exists(key_name):
            if not messagebox.askyesno("Confirm", f"{key_name} already exists. Overwrite?"):
                return
        
        try:
            key = generate_key()
            save_key(key, key_name)
            messagebox.showinfo("Success", f"Key generated and saved to {key_name}")
            self.set_status(f"Key generated: {key_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate key: {e}")


def main():
    """Main entry point for the GUI"""
    root = tk.Tk()
    app = FileEncryptorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
