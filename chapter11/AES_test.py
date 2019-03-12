from Crypto.Cipher import AES

# 加密
tmp = AES.new(b'This is a key123', AES.MODE_CBC, b'This is an IV456')
message = b"The answer is no"
ciphertext = tmp.encrypt(message)
print(ciphertext)

# 解密
obj2 = AES.new(b'This is a key123', AES.MODE_CBC, b'This is an IV456')
s = obj2.decrypt(ciphertext)
print(s)