from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Group
from django.contrib.auth.models import User
from .apps import NotificationConfig

from django.apps import apps

#sender in post_migrate signal is current appconfig so get a current app (or can write it in apps file and pass self from ready func to it -without receiver decorator-) 
@receiver(post_migrate , sender=apps.get_app_config(NotificationConfig.name))
def create_default_groups(sender , **kwargs):
    Group.objects.get_or_create(name='all')
    Group.objects.get_or_create(name='admin')
    print("DEFAULT GROUP`s CREATED")