from __future__ import unicode_literals

from django.apps import apps
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.utils.text import capfirst
from django.utils.encoding import force_text
from django.contrib.auth import get_permission_codename
from django.contrib.admin.utils import unquote, quote
from django.core.urlresolvers import NoReverseMatch, reverse
from django.core.exceptions import PermissionDenied
from django.contrib.admin.views.main import ChangeList
from django.utils.translation import ugettext as _

from .utils import django_version
from .enums import DjangoVersion


class AdminViewPermissionChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        super(AdminViewPermissionChangeList, self).__init__(*args, **kwargs)
        # TODO: Exam if is None
        self.request = args[0]

        # If user has only view permission change the title of the changelist
        # view
        if self.model_admin.has_view_permission(self.request) and \
                not self.model_admin.has_change_permission(self.request,
                                                           only_change=True):
            if self.is_popup:
                title = _('Select %s')
            else:
                title = _('Select %s to view')
            self.title = title % force_text(self.opts.verbose_name)


class AdminViewPermissionBaseModelAdmin(admin.options.BaseModelAdmin):
    def get_model_perms(self, request):
        """
        Returns a dict of all perms for this model. This dict has the keys
        ``add``, ``change``, ``delete`` and ``view`` mapping to the True/False
        for each of those actions.
        """
        return {
            'add': self.has_add_permission(request),
            'change': self.has_change_permission(request),
            'delete': self.has_delete_permission(request),
            'view': self.has_view_permission(request)
        }

    def has_view_permission(self, request, obj=None):
        """
        Returns True if the given request has permission to view an object.
        Can be overridden by the user in subclasses.
        """
        opts = self.opts
        codename = get_permission_codename('view', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def has_change_permission(self, request, obj=None, only_change=False):
        """
        Override this method in order to return True whenever a user has view
        permission and avoid re-implementing the change_view and
        changelist_view views. Also, added an extra argument to determine
        whenever this function will return the original response
        """
        change_permission = super(AdminViewPermissionBaseModelAdmin,
                                  self).has_change_permission(request, obj)
        if only_change:
            return change_permission
        else:
            if change_permission or self.has_view_permission(request, obj):
                return True
            else:
                return change_permission

    def get_fields(self, request, obj=None):
        """
        If the user has only the view permission return these readonly fields
        which are in fields attr
        """
        if self.has_view_permission(request, obj) and \
                not self.has_change_permission(request, obj, True):
            fields = super(AdminViewPermissionBaseModelAdmin, self).get_fields(
                request, obj)
            readonly_fields = self.get_readonly_fields(request, obj)
            new_fields = [i for i in fields if i in readonly_fields]
            return new_fields
        else:
            return super(AdminViewPermissionBaseModelAdmin, self).get_fields(
                request, obj)

    def get_readonly_fields(self, request, obj=None):
        """
        Return all fields as readonly for the view permission
        """
        # get read_only fields specified on the admin class is available
        # (needed for @property fields)
        readonly_fields = super(AdminViewPermissionBaseModelAdmin,
                                self).get_readonly_fields(request, obj)

        if self.has_view_permission(request, obj) and \
                not self.has_change_permission(request, obj, True):

            readonly_fields = list(readonly_fields) + \
                [ field.name for field in self.opts.local_fields if field.editable ] + \
                [ field.name for field in self.opts.local_many_to_many if field.editable ]

            # Try to remove id if user have not specify fields and
            # readonly fields
            try:
                readonly_fields.remove('id')
            except ValueError:
                pass

            if self.fields:
                # Set as readonly fields the specified fields
                readonly_fields = self.fields

        return tuple(readonly_fields)

    def get_actions(self, request):
        """
        Override this funciton to remove the actions from the changelist view
        """
        if self.has_view_permission(request) and \
                not self.has_change_permission(request, only_change=True):
            return None
        else:
            return super(AdminViewPermissionBaseModelAdmin, self).get_actions(
                request)


class AdminViewPermissionInlineModelAdmin(AdminViewPermissionBaseModelAdmin,
                                          admin.options.InlineModelAdmin):
    def get_queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        if self.has_view_permission(request) and \
                not self.has_change_permission(request, None, True):
            return super(AdminViewPermissionInlineModelAdmin, self)\
                .get_queryset(request)
        else:
            # TODO: Somehow super executes admin.options.InlineModelAdmin
            # get_queryset and AdminViewPermissionBaseModelAdmin which is
            # convinient
            return super(AdminViewPermissionInlineModelAdmin, self)\
                .get_queryset(request)

    '''def has_parent_view_permission(self, request, obj=None):
        if getattr(self.parent_model, 'assigned_modeladmin', None):
            parent_modeladmin = self.parent_model.assigned_modeladmin
            return parent_modeladmin.has_view_permission(request, obj) \
                   and not parent_modeladmin.has_change_permission(request,
                                                                   obj, True)

        return False'''


class AdminViewPermissionModelAdmin(AdminViewPermissionBaseModelAdmin, admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super(AdminViewPermissionModelAdmin, self).__init__(model, admin_site)
        # Contibute this class to the model
        setattr(self.model, 'assigned_modeladmin', self)

    def get_changelist(self, request, **kwargs):
        """
        Returns the ChangeList class for use on the changelist page.
        """
        return AdminViewPermissionChangeList

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        for inline_class in self.inlines:
            new_class = type(
                str('DynamicAdminViewPermissionInlineModelAdmin'),
                (inline_class, AdminViewPermissionInlineModelAdmin),
                dict(inline_class.__dict__))

            inline = new_class(self.model, self.admin_site)
            if request:
                if not (inline.has_view_permission(request, obj) or
                        inline.has_add_permission(request) or
                        inline.has_change_permission(request, obj, True) or
                        inline.has_delete_permission(request, obj)):
                    continue
                if inline.has_view_permission(request, obj) and \
                        not inline.has_change_permission(request, obj, True):
                    inline.can_delete = False
                if not inline.has_add_permission(request):
                    inline.max_num = 0
            inline_instances.append(inline)

        return inline_instances

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Override this function to hide the sumbit row from the user who has
        view only permission
        """
        model = self.model
        opts = model._meta

        if object_id:
            obj = None
        else:
            obj = self.get_object(request, unquote(object_id))

        if self.has_view_permission(request, obj) and \
                not self.has_change_permission(request, obj, True):
            extra_context = extra_context or {}
            extra_context['title'] = _('View %s') % force_text(
                opts.verbose_name)

            extra_context['show_save'] = False
            extra_context['show_save_and_continue'] = False

            inlines = self.get_inline_instances(request, obj)
            for inline in inlines:
                if inline.has_change_permission(request, obj, True):
                    extra_context['show_save'] = True
                    extra_context['show_save_and_continue'] = True
                    break

        return super(AdminViewPermissionModelAdmin, self).change_view(request,
                                                                      object_id,
                                                                      form_url,
                                                                      extra_context)


class AdminViewPermissionAdminSite(admin.AdminSite):
    def register(self, model_or_iterable, admin_class=None, **options):
        """
        Create a new ModelAdmin class which inherits from the original and the above and register
        all models with that
        """
        SETTINGS_MODELS = getattr(settings, 'ADMIN_VIEW_PERMISSION_MODELS', None)

        models = model_or_iterable
        if not isinstance(model_or_iterable, tuple):
            models = tuple([model_or_iterable])

        if SETTINGS_MODELS or (SETTINGS_MODELS is not None and len(
                SETTINGS_MODELS) == 0):
            for model in models:
                if django_version() == DjangoVersion.DJANGO_18:
                    model_name = '%s.%s' %(model._meta.app_label,
                                           model._meta.object_name)
                elif django_version() > DjangoVersion.DJANGO_18:
                    model_name = model._meta.label

                if model_name in SETTINGS_MODELS:
                    if admin_class:
                        admin_class = type(
                            str('DynamicAdminViewPermissionModelAdmin'),
                            (admin_class, AdminViewPermissionModelAdmin),
                            dict(admin_class.__dict__))
                    else:
                        admin_class = AdminViewPermissionModelAdmin

                super(AdminViewPermissionAdminSite, self).register(model,
                                                                   admin_class,
                                                                   **options)
        else:
            if admin_class:
                admin_class = type(str('DynamicAdminViewPermissionModelAdmin'),
                                   (
                                       admin_class,
                                       AdminViewPermissionModelAdmin),
                                   dict(admin_class.__dict__))
            else:
                admin_class = AdminViewPermissionModelAdmin

            super(AdminViewPermissionAdminSite, self).register(
                model_or_iterable,
                admin_class, **options)

    def _build_app_dict(self, request, label=None):
        """
        Builds the app dictionary. Takes an optional label parameters to filter
        models of a specific app.
        """
        app_dict = {}

        if label:
            models = {
                m: m_a for m, m_a in self._registry.items()
                if m._meta.app_label == label
                }
        else:
            models = self._registry

        for model, model_admin in models.items():
            app_label = model._meta.app_label

            has_module_perms = model_admin.has_module_permission(request)
            if not has_module_perms:
                if label:
                    raise PermissionDenied
                continue

            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True not in perms.values():
                continue

            info = (app_label, model._meta.model_name)
            model_dict = {
                'name': capfirst(model._meta.verbose_name_plural),
                'object_name': model._meta.object_name,
                'perms': perms,
            }
            if perms.get('change') or perms.get('view'):
                try:
                    model_dict['admin_url'] = reverse(
                        'admin:%s_%s_changelist' % info, current_app=self.name)
                except NoReverseMatch:
                    pass
            if perms.get('add'):
                try:
                    model_dict['add_url'] = reverse('admin:%s_%s_add' % info,
                                                    current_app=self.name)
                except NoReverseMatch:
                    pass

            if app_label in app_dict:
                app_dict[app_label]['models'].append(model_dict)
            else:
                app_dict[app_label] = {
                    'name': apps.get_app_config(app_label).verbose_name,
                    'app_label': app_label,
                    'app_url': reverse(
                        'admin:app_list',
                        kwargs={'app_label': app_label},
                        current_app=self.name,
                    ),
                    'has_module_perms': has_module_perms,
                    'models': [model_dict],
                }

        if label:
            return app_dict.get(label)

        return app_dict
