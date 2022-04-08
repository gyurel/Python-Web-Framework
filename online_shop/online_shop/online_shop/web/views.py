from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import generic as views

# Create your views here.
from online_shop.web.forms import EditProfileForm
from online_shop.web.models import Profile, Product, Cart


class IndexView(LoginRequiredMixin, views.ListView):
    model = Product
    template_name = 'index.html'
    # queryset = 'products_list'
    context_object_name = 'products_list'


class ProfileDetails(views.DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile-details.html'

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = super().get_context_data(**kwargs)
        if self.object:
            context["profile"] = self.object
            if self.context_object_name:
                context[self.context_object_name] = self.object
        context.update(kwargs)
        return context


class EditProfile(views.UpdateView):
    model = Profile
    template_name = 'profile-edit.html'
    form_class = EditProfileForm
    # success_url = reverse_lazy('home page')

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.pk})


def add_to_card_view(request, pk):
    product = Product.objects.get(pk=pk)
    user = get_user(request)
    cart = Cart
    # cart.product = product.pk
    # cart.user = user.pk
    cart.objects.create(product=product, user=user)

    return redirect('home page')


class CartView(views.ListView):
    model = Cart
    template_name = 'cart.html'
    # queryset = 'products_list'
    context_object_name = 'cart'

#     def get(self, request, *args, **kwargs):
#         self.object_list = self.get_queryset()
#         allow_empty = self.get_allow_empty()
#
#         if not allow_empty:
#             # When pagination is enabled and object_list is a queryset,
#             # it's better to do a cheap query than to load the unpaginated
#             # queryset in memory.
#             if self.get_paginate_by(self.object_list) is not None and hasattr(
#                 self.object_list, "exists"
#             ):
#                 is_empty = not self.object_list.exists()
#             else:
#                 is_empty = not self.object_list
#             if is_empty:
#                 raise Http404(
#                     _("Empty list and “%(class_name)s.allow_empty” is False.")
#                     % {
#                         "class_name": self.__class__.__name__,
#                     }
#                 )
#         context = self.get_context_data()
#         result = set()
# ,
# 87for obj in context.cart:
#             if obj.user_id == request.user.id:
#                 result += obj
#         context = result
#         return self.render_to_response(context)
