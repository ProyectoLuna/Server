import hashlib

m = hashlib.md5()

m.update(b"pass2hash")
m.update(b"salamiYork")

print(m.hexdigest())
