from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    is_available = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('product_list', args=[self.slug])

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    product_name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=300, unique=True, allow_unicode=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='product')
    stuck = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_new = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
