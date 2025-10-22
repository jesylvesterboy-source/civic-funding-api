def detect_user_role(user):
    if not user.is_authenticated:
        return 'Guest'
    
    if user.is_superuser:
        return 'Administrator'
    
    # Check user groups
    if user.groups.filter(name__icontains='project').exists() or user.groups.filter(name__icontains='manager').exists():
        return 'Project Manager'
    elif user.groups.filter(name__icontains='field').exists() or user.groups.filter(name__icontains='officer').exists():
        return 'Field Officer' 
    elif user.groups.filter(name__icontains='finance').exists() or user.groups.filter(name__icontains='account').exists():
        return 'Finance Officer'
    else:
        return 'Staff'
