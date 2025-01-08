# SecureEntry

## Overview

SecureEntry is a Python-based software designed to enhance security protocols by implementing robust authentication and encryption methods for Windows access. The program uses a combination of password hashing and encryption to store user credentials securely and authenticate users.

## Features

- User Registration: Securely register users with a username and password.
- User Authentication: Authenticate users with their credentials.
- Password Encryption: Passwords are encrypted using the Fernet symmetric encryption method.
- Secure Storage: User credentials are stored securely in a local SQLite database.

## Requirements

- Python 3.6 or later
- Required Python Libraries:
  - `cryptography`
  - `sqlite3`

You can install the required libraries using pip:

```bash
pip install cryptography
```

## Usage

1. Run the `secure_entry.py` script.

```bash
python secure_entry.py
```

2. Follow the on-screen prompts to register a new user or authenticate an existing user.

## Security Details

- Passwords are hashed using SHA-256 before encryption to enhance security.
- Passwords are encrypted using the Fernet symmetric encryption algorithm, which ensures that stored passwords are not easily reversible without the encryption key.
- The encryption key is stored locally in a file named `secret.key`. Ensure that this file is kept secure to prevent unauthorized access.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.