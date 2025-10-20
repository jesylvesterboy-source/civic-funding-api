from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from core.models import TimeStampedModel, AuditModel
from core.export_import import CustomExportMixin

class Customer(AuditModel, CustomExportMixin):
    """Centralized customer management with demographic tracking"""
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    AGE_RANGE_CHOICES = [
        ('18-25', '18-25 years'),
        ('26-35', '26-35 years'),
        ('36-45', '36-45 years'),
        ('46-55', '46-55 years'),
        ('56-65', '56-65 years'),
        ('65_plus', '65+ years'),
    ]

    # Core Customer Information
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    age_range = models.CharField(max_length=10, choices=AGE_RANGE_CHOICES)

    # Enhanced Customer Profile
    email = models.EmailField(blank=True, null=True)
    location = models.ForeignKey('farmers.Location', on_delete=models.SET_NULL, null=True, blank=True)
    customer_since = models.DateField(auto_now_add=True)
    loyalty_tier = models.CharField(max_length=20, choices=[
        ('new', 'New Customer'),
        ('regular', 'Regular Customer'),
        ('premium', 'Premium Customer'),
        ('wholesale', 'Wholesale Customer'),
    ], default='new')

    # Business Intelligence Fields
    preferred_categories = models.CharField(max_length=500, blank=True, null=True, help_text='Comma-separated preferred product categories')
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_purchases = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

    @property
    def purchase_count(self):
        return self.sales.count()

    def update_customer_metrics(self):
        """Update customer metrics based on sales data"""
        sales = self.sales.filter(status='paid')
        if sales.exists():
            self.total_purchases = sum(sale.final_amount for sale in sales)
            self.average_order_value = self.total_purchases / sales.count()
            self.save()

    @classmethod
    def export_to_csv(cls):
        """Export customers with comprehensive data"""
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customers.csv"'
        writer = csv.writer(response)

        headers = [
            'Customer Name', 'Phone Number', 'Gender', 'Age Range', 'Email',
            'Location', 'Customer Since', 'Loyalty Tier', 'Total Purchases',
            'Average Order Value', 'Purchase Count'
        ]
        writer.writerow(headers)

        for customer in cls.objects.all():
            writer.writerow([
                customer.name,
                customer.phone_number,
                customer.gender,
                customer.age_range,
                customer.email or '',
                customer.location.name if customer.location else '',
                customer.customer_since.strftime('%Y-%m-%d'),
                customer.loyalty_tier,
                customer.total_purchases,
                customer.average_order_value,
                customer.purchase_count
            ])

        return response

