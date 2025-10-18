import os
from django.core.management import execute_from_command_line

# Auto-create superuser on startup in production
if os.environ.get('RENDER'):
    import django
    from django.db import connections
    from django.db.utils import OperationalError
    
    # Wait for database to be ready
    django.setup()
    
    from django.contrib.auth import get_user_model
    from django.db import IntegrityError
    
    try:
        # Check if database is ready
        connections['default'].cursor()
        
        User = get_user_model()
        if not User.objects.filter(username='Jeremiah').exists():
            User.objects.create_superuser(
                username='Jeremiah',
                email='jesylvesterboy@gmail.com', 
                password='7008GC@7008gc'
            )
            print(' Superuser Jeremiah created successfully in production!')
        else:
            print('ℹ  Superuser Jeremiah already exists')
    except OperationalError:
        print(' Database not ready yet, superuser creation skipped')
    except IntegrityError:
        print('ℹ  Superuser Jeremiah already exists')
    except Exception as e:
        print(f' Superuser creation failed: {e}')
