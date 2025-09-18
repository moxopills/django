from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect,reverse
from django.shortcuts import render, get_object_or_404
from blog.models import Blog
from blog.form import BlogForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_http_methods

def blog_list(request):
    blogs = Blog.objects.all().order_by( '-created_at' )
    q = request.GET.get('q')
    if q:
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )

    paginator = Paginator(blogs, 10)

    page = request.GET.get('page')
    page_object = paginator.get_page(page)

    context = {
        'blogs':blogs,
        'page_object': page_object,
     }

    return render(request, 'blog_list.html', context)

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {'blog': blog}
    return render(request, 'blog_detail.html', context)

@login_required()
def blog_create(request):

    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return redirect(reverse('blog_detail', kwargs={'pk':blog.id}))

    context = {'form': form}
    return render(request, 'blog_create.html', context)

@login_required()
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        form.save()
        return redirect(reverse('blog_detail', kwargs= {'pk':blog.pk}))

    context = {'blog':blog,
        'form': form,
               }
    return render(request, 'blog_update.html', context)

@login_required()
@require_http_methods(['POST'])
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog.delete()

    return redirect(reverse('blog_list'))