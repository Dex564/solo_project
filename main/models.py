from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
    
    def __str__(self):
        return self.name




class Product(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    main_image = models.ImageField(upload_to='products/main')
    
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-available', 'name']
        verbose_name = 'Produkt'
        verbose_name_plural = 'Produktы'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.id, self.slug])
    

