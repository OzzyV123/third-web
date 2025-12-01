from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *

from .forms import PostForm
from .models import Post
from .filters import *


class PostList(ListView):
    model = Post
    ordering = 'name'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "NW"
        return super().form_valid(form)

class ArticleCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "AR"
        return super().form_valid(form)

class NewsUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "NW"
        return super().form_valid(form)

class ArticleUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "AR"
        return super().form_valid(form)

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')