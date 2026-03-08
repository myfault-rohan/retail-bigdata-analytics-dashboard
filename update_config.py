import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

hasher = stauth.Hasher()
admin_hash = hasher.hash('admin123')
analyst_hash = hasher.hash('data123')

with open('ui/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

config['credentials']['usernames']['admin']['password'] = admin_hash
config['credentials']['usernames']['analyst']['password'] = analyst_hash

with open('ui/config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)

print("Updated config.yaml with full hashes.")
print(f"Admin hash length: {len(admin_hash)}")
print(f"Analyst hash length: {len(analyst_hash)}")
