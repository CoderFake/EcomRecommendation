from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_stars(rating):
    stars_html = ''
    for i in range(5):
        if i < rating:
            stars_html += '<i class="ecicon eci-star fill"></i>'
        else:
            stars_html += '<i class="ecicon eci-star-o"></i>'
    return mark_safe(stars_html)  # Đánh dấu chuỗi là "an toàn"
