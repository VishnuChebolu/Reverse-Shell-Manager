import rsa
from Utilities.Encryption.rsa import encrypt, decrypt
# with open('publicKey.pem', 'rb') as p:
#     print(p.read())
#     # publicKey = rsa.PublicKey.load_pkcs1(p.read())


# print(publicKey)

with open('privateKey.pem', 'rb') as p:
    # print(p.read())
    privateKey = rsa.PrivateKey.load_pkcs1(p.read())

key = b'-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAmk+g3GdxD4hKYbpU4AEAUfp8ofDVtOoOAjSCgrCthwBac29j+8E2\ng4JLWs7SF8J5uDUZcRtSQYksuVoe36neCQziKWaFd9f7X9965tBKFc6GUBUokq4i\nIC/XAO+9dAZWjTGqO/CCNCNfqUHRErIh+5suaKw3fL2uKlPVn4ZGWzjSVOZ0QNgp\nKppD5XWQTwLixozcQm1pKhKqSq7WXBV2z+bgovOTXoSepWBhuRqg7BNRIs6wWMxb\nWassuu1eBDRbfpk4jOOOvq0JzMN27hLcgGSV0MIpNoUfjyYeNVgBDOl3Qc1nt1CU\n5WmYAT7oZJ75jO7WPQboOalQtB2c2P4MGQIDAQAB\n-----END RSA PUBLIC KEY-----\n'
publicKey = rsa.PublicKey.load_pkcs1(key)


message = input('Write your message here:')
ciphertext = encrypt(message, publicKey)
text = decrypt(ciphertext, privateKey)
print(f'Cipher text: {ciphertext}')
print(f'Message text: {text}')