from cryptography.fernet import Fernet

plain_message = '@Maixanh45'

def main():
    key = Fernet.generate_key()
    print('Encryption key: ', key)
    encoded_message = plain_message.encode()
    f = Fernet(key)
    encrypted_data = f.encrypt(encoded_message)
    print('Encrypted: ', encrypted_data)

def read_and_encrypt(data_name, file):
    with open(file) as plain_file:
        plain_data_list = plain_file.read().split('\n')
        key = Fernet.generate_key()
        print('Encryption key: ', key)
        encrypted_file_name = data_name + '.env'
        with open(encrypted_file_name, 'w') as encrypted_file:
            encrypted_file.write(key.decode()+'\n')
            for data_num in range(len(plain_data_list)):
                encrypted_data = encrypt(key, plain_data_list[data_num])
                print('encrypted_data: ', encrypted_data)
                encrypted_file.write(encrypted_data.decode()+'\n')
    print('DONE!')

def encrypt(key, plain_data_list):
    f = Fernet(key)
    encrypted_data = f.encrypt(plain_data_list.encode())
    print('Encrypted: ', encrypted_data)
    return encrypted_data

#read_and_encrypt('bb_account', 'bb_plain.txt')

main()