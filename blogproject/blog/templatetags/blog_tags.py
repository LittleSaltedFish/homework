import os,django

from django.db.models.aggregates import Count
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogproject.settings")# project_name 项目名称django.setup()
django.setup()
from django import template

from blog.models import Post, Category, Tag

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    # 别忘了在顶部引入 Category 类
    return Category.objects.all()


@register.simple_tag
def get_post_by_view():
    return Post.objects.order_by('views')[:5]


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

