import streamlit_authenticator as stauth
import yaml

passwords = ['admin123', 'data123']

try:
    print("Trying Hasher(passwords).generate()...")
    hasher = stauth.Hasher(passwords)
    print(hasher.generate())
except Exception as e:
    print(f"Failed: {e}")

try:
    print("Trying Hasher.hash_passwords(passwords)...")
    print(stauth.Hasher.hash_passwords(passwords))
except Exception as e:
    print(f"Failed: {e}")

try:
    print("Trying stauth.Hasher().hash('admin123')...")
    print(stauth.Hasher().hash('admin123'))
except Exception as e:
    print(f"Failed: {e}")
