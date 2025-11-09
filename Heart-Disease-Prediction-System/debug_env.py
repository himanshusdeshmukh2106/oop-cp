"""Debug script to check environment variables"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
print(f"Looking for .env at: {env_path}")
print(f"File exists: {env_path.exists()}")

if env_path.exists():
    load_dotenv(env_path)
    print("\n✓ Loaded .env file")
else:
    print("\n✗ .env file not found!")

print("\n" + "="*60)
print("ENVIRONMENT VARIABLES")
print("="*60)

vars_to_check = [
    'TWILIO_ACCOUNT_SID',
    'TWILIO_AUTH_TOKEN',
    'TWILIO_PHONE_NUMBER',
    'TEST_PHONE_NUMBER'
]

for var in vars_to_check:
    value = os.getenv(var, 'NOT SET')
    if value and value != 'NOT SET':
        # Show first 10 chars only for security
        display_value = value[:15] + '...' if len(value) > 15 else value
        print(f"{var}: {display_value}")
    else:
        print(f"{var}: ✗ NOT SET")

print("="*60)

# Try reading .env file directly
print("\n" + "="*60)
print("DIRECT .env FILE CONTENT")
print("="*60)
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and 'TWILIO' in line:
                # Mask sensitive data
                if '=' in line:
                    key, value = line.split('=', 1)
                    if len(value) > 15:
                        value = value[:15] + '...'
                    print(f"{key}={value}")
                else:
                    print(line)
