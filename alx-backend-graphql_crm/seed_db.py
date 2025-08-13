import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Product

Customer.objects.create(
    name="Test User", email="test@example.com", phone="+1234567890"
)
Product.objects.create(name="Sample Product", price=10.99, stock=100)

print("Database seeded successfully!")
