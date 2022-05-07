from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from online_shop.auth_app.forms import UserRegistrationForm, EditUserForm, DeleteUserForm
from django.views import generic as views
from online_shop.auth_app.models import AppUser


class UserRegistrationView(views.CreateView):

    form_class = UserRegistrationForm  # This is my custom form
    template_name = 'auth/register.html'
    success_url = reverse_lazy('home page')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home page')
        self.object = None
        return super().get(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        """
        Return a response, using the `response_class` for this view, with a
        template rendered with the given context.

        Pass response_kwargs to the constructor of the response class.
        """
        response_kwargs.setdefault("content_type", self.content_type)

        for _, field in context['form'].fields.items():
            if _ == 'email':
                field.widget.attrs['placeholder'] = 'Your email here'
            elif _ == 'password1':
                field.widget.attrs['placeholder'] = 'Your password here'
            elif _ == 'password2':
                field.widget.attrs['placeholder'] = 'Repeat your password'
            elif _ == 'first_name':
                field.widget.attrs['placeholder'] = 'Your first name here'

        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)

        login(self.request, self.object)
        return result


class UserLoginView(auth_views.LoginView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        if request.user.is_authenticated:
            return redirect('home page')
        return self.render_to_response(self.get_context_data())

    def render_to_response(self, context, **response_kwargs):
        """
        Return a response, using the `response_class` for this view, with a
        template rendered with the given context.

        Pass response_kwargs to the constructor of the response class.
        """
        response_kwargs.setdefault("content_type", self.content_type)

        for _, field in context['form'].fields.items():
            if _ == 'username':
                field.widget.attrs['placeholder'] = 'Your email here'
            elif _ == 'password':
                field.widget.attrs['placeholder'] = 'Your password here'

        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )

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
