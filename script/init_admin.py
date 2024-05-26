from web import models
from utils.encryption import md5_encrypt


models.Administrator.objects.create(
    active=1,
    username='caoruchen',
    password=md5_encrypt('crccrc'),
    phone='13012493015',
    email='caoruchen@stu.ouc.edu.cn',
)
