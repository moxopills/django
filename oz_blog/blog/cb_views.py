from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog, Comment
from blog.form import CommentForm


class BlogListView(ListView):
    model = Blog
    template_name = 'blog_list.html'
    paginate_by = 8
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )
        return queryset


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    pk_url_kwarg = 'blog_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['blog'] = self.object
        return context


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog_form.html'
    fields = ('category', 'title', 'content')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '작성'
        context['btn_name'] = '생성'
        return context


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog_form.html'
    fields = ('category', 'title', 'content')

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '수정'
        context['btn_name'] = '수정'
        return context


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('blog:list')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get(self, *args, **kwargs):
        raise Http404

    def form_valid(self, form):
        blog = self.get_blog()
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.blog = blog
        self.object.save()
        return HttpResponseRedirect(reverse('blog:detail', kwargs={'blog_pk': blog.pk}))

    def get_blog(self):
        pk = self.kwargs['blog_pk']
        return get_object_or_404(Blog, pk=pk)
