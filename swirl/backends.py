from django.contrib.auth.backends import ModelBackend
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth.models import User, Group

import logging as logger

logger.basicConfig(level=logger.INFO)

AUTO_PRIVISIONED_GROUP_NAME = 'swirl_auto_provisioned_group'

def generate_username(email):
    """
    simplest thing that can work
    """
    return email

def add_user_to_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        logger.info(f'User "{user}" has been added to group "{group_name}".')
    except User.DoesNotExist:
       logger.error(f'User "{user}" not found.')
    except Group.DoesNotExist:
        logger.error(f'Group "{group_name}" not found.')

class CustomModelOIDCBackend(OIDCAuthenticationBackend):
    def authenticate(self, request, **kwargs):
        # First, try OIDC authentication
        user = OIDCAuthenticationBackend.authenticate(self, request, **kwargs)
        if user is not None:
            return user

        # If OIDC authentication fails, fall back to Django's authentication
        return ModelBackend.authenticate(self, request, **kwargs)

    def create_user(self, claims):
        user = super().create_user(claims)
        user.is_staff = False # You can modify this according to your requirements
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        add_user_to_group(user, AUTO_PRIVISIONED_GROUP_NAME)
        user.save()
        return user

    def update_user(self, user, claims):
        user = super().update_user(user, claims)
        user.is_staff = False # You can modify this according to your requirements
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        add_user_to_group(user, AUTO_PRIVISIONED_GROUP_NAME)
        user.save()
        return user
