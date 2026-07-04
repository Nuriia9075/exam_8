from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser
from django.db import models

def get_avatar_path(instance, filename):
    return f'avatars/{instance.username}/{filename}'


class Author(AbstractUser):
    avatar = models.ImageField(upload_to=get_avatar_path, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False, verbose_name="Email")
    groups = models.ManyToManyField('auth.Group', related_name='author_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='author_permissions_set', blank=True)

    def __str__(self):
        return self.username + "'s User"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Topic(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank= False, null= False, verbose_name="Описание")
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, blank=False, null=False, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'{self.pk} by {self.author.username}'

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['-created_at']

class Answer(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=False, null=False, related_name='answers')
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, blank=False, null=False, related_name='answers')
    created_at=models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False, null=False, verbose_name="Описание")

    def __str__(self):
        return f'{self.pk} by {self.topic.title}'
    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural='Ответы'
        ordering = ['created_at']