from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64decode, b64encode

def xor(a: bytes, b: bytes):
    return bytes([_a ^ _b for _a, _b in zip(a, b)])

iv = Random.new().read(AES.block_size)
key = Random.new().read(AES.block_size)

cipher = AES.new(key, AES.MODE_CFB, iv)

username = 'thangpd11'
role = 1
usernamebytes = username.encode('utf-8')
usernamelen = len(usernamebytes)
plainbytes = len(usernamebytes).to_bytes(2, "little") + usernamebytes + role.to_bytes(1, "little")

# cipherbytes = cipher.encrypt(plainbytes)
cipherbytes = b64decode(b'tzRxbyN82l8uJK06ZdSQSI+kc1x1vnjPTLXL6w==')
iv = cipherbytes[:AES.block_size]
cipherbytes = cipherbytes[AES.block_size:]

new_role = 0
plainbytes_new = len(usernamebytes).to_bytes(2, "little") + usernamebytes + new_role.to_bytes(1, "little")

cipherbytes_new = xor(xor(plainbytes_new, plainbytes), cipherbytes)

ciphertext_new = b64encode(iv + cipherbytes_new)
print(ciphertext_new)
# new_cipher = AES.new(key, AES.MODE_CFB, iv)
# results = new_cipher.decrypt(cipherbytes_new)
# print(plainbytes)
# print(results)