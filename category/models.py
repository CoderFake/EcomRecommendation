from django.db import models
from django.urls import reverse

category_main_choices = (
    ('Electronics', 'Electronics'),
    ('Clothing', 'Clothing'),
    ('Food', 'Food'),
)


class CategoryMain(models.Model):
    category_name = models.CharField(max_length=50 )
    slug = models.SlugField(max_length=100, unique=True)
    cat_main_img = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['category_name']

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(CategoryMain, related_name='subcategories', on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    cat_sub_img = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'
        ordering = ['sub_category_name']

    def get_url(self):
        return reverse('products_by_sub_category', args=[self.slug])

    def __str__(self):
        return self.sub_category_name
