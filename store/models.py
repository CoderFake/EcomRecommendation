from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from category.models import CategoryMain, SubCategory


class Product(models.Model):
    # Existing fields
    product_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    category_main = models.ForeignKey(CategoryMain, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    mrp_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    short_desp = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # New fields for OLAP
    brand_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=30, null=True, blank=True)
    season = models.CharField(max_length=50,  null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail', args=[self.slug])


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(Variation_category='Color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(Variation_category='Size', is_active=True)


variation_category_choice = (
    ('Size', 'Size'),
    ('Color', 'Color'),
)


class Variation(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    Variation_value = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    objects = VariationManager()

    def __str__(self):
        return self.Variation_value


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_type = models.CharField(max_length=50, choices=[
        ('default', 'Default'),
        ('back', 'Back'),
        ('front', 'Front'),
        ('top', 'Top'),
        ('left', 'Left'),
        ('right', 'Right'),
        ('bottom', 'Bottom')
    ])
    image_url = models.URLField(max_length=2000, blank=True, null=True)

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        unique_together = ('product', 'image_type')

    def __str__(self):
        return f"{self.product.product_name} - {self.image_type}"

