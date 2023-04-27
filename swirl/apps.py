from django.apps import AppConfig

from swirl.utils import create_group_if_not_exists

AUTO_PRIVISIONED_GROUP_NAME= 'swirl_auto_provisioned_group'
class SwirlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'swirl'

    def ready(self):
        # Replace 'your_group_name' with the desired group name
        auto_provision_permissions = [
            'add_search',
            'change_search',
            'view_search',
            'add_result',
            'change_result',
            'view_result',
            'add_querytransform',
            'change_querytransform',
            'view_querytransform',
            'view_searchprovider'
        ]
        create_group_if_not_exists(AUTO_PRIVISIONED_GROUP_NAME,
            permissions=auto_provision_permissions)
