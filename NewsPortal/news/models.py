from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator


class Author(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = self.post_set.aggregate(models.Sum('rating'))['rating__sum'] or 0
        post_rating *= 3
        comment_rating = self.user.comment_set.aggregate(models.Sum('rating'))['rating__sum'] or 0
        post_comment_rating = Comment.objects.filter(post__author=self).aggregate(models.Sum('rating'))['rating__sum'] or 0

        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()

class Post(models.Model):
    article = "AR"
    text = "NW"

    TYPES = [
        (article, "статья"),
        (text, "новость")
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length = 2, choices = TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(to='Category',on_delete=models.CASCADE,related_name='posts')
    name = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + "..."

    def __str__(self):
        return f'{self.name.title()}: {self.content[:20]}'

    class Meta:
        ordering = ['timestamp']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()
