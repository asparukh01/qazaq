from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.base import View

from .forms import UserCreationForm, UserUpdateForm, ProfileUpdateForm, PasswordChangeForm
from gallery.models import Favorite

from gallery.models import Image


class LoginView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'accounts/login.html', {'next': request.GET.get('next')})

    def post(self, request, *args, **kwargs):
        context = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            next = request.GET.get('next')
            login(request, user)
            if next:
                return redirect(next)
            return redirect('image_list')
        context['has_error'] = True
        return render(request, 'accounts/login.html', context)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('image_list')


class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/profile.html'
    context_object_name = 'user_obj'
    paginate_by = 5
    paginate_orphans = 0

    def get_context_data(self, **kwargs):
        images = self.object.images.order_by('-created_at')
        paginator = Paginator(images, self.paginate_by, self.paginate_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['projects'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)



class ProfileUpdateView(UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'accounts/profile_update.html'

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def get_object(self):
        return self.model.objects.get(id=self.request.user.id)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileUpdateForm(**form_kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super(ProfileUpdateView, self).form_valid(form)
        profile_form.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(
            form=form, profile_form=profile_form
        )
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})


class ChangePasswordView(UpdateView):
    model = get_user_model()
    template_name = 'accounts/user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return redirect(self.get_success_url())

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})




