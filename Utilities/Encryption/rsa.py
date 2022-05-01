import rsa

def generateKeys():
    (publicKey, privateKey) = rsa.newkeys(2048)
    with open('publicKey.pem', 'wb') as p:
        p.write(publicKey.save_pkcs1('PEM'))
    with open('privateKey.pem', 'wb') as p:
        p.write(privateKey.save_pkcs1('PEM'))


def loadKeys():
    with open('publicKey.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open('privateKey.pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return publicKey, privateKey


def encrypt(message, key):
    return rsa.encrypt(message.encode('ascii'), key)



def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('ascii')
    except Exception as e:
        return e

# generateKeys()
# publicKey, privateKey =loadKeys()

# message = input('Write your message here:')
# ciphertext = encrypt(message, publicKey)
# text = decrypt(ciphertext, privateKey)
# print(f'Cipher text: {ciphertext}')
# print(f'Message text: {text}')
