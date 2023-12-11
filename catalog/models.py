from django.db import models

NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.name} {self.description}'

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    picture = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, verbose_name='категория', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='цена за штуку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    last_modified = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')

    in_stock = models.BooleanField(default=True, verbose_name='в наличии')

    def __str__(self):
        return f'{self.name} {self.description}'

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ('-created_at',)


class Contacts(models.Model):
    name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    email = models.EmailField(verbose_name='эл. почта')
    town = models.CharField(max_length=50, verbose_name='город')

    def __str__(self):
        return f'{self.name} {self.town}'

    class Meta:
        verbose_name = "контакт"
        verbose_name_plural = "контакты"
        ordering = ('town',)
