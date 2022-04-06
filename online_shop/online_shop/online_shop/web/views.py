from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views import generic as views

# Create your views here.
from online_shop.web.forms import EditProfileForm
from online_shop.web.models import Profile, Product


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
