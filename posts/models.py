from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from hitcount.models import HitCountMixin, HitCount
from markdown_deux import markdown
from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItem

from posts.utils import generate_unique_slug


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Post(models.Model, HitCountMixin):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="post_by")
    anonymous = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=255)
    category = models.ForeignKey(Category, related_name="posts")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_on = models.DateTimeField(auto_now_add=False, auto_now=True)
    follower = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="follows")
    solved = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count')

    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    def get_num_follow(self):
        obj = Post.objects.get(pk=self.pk)
        return obj.follower.count()

    def get_num_reply(self):
        return self.replies.all().count()

    def get_num_view(self):
        obj = HitCount.objects.get(object_pk=self.pk)
        if obj is not None:
            return obj.hits
        else:
            return 0

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def as_json(self):
        tag_items = TaggedItem.objects.filter(object_id=self.pk)
        tags = []
        for item in tag_items:
            tag = Tag.objects.get(pk=item.tag_id)
            tags.append(tag.name)
        return dict(
            title=self.title, num_view=self.get_num_view(),
            num_follow=self.get_num_follow(),
            num_reply=self.get_num_reply(),
            tags=tags)

    class Meta:
        ordering = ["-created_on", "-updated_on"]


class Reply(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="reply_by")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_on = models.DateTimeField(auto_now_add=False, auto_now=True)
    post = models.ForeignKey(Post, blank=True, null=True, related_name="replies")
    up_vote = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.content

    def get_comments(self):
        return self.comments.all()

    class Meta:
        ordering = ["-up_vote"]


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="comment_by")
    reply = models.ForeignKey(Reply, null=True, blank=True, related_name="comments")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.content


class Announcement(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-created_on"]


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_unique_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)
