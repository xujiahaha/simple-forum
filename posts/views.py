from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Count
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from taggit.models import Tag

from posts.forms import PostForm
from posts.models import Post, Category, Reply, Announcement


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    if not request.user.is_authenticated():
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form
    }
    return render(request, 'post_create_form.html', context)


def post_list(request, tag_slug=None, category_slug=None):
    if request.user.is_authenticated():
        queryset_list = Post.objects.annotate(reply_count=Count('replies')).order_by('-reply_count')
    else:
        queryset_list = Post.objects.filter(public=True)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        queryset_list = queryset_list.filter(tags__in=[tag])
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        queryset_list = queryset_list.filter(category=category)
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(Q(title__icontains=query)|
                                             Q(content__icontains=query)).distinct()
    paginator = Paginator(queryset_list, 25)  # Show 25 posts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    all_tags = Tag.objects.all()
    all_categories = Category.objects.all()
    context = {
        "posts": queryset,
        "page_request_var": page_request_var,
        'tag': tag,
        'tags': all_tags,
        'categories': all_categories,
    }
    return render(request, "post_list.html", context)


def get_posts_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category)
    if request.is_ajax():
        html = render_to_string('post_list_content.html', {'posts': posts})
        return HttpResponse(html)


def post_detail(request, slug=None):  # Retrieve
    if request.is_ajax():
        reply_create(request)
    post = get_object_or_404(Post, slug=slug)
    replies = post.replies.all()
    context = {
        "post": post,
        "replies": replies,
        'tags': Tag.objects.all(),
    }
    return render(request, 'post_detail.html', context)


def reply_create(request):
    post_id = request.POST.get('post_id')
    reply_content = request.POST.get('reply_content')
    author_id = request.POST.get('author_id')
    post = Post.objects.get(pk=post_id)
    author = AUTH_USER_MODEL.objects.get(pk=author_id)
    reply = Reply(post=post)
    reply.author = author
    reply.content = reply_content
    reply.save()
    return HttpResponse('success')


def announcement_list(request):
    if request.user.is_authenticated():
        announcements = Announcement.objects.all()
    context = {
        "announcements": announcements,
    }
    return render(request, "announcement_list.html", context)