from random import randint
from hashlib import md5


def md5_encrypt(text: str):
    md5_obj = md5()
    md5_obj.update(text.encode('utf-8'))
    return md5_obj.hexdigest()


def random_code(lth: int):
    code = ""
    for i in range(lth):
        digit = randint(0, 9)
        code += str(digit)
    return code
