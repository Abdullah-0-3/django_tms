from django.apps import AppConfig

class RbacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'organization.rbac'
    label = 'organization_rbac'