import unidecode as unidecode
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from unidecode import unidecode
NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class Category(models.Model):
    """
    Represents a category for products.
    Stores a name and a description for each category.
    """
    name = models.CharField(max_length=255, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        """
        Returns the category name and description as a string.
        """
        return f'{self.name} {self.description}'

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ('name',)


class Product(models.Model):
    """
    Represents a product within a category.
    Includes information like name, description, image, price, and stock status.
    """
    name = models.CharField(max_length=100, verbose_name='наименование')
    # slug = models.SlugField(max_length=200, unique=False, default='')
    description = models.TextField(verbose_name='описание')
    picture = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, verbose_name='категория', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    last_modified = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')
    in_stock = models.BooleanField(default=True, verbose_name='в наличии')

    # def save(self, *args, **kwargs):
    #     if not self.slug:  # If no slug is provided, generate one from the title
    #
    #         self.slug = slugify(unidecode(self.name))
    #     super(Product, self).save(*args, **kwargs)

    def __str__(self):
        """
        Returns the product name and description as a string.
        """
        return f'{self.name} {self.description}'

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ('-created_at',)


class Contacts(models.Model):
    """
    Stores contact information for individuals or entities.
    Includes name, last name, email, and town.
    """
    name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    email = models.EmailField(verbose_name='эл. почта')
    town = models.CharField(max_length=50, verbose_name='город')

    def __str__(self):
        """
        Returns the contact's name and town as a string.
        """
        return f'{self.name} {self.town}'

    class Meta:
        verbose_name = "контакт"
        verbose_name_plural = "контакты"
        ordering = ('town',)


class BlogPost(models.Model):
    """
    Represents a blog post with a title, slug, content, and preview image.
    Includes the date of creation, publication status, and view count.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    preview = models.ImageField(upload_to='blog_previews/', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:  # If no slug is provided, generate one from the title

            self.slug = slugify(unidecode(self.title))
        super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        """
        Returns the blog post title as a string.
        """
        return self.title
