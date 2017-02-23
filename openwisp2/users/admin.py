from allauth.account.models import EmailAddress
from django import forms
from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.utils.translation import ugettext_lazy as _
from organizations.base_admin import (BaseOrganizationAdmin,
                                      BaseOrganizationOwnerAdmin,
                                      BaseOrganizationUserAdmin,
                                      BaseOwnerInline)

from .models import (Group, Organization, OrganizationOwner, OrganizationUser,
                     User)


class EmailAddressInline(admin.StackedInline):
    model = EmailAddress
    extra = 0
    readonly_fields = ['email']

    def has_add_permission(self, *args, **kwargs):
        """
        Do not let admins add new email objects via inlines
        in order to not mess the coherence of the database.
        Admins can still change the main email field of the User model,
        that will automatically add a new email address object and
        send a confirmation email, see ``UserAdmin.save_model``
        """
        return False


class OrganizationUserInline(admin.StackedInline):
    model = OrganizationUser
    extra = 0


class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(label=_('Email'), max_length=254, required=True)


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    readonly_fields = ['last_login', 'date_joined']
    list_display = ('username', 'email', 'is_superuser', 'date_joined', 'last_login')
    inlines = [EmailAddressInline, OrganizationUserInline]
    save_on_top = True

    def get_inline_instances(self, request, obj=None):
        """
        Avoid displaying inline objects when adding a new user
        """
        if obj:
            return super(UserAdmin, self).get_inline_instances(request, obj)
        return []

    def save_model(self, request, obj, form, change):
        """
        Automatically creates email addresses for users
        added/changed via the django-admin interface
        """
        super(UserAdmin, self).save_model(request, obj, form, change)
        if obj.email:
            EmailAddress.objects.add_email(request,
                                           user=obj,
                                           email=obj.email,
                                           confirm=True,
                                           signup=True)


base_fields = list(UserAdmin.fieldsets[1][1]['fields'])
additional_fields = ['bio', 'url', 'company', 'location']
UserAdmin.fieldsets[1][1]['fields'] = base_fields + additional_fields
UserAdmin.add_fieldsets[0][1]['fields'] = ('username', 'email', 'password1', 'password2')


class OwnerInline(BaseOwnerInline):
    model = OrganizationOwner


class OrganizationAdmin(BaseOrganizationAdmin):
    inlines = [OwnerInline]


class OrganizationUserAdmin(BaseOrganizationUserAdmin):
    pass


class OrganizationOwnerAdmin(BaseOrganizationOwnerAdmin):
    list_display = ('get_user', 'organization')

    def get_user(self, obj):
        return obj.organization_user.user


admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationUser, OrganizationUserAdmin)
admin.site.register(OrganizationOwner, OrganizationOwnerAdmin)
# unregister auth.Group
base_group_model = apps.get_model('auth', 'Group')
admin.site.unregister(base_group_model)
# register openwisp2.users.Group (proxy model)
admin.site.register(Group, GroupAdmin)

# unregister allauth admin to keep the admin interface simple
# we can re-enable these models later when they will be really needed
for model in [('sites', 'Site'),
              ('account', 'EmailAddress'),
              ('socialaccount', 'SocialApp'),
              ('socialaccount', 'SocialToken'),
              ('socialaccount', 'SocialAccount')]:
    admin.site.unregister(apps.get_model(*model))