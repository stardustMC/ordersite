import os
import sys
import django
from random import randint

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ordersite.settings')
django.setup()


from web import models
from utils.encryption import md5_encrypt

# initialize prior
prior_count = 5
for i in range(prior_count):
    models.Prior.objects.create(
        title="会员{}".format(i),
        discount=100 - i * prior_count,
        active=1,
    )

# initialize price policy
models.PricePolicy.objects.create(count=1000, price=20)
models.PricePolicy.objects.create(count=2000, price=35)
models.PricePolicy.objects.create(count=5000, price=80)

# initialize customer
models.Customer.objects.create(
        active=1,
        username='caoruchen',
        password=md5_encrypt('crccrc'),
        phone='13012493015',
        email='549389490@qq.com',
        balance=20000,
        prior_id=1,
        creator_id=1,
    )

for i in range(50):
    models.Customer.objects.create(
        active=1,
        username='customer-{}'.format(i),
        password=md5_encrypt('crccrc'),
        phone='1' + str(randint(1000000000, 9999999999)),
        email=str(randint(1000000, 9999999)) + '@' + ['qq.com', '163.com', 'gmail.com', '126.com'][randint(0, 3)],
        balance=5 * randint(20, 100),
        prior_id=randint(1, prior_count),
        creator_id=1,
    )
