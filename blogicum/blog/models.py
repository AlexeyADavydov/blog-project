from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class CoreModel(models.Model):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class Category(CoreModel):
    title = models.CharField('Заголовок', max_length=256)

    description = models.TextField('Описание')

    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, '
                   'дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(CoreModel):
    name = models.CharField(
        'Название места',
        max_length=256
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(CoreModel):
    title = models.CharField('Заголовок', max_length=256)

    text = models.TextField('Текст')

    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.')
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение',
        related_name='posts',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts'
    )

    image = models.ImageField(
        "Изображение",
        upload_to='post_images',
        blank=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def get_absolute_url(self):
        return f'/profile/{self.author}/'

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField('Комментарий')

    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name='comments'
    )

    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('created_at',)
        default_related_name = 'comments'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={"pk": self.post})