class ProductCategory(TimeStampedModel, CustomExportMixin):
    """Hierarchical product categorization"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Product Categories'

class Product(TimeStampedModel, CustomExportMixin):
    """Centralized product catalog with variants"""
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Liter'),
        ('ml', 'Milliliter'),
        ('bag', 'Bag'),
        ('sack', 'Sack'),
        ('piece', 'Piece'),
        ('set', 'Set'),
        ('pack', 'Pack'),
    ]

    # Core Product Information
    name = models.CharField(max_length=200)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)

    # Pricing and Inventory
    unit_measure = models.CharField(max_length=10, choices=UNIT_CHOICES)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Product Attributes for Variants
    brand = models.CharField(max_length=100, blank=True, null=True)
    variety = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True, null=True)

    # Status and Tracking
    is_active = models.BooleanField(default=True)
    sku = models.CharField(max_length=50, unique=True, help_text='Stock Keeping Unit')

    def __str__(self):
        attributes = []
        if self.brand: attributes.append(self.brand)
        if self.variety: attributes.append(self.variety)
        if self.size: attributes.append(self.size)
        attr_str = f" ({', '.join(attributes)})" if attributes else ""
        return f'{self.name}{attr_str}'

    @property
    def profit_margin(self):
        if self.cost_price > 0:
            return ((self.selling_price - self.cost_price) / self.cost_price) * 100
        return 0

    @property
    def needs_restock(self):
        return self.current_stock <= self.minimum_stock

    @property
    def attribute_name(self):
        """Combined attribute name for display"""
        attributes = []
        if self.brand: attributes.append(self.brand)
        if self.variety: attributes.append(self.variety)
        if self.size: attributes.append(self.size)
        return ', '.join(attributes) if attributes else 'N/A'

class Sale(AuditModel, CustomExportMixin):
    """Comprehensive sales tracking with business intelligence"""
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Bank Transfer'),
        ('credit', 'Credit'),
        ('cheque', 'Cheque'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    # Core Sale Information
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales')
    sale_date = models.DateTimeField(auto_now_add=True)
    sale_number = models.CharField(max_length=50, unique=True)

    # Transaction Details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True, null=True)

    # Financial Summary (auto-calculated)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Location and Channel
    sale_location = models.ForeignKey('farmers.Location', on_delete=models.SET_NULL, null=True, blank=True)
    sales_channel = models.CharField(max_length=20, choices=[
        ('store', 'Physical Store'),
        ('online', 'Online'),
        ('field', 'Field Sales'),
        ('agent', 'Sales Agent'),
    ], default='store')

    def save(self, *args, **kwargs):
        # Auto-generate sale number if not set
        if not self.sale_number:
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_sale = Sale.objects.filter(sale_number__startswith=f'SALE-{date_str}').order_by('-sale_number').first()
            if last_sale:
                last_num = int(last_sale.sale_number.split('-')[-1])
                self.sale_number = f'SALE-{date_str}-{last_num + 1:04d}'
            else:
                self.sale_number = f'SALE-{date_str}-0001'

        # Auto-calculate totals
        if hasattr(self, 'items'):
            self.total_amount = sum(item.line_total for item in self.items.all())
            self.final_amount = self.total_amount - self.discount_amount + self.tax_amount

        super().save(*args, **kwargs)

        # Update customer metrics when sale is completed
        if self.status == 'paid':
            self.customer.update_customer_metrics()

    def __str__(self):
        return f'{self.sale_number} - {self.customer.name}'

    @property
    def item_count(self):
        return self.items.count()

    @classmethod
    def get_sales_metrics(cls):
        """Get comprehensive sales metrics"""
        today = timezone.now()
        last_30_days = today - timedelta(days=30)

        metrics = {
            'total_sales': cls.objects.filter(status='paid').count(),
            'total_revenue': cls.objects.filter(status='paid').aggregate(Sum('final_amount'))['final_amount__sum'] or 0,
            'average_sale_value': cls.objects.filter(status='paid').aggregate(Avg('final_amount'))['final_amount__avg'] or 0,
            'recent_sales_count': cls.objects.filter(sale_date__gte=last_30_days, status='paid').count(),
            'recent_revenue': cls.objects.filter(sale_date__gte=last_30_days, status='paid').aggregate(Sum('final_amount'))['final_amount__sum'] or 0,
        }
        return metrics

    @classmethod
    def export_to_csv(cls):
        """Export comprehensive sales data"""
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales.csv"'
        writer = csv.writer(response)

        headers = [
            'Sale Number', 'Sale Date', 'Customer Name', 'Customer Phone', 'Customer Gender',
            'Customer Age Range', 'Payment Method', 'Status', 'Total Amount', 'Tax Amount',
            'Discount Amount', 'Final Amount', 'Item Count', 'Sale Location', 'Sales Channel'
        ]
        writer.writerow(headers)

        for sale in cls.objects.all().select_related('customer', 'sale_location'):
            writer.writerow([
                sale.sale_number,
                sale.sale_date.strftime('%Y-%m-%d %H:%M'),
                sale.customer.name,
                sale.customer.phone_number,
                sale.customer.gender,
                sale.customer.age_range,
                sale.payment_method,
                sale.status,
                sale.total_amount,
                sale.tax_amount,
                sale.discount_amount,
                sale.final_amount,
                sale.item_count,
                sale.sale_location.name if sale.sale_location else '',
                sale.sales_channel
            ])

        return response

    @classmethod
    def export_sales_records_csv(cls):
        """Export sales records with exact requested headlines"""
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales_records.csv"'
        writer = csv.writer(response)

        # Exact headers you requested
        headers = [
            'Customer name', 'Phone Number', 'Gender', 'Age range', 
            'Product', 'Attribute Name', 'Unit Measure', 'Quantity', 
            'Unit Price', 'Product Amount'
        ]
        writer.writerow(headers)

        for sale in cls.objects.all().prefetch_related('items__product', 'customer'):
            for item in sale.items.all():
                writer.writerow([
                    sale.customer.name,
                    sale.customer.phone_number,
                    sale.customer.gender,
                    sale.customer.age_range,
                    item.product.name,
                    item.attribute_name,
                    item.product.unit_measure,
                    item.quantity,
                    item.unit_price,
                    item.line_total
                ])

        return response

class SaleItem(TimeStampedModel):
    """Individual items within a sale with all requested fields"""
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    # Track product attributes at time of sale
    product_variety = models.CharField(max_length=100, blank=True, null=True)
    product_brand = models.CharField(max_length=100, blank=True, null=True)
    product_size = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Capture product attributes at time of sale
        if not self.product_variety:
            self.product_variety = self.product.variety
        if not self.product_brand:
            self.product_brand = self.product.brand
        if not self.product_size:
            self.product_size = self.product.size

        # Update stock when sale item is created
        if not self.pk:  # Only on creation
            self.product.current_stock -= self.quantity
            self.product.save()

        super().save(*args, **kwargs)

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    @property
    def attribute_name(self):
        """Combined attribute name for display"""
        attributes = []
        if self.product_brand:
            attributes.append(self.product_brand)
        if self.product_variety:
            attributes.append(self.product_variety)
        if self.product_size:
            attributes.append(self.product_size)
        return ', '.join(attributes) if attributes else 'N/A'

    def __str__(self):
        return f'{self.product.name} - {self.quantity} {self.product.unit_measure}'

class Purchase(AuditModel, CustomExportMixin):
    """Supplier purchase tracking with inventory management"""
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='purchases')
    purchase_date = models.DateTimeField(auto_now_add=True)
    purchase_number = models.CharField(max_length=50, unique=True)

    # Purchase Details
    supplier = models.CharField(max_length=200)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[
        ('ordered', 'Ordered'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ], default='ordered')

    def save(self, *args, **kwargs):
        # Auto-generate purchase number
        if not self.purchase_number:
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_purchase = Purchase.objects.filter(purchase_number__startswith=f'PUR-{date_str}').order_by('-purchase_number').first()
            if last_purchase:
                last_num = int(last_purchase.purchase_number.split('-')[-1])
                self.purchase_number = f'PUR-{date_str}-{last_num + 1:04d}'
            else:
                self.purchase_number = f'PUR-{date_str}-0001'

        # Auto-calculate total
        if hasattr(self, 'items'):
            self.total_amount = sum(item.line_total for item in self.items.all())

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.purchase_number} - {self.customer.name}'

    @classmethod
    def get_purchase_metrics(cls):
        """Get comprehensive purchase metrics"""
        today = timezone.now()
        last_30_days = today - timedelta(days=30)

        metrics = {
            'total_purchases': cls.objects.filter(status='received').count(),
            'total_purchase_amount': cls.objects.filter(status='received').aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
            'average_purchase_value': cls.objects.filter(status='received').aggregate(Avg('total_amount'))['total_amount__avg'] or 0,
            'recent_purchases_count': cls.objects.filter(purchase_date__gte=last_30_days, status='received').count(),
            'recent_purchase_amount': cls.objects.filter(purchase_date__gte=last_30_days, status='received').aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        }
        return metrics

    @classmethod
    def export_to_csv(cls):
        """Export comprehensive purchase data"""
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="purchases.csv"'
        writer = csv.writer(response)

        headers = [
            'Purchase Number', 'Purchase Date', 'Customer Name', 'Customer Phone',
            'Customer Gender', 'Customer Age Range', 'Supplier', 'Total Amount', 'Status'
        ]
        writer.writerow(headers)

        for purchase in cls.objects.all().select_related('customer'):
            writer.writerow([
                purchase.purchase_number,
                purchase.purchase_date.strftime('%Y-%m-%d %H:%M'),
                purchase.customer.name,
                purchase.customer.phone_number,
                purchase.customer.gender,
                purchase.customer.age_range,
                purchase.supplier,
                purchase.total_amount,
                purchase.status
            ])

        return response

    @classmethod
    def export_purchase_records_csv(cls):
        """Export purchase records with exact requested headlines"""
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="purchase_records.csv"'
        writer = csv.writer(response)

        # Exact headers you requested
        headers = [
            'Customer name', 'Phone Number', 'Gender', 'Age range',
            'Product Category', 'Product', 'Attribute', 'Unit Measure',
            'Quantity', 'Unit Price'
        ]
        writer.writerow(headers)

        for purchase in cls.objects.all().prefetch_related('items__product_category'):
            for item in purchase.items.all():
                writer.writerow([
                    purchase.customer.name,
                    purchase.customer.phone_number,
                    purchase.customer.gender,
                    purchase.customer.age_range,
                    item.product_category.name,
                    item.product_name,
                    item.product_attribute or '',
                    item.unit_measure,
                    item.quantity,
                    item.unit_price
                ])

        return response

class PurchaseItem(TimeStampedModel):
    """Individual items within a purchase with all requested fields"""
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product_category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200)
    product_attribute = models.CharField(max_length=100, blank=True, null=True)
    unit_measure = models.CharField(max_length=10, choices=Product.UNIT_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        # Update product stock when purchase is received
        if self.purchase.status == 'received' and not self.pk:
            try:
                # Try to find existing product
                product = Product.objects.filter(
                    name=self.product_name,
                    product_category=self.product_category
                ).first()
                
                if product:
                    product.current_stock += self.quantity
                    product.save()
            except Product.DoesNotExist:
                # Product doesn't exist, that's okay for purchase records
                pass

        super().save(*args, **kwargs)

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    @property
    def full_product_name(self):
        """Product name with attributes"""
        if self.product_attribute:
            return f"{self.product_name} ({self.product_attribute})"
        return self.product_name

    def __str__(self):
        return f'{self.product_name} - {self.quantity} {self.unit_measure}'
    @classmethod
    def export_to_csv(cls):
        """Export product categories to CSV"""
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="product_categories.csv"'
        writer = csv.writer(response)

        headers = ['Name', 'Description', 'Parent Category', 'Created', 'Updated']
        writer.writerow(headers)

        for category in cls.objects.all():
            writer.writerow([
                category.name,
                category.description or '',
                category.parent_category.name if category.parent_category else '',
                category.created_at.strftime('%Y-%m-%d %H:%M'),
                category.updated_at.strftime('%Y-%m-%d %H:%M')
            ])

        return response

