from __future__ import unicode_literals

from collections import OrderedDict

from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.options import TO_FIELD_VAR
from django.contrib.admin.templatetags.admin_modify import \
    submit_row as original_submit_row
from django.contrib.admin.templatetags.admin_modify import register
from django.contrib.admin.utils import flatten, unquote
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth import get_permission_codename
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import NoReverseMatch, reverse
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.utils.translation import ugettext as _

from .utils import get_model_name


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    """submit buttons context change"""
    ctx = original_submit_row(context)
    ctx.update({
        'show_save_as_new': context.get(
            'show_save_as_new', ctx['show_save_as_new']),
        'show_save_and_add_another': context.get(
            'show_save_and_add_another', ctx['show_save_and_add_another']),
        'show_save_and_continue': context.get(
            'show_save_and_continue', ctx['show_save_and_continue']),
        'show_save': context.get(
            'show_save', ctx['show_save']),
    })
    return ctx


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

    def get_excluded_fields(self):
        """
        Check if we have no excluded fields defined as we never want to
        show those (to any user)
        """
        if self.exclude is None:
            exclude = []
        else:
            exclude = list(self.exclude)

        # logic taken from: django.contrib.admin.options.ModelAdmin#get_form
        if self.exclude is None and hasattr(
                self.form, '_meta') and self.form._meta.exclude:
            # Take the custom ModelForm's Meta.exclude into account only
            # if the ModelAdmin doesn't define its own.
            exclude.extend(self.form._meta.exclude)

        return exclude

    def get_fields(self, request, obj=None):
        """
        If the user has only the view permission return these readonly fields
        which are in fields attr
        """
        if ((self.has_view_permission(request, obj) and (
            obj and not self.has_change_permission(request, obj, True))) or (
                obj is None and not self.has_add_permission(request))):
            fields = super(
                AdminViewPermissionBaseModelAdmin,
                self).get_fields(request, obj)
            excluded_fields = self.get_excluded_fields()
            readonly_fields = self.get_readonly_fields(request, obj)
            new_fields = [i for i in flatten(fields) if
                          i in readonly_fields and
                          i not in excluded_fields]

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

        if ((self.has_view_permission(request, obj) and (
            obj and not self.has_change_permission(request, obj, True))) or (
                obj is None and not self.has_add_permission(request))):
            readonly_fields = (
                list(readonly_fields) +
                [field.name for field in self.opts.fields
                 if field.editable] +
                [field.name for field in self.opts.many_to_many
                 if field.editable]
            )

            # Try to remove id if user has not specified fields and
            # readonly fields
            try:
                readonly_fields.remove('id')
            except ValueError:
                pass

            if self.fields:
                # Set as readonly fields the specified fields
                readonly_fields = flatten(self.fields)

            # Remove from the readonly_fields list the excluded fields
            # specified on the form or the modeladmin
            excluded_fields = self.get_excluded_fields()
            if excluded_fields:
                readonly_fields = [
                    f for f in readonly_fields if f not in excluded_fields
                ]

        return tuple(readonly_fields)

    def get_actions(self, request):
        """
        Override this funciton to remove the actions from the changelist view
        """
        actions = super(AdminViewPermissionBaseModelAdmin, self).get_actions(
            request)

        if self.has_view_permission(request) and \
                not self.has_change_permission(request, only_change=True):
            # If the user doesn't have delete permission return an empty
            # OrderDict otherwise return only the default admin_site actions
            if not self.has_delete_permission(request):
                return OrderedDict()
            else:
                return OrderedDict(
                    (name, (func, name, desc))
                    for func, name, desc in actions.values()
                    if name in dict(self.admin_site.actions).keys()
                )

        return actions


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


class AdminViewPermissionModelAdmin(AdminViewPermissionBaseModelAdmin,
                                    admin.ModelAdmin):
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
        to_field = request.POST.get(
            TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR)
        )
        model = self.model
        opts = model._meta

        # TODO: Overriding the change_view costs 1 query more (one from us
        # and another from the super)
        obj = self.get_object(request, unquote(object_id), to_field)

        if self.has_view_permission(request, obj) and \
                not self.has_change_permission(request, obj, True):
            extra_context = extra_context or {}
            extra_context['title'] = _('View %s') % force_text(
                opts.verbose_name)

            extra_context['show_save'] = False
            extra_context['show_save_and_continue'] = False
            extra_context['show_save_and_add_another'] = False
            extra_context['show_save_as_new'] = False

            inlines = self.get_inline_instances(request, obj)
            for inline in inlines:
                if (inline.has_change_permission(request, obj, True) or
                        inline.has_add_permission(request)):
                    extra_context['show_save'] = True
                    extra_context['show_save_and_continue'] = True
                    break

        return super(AdminViewPermissionModelAdmin, self).change_view(
            request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        resp = super(AdminViewPermissionModelAdmin, self).changelist_view(
            request, extra_context)
        if self.has_view_permission(request) and \
                not self.has_change_permission(request, only_change=True):
            resp.context_data['cl'].formset = None

        return resp


class AdminViewPermissionAdminSite(admin.AdminSite):
    def register(self, model_or_iterable, admin_class=None, **options):
        """
        Create a new ModelAdmin class which inherits from the original and
        the above and register all models with that
        """
        SETTINGS_MODELS = getattr(settings, 'ADMIN_VIEW_PERMISSION_MODELS',
                                  None)

        models = model_or_iterable
        if not isinstance(model_or_iterable, (tuple, list)):
            models = tuple([model_or_iterable])

        if SETTINGS_MODELS or (SETTINGS_MODELS is not None and len(
                SETTINGS_MODELS) == 0):
            for model in models:
                model_name = get_model_name(model)
                if model_name in SETTINGS_MODELS:
                    if admin_class:
                        admin_class = type(
                            str('DynamicAdminViewPermissionModelAdmin'),
                            (admin_class, AdminViewPermissionModelAdmin),
                            dict(admin_class.__dict__))
                    else:
                        admin_class = AdminViewPermissionModelAdmin

                super(AdminViewPermissionAdminSite, self).register([model],
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
