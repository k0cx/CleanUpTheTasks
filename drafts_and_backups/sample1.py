from cryptography.fernet import Fernet
from pathlib import Path
import json


cutt_data_dir = Path.home() / "CUTT"

generated_key = Fernet.generate_key()
decoded_key = generated_key.decode("utf-8")
cipher_key = decoded_key.encode("utf-8")
print("======")
print(generated_key)
print(decoded_key)
print(cipher_key)

cipher = Fernet(cipher_key)

data = {"client_uid": cipher_key.decode("utf-8"), "login": "login"}

settings_json = cutt_data_dir / "settings.json"
with open(settings_json, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

text = b"My super secret message"
encrypted_text = cipher.encrypt(text)

print(encrypted_text)

decrypted_text = cipher.decrypt(encrypted_text)
print(decrypted_text.decode("utf-8"))  # 'My super secret message'
