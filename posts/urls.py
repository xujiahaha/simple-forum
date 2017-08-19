from django.conf.urls import url

from posts.views import post_list, post_detail, get_posts_by_category, post_create, reply_create

urlpatterns = [
    url(r'^$', post_list, name="list"),
    url(r'^create/$', post_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name="detail"),
    url(r'^tag/(?P<tag_slug>[\w-]+)/$', post_list, name='post_list_by_tag'),
    url(r'^category/(?P<category_slug>[\w-]+)/$', get_posts_by_category, name='post_list_by_category'),
    url(r'^reply/$', reply_create, name="reply"),
]