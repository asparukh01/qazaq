from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from .forms import ImageForm, FavoriteForm
from .models import Image, Favorite


class ImageListView(ListView):
    template_name = 'image/image_list.html'
    context_object_name = 'images'
    model = Image
    ordering = ('-created_at',)
    paginate_by = 10


class ImageCreateView(LoginRequiredMixin, CreateView):
    template_name = 'image/image_create.html'
    model = Image
    form_class = ImageForm

    def form_valid(self, form):
        image = form.save(commit=False)
        image.author = self.request.user
        image.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('image_list')


class ImageUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'image/image_update.html'
    model = Image
    form_class = ImageForm
    context_object_name = 'image'
    permission_required = 'gallery.change_image'

    def has_permission(self):
        return self.get_object().author == self.request.user or self.request.user.has_perm(self.permission_required)

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('image_detail', pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('image_list')


class ImageDetailView(DetailView):
    template_name = 'image/image_detail.html'
    model = Image
    context_object_name = 'image'
    pk_url_kwarg = 'pk'


class ImageDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'partial/common/image_delete.html'
    model = Image
    context_object_name = 'image'
    success_url = reverse_lazy('image_list')
    pk_url_kwarg = 'pk'
    permission_required = 'gallery.delete_image'

    def has_permission(self):
        return self.get_object().author == self.request.user or self.request.user.has_perm(self.permission_required)

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('image_detail', pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)


class FavoriteAddView(CreateView):
    model = Favorite
    form_class = FavoriteForm
    template_name = 'image/image_list.html'

    def form_valid(self, form):
        form.instance.image = get_object_or_404(Image, pk=self.kwargs.get('pk'))
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('image_list')