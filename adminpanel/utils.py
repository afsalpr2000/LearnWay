# adminpanel/utils.py

import string
import random
from .models import Coupon

def generate_unique_coupon_code(length=10):
    """Generates a unique coupon code."""
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(characters) for _ in range(length))
        if not Coupon.objects.filter(code=code).exists():
            return code
