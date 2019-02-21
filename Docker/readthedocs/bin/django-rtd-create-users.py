import os
import readthedocs.settings.container as config
from django.contrib.auth.models import User

print("django-rtd-create-users")
try:
    user = User.objects.create_superuser(
        config.ADMIN_USERNAME,
        config.ADMIN_EMAIL,
        config.ADMIN_PASSWORD
    )
    user.save()
    print("Created {0} superuser password {1} email {2}".format(config.ADMIN_USERNAME,config.ADMIN_PASSWORD,config.ADMIN_EMAIL))
except Exception as e:
    print("exception {0}".format(e))
    print("Failed to create {0} user".format(config.ADMIN_USERNAME))

try:
    slumber = User.objects.create(
        username=config.SLUMBER_USERNAME,
        email=config.SLUMBER_EMAIL,
        is_staff=True,
        is_active=True
    )

    slumber.set_password(config.SLUMBER_PASSWORD)

    slumber.save()

    print("Created {0} user".format(config.SLUMBER_USERNAME))
except Exception as e:
    print("exception {0}".format(e))
    print("Failed to create {0} user".format(config.SLUMBER_USERNAME))
