from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse


#
# class BootstrapFormMixin:
#     pass
#     fields = {}
#
#     def _init_bootstrap_form_controls(self):
#         for _, field in self.fields.items():
#             if not hasattr(field.widget, 'attrs'):
#                 setattr(field.widget, 'attrs', {})
#             if 'class' not in field.widget.attrs:
#                 field.widget.attrs['class'] = ''
#             field.widget.attrs['class'] += ' form-control'


# class CustomNoPermissionMixin:
#     def dispatch(request, *args, **kwargs):
#         if request.user.pk != kwargs['pk']:
#             return redirect('home page')
#
#         response = super().dispatch(request, *args, **kwargs)
#
#         return response
#
