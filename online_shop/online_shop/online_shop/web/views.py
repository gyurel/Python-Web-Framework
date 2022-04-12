from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

# Create your views here.
from online_shop.web.forms import EditProfileForm
from online_shop.web.models import Profile, Product, Cart, Favorites, Storage


class IndexView(LoginRequiredMixin, views.ListView):  # Should be tested!
    paginate_by = 8
    model = Product
    template_name = 'index.html'
    context_object_name = 'products_list'
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['storage'] = Storage.objects.all()  # My custom logic here!
        return context


class ProfileDetailsView(LoginRequiredMixin, views.DetailView):  # Should be tested!
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile-details.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.pk != self.kwargs['pk']:  # My custom logic here!
            return redirect('home page')

        response = super().dispatch(request, *args, **kwargs)

        return response


class EditProfileView(LoginRequiredMixin, views.UpdateView):  # Should be tested!
    model = Profile
    template_name = 'profile-edit.html'
    form_class = EditProfileForm
    # success_url = reverse_lazy('home page')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.pk != self.kwargs['pk']:  # My custom logic here!
            return redirect('home page')

        response = super().dispatch(request, *args, **kwargs)

        return response

    def get_success_url(self):  # My custom logic here!
        return reverse_lazy('profile details', kwargs={'pk': self.object.pk})


class CartView(LoginRequiredMixin, views.ListView):  # Should be tested!
    model = Cart
    template_name = 'cart.html'
    context_object_name = 'cart'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset().filter(user_id=request.user.id).order_by('id')
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404('Empty list')
        context = self.get_context_data()
        return self.render_to_response(context)


def add_to_cart_view(request, pk):

    if not request.user.is_authenticated:
        return redirect('home page')

    current_product = Product.objects.get(pk=pk)
    # products = Product.objects.all()
    user = get_user(request)
    cart = Cart
    articules = Cart.objects.all()
    # cart.product = product.pk
    # cart.user = user.pk

    # for product in products:
    for articul in articules:
        if articul.user_id == user.id:
            if articul.product_id == current_product.id:
                return redirect('home page')

    cart.objects.create(product=current_product, user=user)
    storage_of_articul = Storage.objects.get(pk=current_product.id)
    storage_of_articul.quantity -= 1
    storage_of_articul.save()

    return redirect('home page')


def add_one_to_articul_in_cart_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('home page')

    # form = AddOneToArticul
    articul = Cart.objects.get(pk=pk)
    storage_of_articul = Storage.objects.get(pk=articul.product.id)
    if storage_of_articul.quantity > 0:
        storage_of_articul.quantity -= 1
        articul.quantity += 1
        articul.save()
        storage_of_articul.save()

    return redirect('user cart', pk=pk)


def subtract_one_from_articul_in_cart_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('home page')

    articul = Cart.objects.get(pk=pk)
    storage_of_articul = Storage.objects.get(pk=articul.product.id)

    storage_of_articul.quantity += 1
    articul.quantity -= 1
    articul.save()
    storage_of_articul.save()

    return redirect('user cart', pk=pk)


def delete_cart_articul_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('home page')

    articul = Cart.objects.get(pk=pk)
    storage_of_articul = Storage.objects.get(pk=articul.product.id)

    storage_of_articul.quantity += articul.quantity
    storage_of_articul.save()
    articul.delete()

    return redirect('user cart', pk=pk)


class FavoritesView(LoginRequiredMixin, views.ListView):
    model = Favorites
    template_name = 'favorites.html'
    context_object_name = 'favorites'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset().filter(user_id=request.user.id)
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404('Empty list')
        context = self.get_context_data()
        return self.render_to_response(context)


def add_to_favorites_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('home page')

    current_product = Product.objects.get(pk=pk)
    # products = Product.objects.all()
    user = get_user(request)
    model = Favorites
    favorites = Favorites.objects.all()
    # cart.product = product.pk
    # cart.user = user.pk

    # for product in products:
    for favorit in favorites:
        if favorit.user_id == user.id:
            if favorit.product_id == current_product.id:
                return redirect('home page')

    model.objects.create(product=current_product, user=user)

    return redirect('home page')


def remove_product_from_favorites_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('home page')

    favorit_product = Favorites.objects.get(pk=pk)
    favorit_product.delete()

    return redirect('user favorites', pk=request.user.id)


class CheckOutView(LoginRequiredMixin, views.ListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    model = Cart
    template_name = 'checkout.html'
    context_object_name = 'cart'

    @property
    def cart_subtotal(self):
        subtotal = 0
        for obj in self.object_list:
            subtotal += (obj.product.price * obj.quantity)
        return subtotal

    @property
    def cart_total(self):
        subtotal = self.cart_subtotal
        total = subtotal + 10
        return total

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get the context for this view."""
        queryset = object_list if object_list is not None else self.object_list
        page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_context_object_name(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(
                queryset, page_size
            )
            context = {
                "paginator": paginator,
                "page_obj": page,
                "is_paginated": is_paginated,
                "object_list": queryset,
                "subtotal": self.cart_subtotal,  #Custom inserted form me
                "total": self.cart_total,  #Custom inserted form me

            }
        else:
            context = {
                "paginator": None,
                "page_obj": None,
                "is_paginated": False,
                "object_list": queryset,
                "subtotal": self.cart_subtotal,  #Custom inserted form me
                "total": self.cart_total,  #Custom inserted form me
            }
        if context_object_name is not None:
            context[context_object_name] = queryset
        context.update(kwargs)
        return super().get_context_data(**context)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset().filter(user_id=request.user.id).order_by('id')
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404('Empty list')
        context = self.get_context_data()
        return self.render_to_response(context)


def pay_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('home page')

    user_cart = Cart.objects.all().filter(user_id=pk)

    for article in user_cart:
        article.delete()

    return redirect('user cart', pk=pk)


class AboutView(views.TemplateView):
    template_name = 'about.html'


class ContactView(views.TemplateView):
    template_name = 'contact.html'
