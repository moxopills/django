from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from blog.models import Blog

class BlogListView(ListView):
    queryset = Blog.objects.all()
    template_name = 'blog_list.html'
    paginate_by = 8
    ordering = ['-created_at',]

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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id_lte=25)

    def get_object(self, queryset=None):
        object = super().get_object()
        object = self.model.objects.get(pk=self.kwargs.get('pk'))

        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = 'CBV'

        return context

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog_create.html'
    fields = ('title','content')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return  reverse_lazy('cb_blog_detail',kwargs={'pk':self.object.pk})

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog_update.html'
    fields = ('title','content')

    def get_queryset(self):
        quertset = super().get_queryset()
        return  quertset.filter(author = self.request.user)

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('blog_list')