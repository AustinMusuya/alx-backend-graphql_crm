#!/bin/bash

# Navigate to project root (adjust if manage.py is not at repo root)
cd "$(dirname "$0")/../.." || exit 1

# Run the Django shell command
deleted_count=$(python3 manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

cutoff_date = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(orders__isnull=True) | Customer.objects.exclude(orders__created_at__gte=cutoff_date)
deleted, _ = qs.distinct().delete()
print(deleted)
")

# Log result
echo \"\$(date '+%Y-%m-%d %H:%M:%S') - Deleted \$deleted_count customers\" >> /tmp/customer_cleanup_log.txt
