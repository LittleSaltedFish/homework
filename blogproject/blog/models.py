import markdown
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
#类别
from django.urls import reverse
from django.utils.html import strip_tags


class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
#标签
class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Post(models.Model):
    #标题
    title = models.CharField(max_length=70)
    #正文
    body = models.TextField()
    #文章创建时间
    created_time = models.DateTimeField()
    #文章最后一次修改时间
    modified_time = models.DateTimeField()
    #文章摘要
    #指定black=True,即可为空
    excerpt = models.CharField(max_length=200,blank=True)
    #一个分类可以有多篇文章，一篇文章只能对应一个分类，即分类和文章是一对多的关系
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    #一个标签可以对应多篇文章，一篇文章也可以对应多个分类，即标签和文章是多对多的关系，标签也可能为空，所以blank=True.
    tags = models.ManyToManyField(Tag,blank=True)
    author = models.ForeignKey(User)
    views = models.PositiveIntegerField(default=0)
    is_delete = models.CharField(max_length=2,default='0')


    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    class Meta:
        ordering = ['-created_time']

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)
