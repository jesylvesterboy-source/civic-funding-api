from dashboard.metrics_calculator import get_role_specific_metrics
from django.contrib.auth.models import AnonymousUser

# Test with anonymous user
user = AnonymousUser()
metrics = get_role_specific_metrics(user, 'Guest')

print('REAL-TIME METRICS FROM DATABASE:')
print('=' * 40)
print(f"Farmers: {metrics['farmers']}")
print(f"Projects: {metrics['projects']}")
print(f"Active Projects: {metrics['active_projects']}")
print(f"Sales Value: ${metrics['sales_value']:,}")
print(f"Total Budget: ${metrics['budget']:,}")
print(f"Households: {metrics['households']}")
print(f"Products: {metrics['products']}")
print(f"Sales Count: {metrics['sales_count']}")
print(f"Budget Utilization: {metrics['utilization']}%")
print('=' * 40)

if metrics['farmers'] == 0 and metrics['projects'] == 0:
    print('  WARNING: Database might be empty or models not accessible')
    print(' TIP: Add some test data through Django admin')
else:
    print(' SUCCESS: Real-time metrics are working!')
