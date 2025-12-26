from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *

from .forms import PostForm
from .models import *
from .filters import *

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin

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

class NewsCreate(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    permission_required = ('news.add_news',)
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "NW"
        return super().form_valid(form)

class ArticleCreate(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    permission_required = ('news.add_news',)
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "AR"
        return super().form_valid(form)

class NewsUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    permission_required = ('news.add_news',)
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "NW"
        return super().form_valid(form)

class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    permission_required = ('news.add_news',)
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "AR"
        return super().form_valid(form)

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

@login_required
def subscribe_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    obj, created = CategorySub.objects.get_or_create(
        user=request.user,
        category=category
    )
    print("CREATED:", created)
    print("COUNT:", CategorySub.objects.count())
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def unsubscribe_category(request, category_id):
    CategorySub.objects.filter(
        user=request.user,
        category_id=category_id
    ).delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = CategorySub.objects.filter(
            user=request.user,
            category=category
        ).exists()

    return render(request, 'category.html', {
        'category': category,
        'is_subscribed': is_subscribed,
    })
