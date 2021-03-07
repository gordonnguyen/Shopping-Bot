from cryptography.fernet import Fernet

plain_message = '@Maixanh45'

def main():
    key = Fernet.generate_key()
    print('Encryption key: ', key)
    encoded_message = plain_message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    print('Encrypted: ', encrypted_message)

main()