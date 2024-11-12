import random
from captcha.image import ImageCaptcha
import os

os.chdir('assets')

image=ImageCaptcha()

def captcha():
    code=''
    for i in range(5):
        code+=str(random.choice(range(10)))
    data=image.generate(code)
    image.write(code,f'{code}.png')
    return code

#print(captcha())