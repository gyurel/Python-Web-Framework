# from django.shortcuts import render
from django.contrib.auth import login, get_user_model
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

# from common.helpers import NotLoggedRequiredMixin
from online_shop.auth_app.forms import UserRegistrationForm, EditUserForm, DeleteUserForm
from django.views import generic as views


# Create your views here.
from online_shop.auth_app.models import AppUser


class UserRegistrationView(views.CreateView):
    # form_class = auth_forms.UserCreationForm #this is the standard django form
    form_class = UserRegistrationForm  # This is my custom form
    template_name = 'auth/register.html'
    success_url = reverse_lazy('home page')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home page')
        self.object = None
        return super().get(request, *args, **kwargs)

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        # user => self.object
        # request => self.request
        login(self.request, self.object)
        return result


class UserLoginView(auth_views.LoginView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        if request.user.is_authenticated:
            return redirect('home page')
        return self.render_to_response(self.get_context_data())

    template_name = 'auth/login.html'

    def get_success_url(self):
        next = self.request.GET.get('next', None)
        if next:
            return next
        return reverse_lazy('home page')


class UserLogoutView(auth_views.LogoutView):
    pass


class EditUserView(auth_views.PasswordChangeView):
    form_class = EditUserForm
    template_name = 'auth/edit-user.html'
    success_url = reverse_lazy('edit user success')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class SuccessfullyEditedUser(auth_views.PasswordChangeDoneView):
    template_name = 'auth/successfully-changed-user.html'

#
# class DeleteUserView(views.DeleteView):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     # def get_queryset(self):
#     #     return super().get_queryset().prefetch_related()
#
#     model = get_user_model()
#     # user = AppUser.objects.get(pk=pk)
#     form_class = DeleteUserForm
#     template_name = 'auth/delete-user.html'
#     success_url = reverse_lazy('home page')


def delete_user_view(request, pk):
    user = AppUser.objects.get(pk=pk)
    if request.method == 'POST':
        form = DeleteUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home page')
    else:
        form = DeleteUserForm(instance=user)

    context = {
        'form': form,
    }

    return render(request, 'auth/delete-user.html', context)
