from django.contrib import admin

# Register your models here.
from posts.models import Post, Comment, Reply, Category, Announcement


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "updated_on", "created_on"]
    list_display_links = ["title"]
    list_filter = ["updated_on", "created_on"]
    search_fields = ["title", "content"]

    class Meta:
        model = Post

    class Media:
        js = (
            'tinymce/js/tinymce/tinymce.min.js',  # tinymce js file
            'js/tinymce_config.js',  # project static folder
        )

class ReplyModelAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "created_on"]
    search_fields = ["post"]

    class Meta:
        model = Reply

    class Media:
        js = (
            'tinymce/js/tinymce/tinymce.min.js',  # tinymce js file
            'js/tinymce_config.js',  # project static folder
        )


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["reply", "author", "created_on"]

    class Meta:
        model = Comment

    class Media:
        js = (
            'tinymce/js/tinymce/tinymce.min.js',  # tinymce js file
            'js/tinymce_config.js',  # project static folder
        )


class AnnouncementModelAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_on"]
    search_fields = ["title"]

    class Meta:
        model = Announcement

    class Media:
        js = (
            'tinymce/js/tinymce/tinymce.min.js',  # tinymce js file
            'js/tinymce_config.js',  # project static folder
        )


admin.site.register(Post, PostModelAdmin)
admin.site.register(Reply, ReplyModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
admin.site.register(Category)
admin.site.register(Announcement, AnnouncementModelAdmin)