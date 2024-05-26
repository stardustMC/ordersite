import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ordersite.settings')
django.setup()

from web import models
from utils.encryption import md5_encrypt

models.Administrator.objects.create(
    active=1,
    username='caoruchen',
    password=md5_encrypt('crccrc'),
    phone='13012493015',
    email='caoruchen@stu.ouc.edu.cn',
)
