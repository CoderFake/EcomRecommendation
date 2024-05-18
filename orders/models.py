import requests
from django.db import models
from accounts.models import Account
from store.models import Product, Variation

def get_locations(id, parent_id):
    api_url = "https://member.lazada.vn/locationtree/api/getSubAddressList?countryCode=VN"
    if parent_id:
        api_url += f"&addressId={parent_id}"
    response = requests.get(api_url)
    locations = response.json().get('module', [])
    for location in locations:
        if location.get('id') == id:
            return location.get('name')
    return None

class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.FloatField()
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('new', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    ORDER_STATUS = (
        ('Accepted', 'Accepted'),
        ('Ready to ship', 'Ready to ship'),
        ('On shipping', 'On shipping'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Return', 'Return')
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.OneToOneField(Payment, related_name="order", on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    payment_method = models.CharField(max_length=50, blank=True)
    road = models.CharField(max_length=150, blank=True)
    ward = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    order_note = models.TextField(blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default='new')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_items = models.IntegerField(default=0)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default='Accepted')
    is_view = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name + ' ' + self.order_number

    def address(self):
        return self.road + ', ' + get_locations(self.ward, self.district) + ', ' + get_locations(self.district, self.city) + ', ' + get_locations(self.city, '')
    
    def date(self):
        return self.created_at.strftime('%d %m %Y')


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order', on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.product.product_name


class Review(models.Model):
    order_product = models.ForeignKey(OrderProduct, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField(verbose_name="Review Text")
    rating = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)], verbose_name="Rating")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review for {self.order_product.product.product_name} by {self.order_product.order.user.username}'

