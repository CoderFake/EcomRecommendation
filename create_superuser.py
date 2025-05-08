import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartparking.settings")
django.setup()

import logging

logger = logging.getLogger(__name__)

from accounts.models import Account

username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin")

try:
    user = User.objects.get(email=email)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()

    logger.info(f"Admin account '{username}' already exists. Password has been updated.")
except User.DoesNotExist:
    User.objects.create_superuser(username=username, email=email, password=password)
    logger.info(f"Admin account '{username}' created successfully!")


from django.contrib.sites.models import Site


site_id = int(os.getenv("SITE_ID", 1))
domain = os.getenv("SITE_DOMAIN", "localhost:8000")
site_name = os.getenv("SITE_NAME", "ecommerce")

try:
    site = Site.objects.get(id=site_id)
    site.domain = domain
    site.name = site_name
    site.save()
    logger.info(f"Site ID {site_id} updated with domain '{domain}' and name '{site_name}'!")
except Site.DoesNotExist:
    Site.objects.create(
        id=site_id,
        domain=domain,
        name=site_name
    )
    logger.info(f"Site ID {site_id} created with domain '{domain}' and name '{site_name}'!")
