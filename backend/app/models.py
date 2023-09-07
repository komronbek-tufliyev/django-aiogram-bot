from django.db import models
from django.utils.translation import gettext_lazy as _
from latlong import get_lat_lot
from django.utils.html import format_html
# Create your models here.


class BotUser(models.Model):
    telegram_username = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Username'), help_text=_('Enter username'),)
    name = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Name'), help_text=_('Enter name'),)
    telegram_id = models.IntegerField(unique=True, verbose_name=_("Telegram ID"), db_index=True, help_text=_("Enter Telegram ID"))
    language = models.CharField(max_length=5, default='uz', verbose_name=_("Language"), choices=(('uz', 'Uzbek'), ('ru', 'Russian'), ('en', 'English')))
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Phone Number"))
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else f"{self.telegram_id} ID-li foydalanuvchi"

    class Meta:
        db_table = 'BotUser'
        verbose_name = _("BotUser")
        verbose_name_plural = _("BotUsers")


class Location(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, verbose_name=_("Bot User"), to_field='telegram_id')
    latitude = models.FloatField(verbose_name=_("Latitude"), max_length=50, blank=True, null=True)
    longitude = models.FloatField(verbose_name=_("Longitude"), max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        if self.latitude and self.longitude:
            return get_lat_lot(self.latitude, self.longitude)
        else:
            return "Location"
    class Meta:
        db_table = 'Location'
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        

class Category(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("Category") )
    def __str__(self):
        return self.name
    
    class Meta:
        db_table= 'Category'
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class SubCategory(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("SubCategory"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    def __str__(self):
        return self.name
    
    class Meta:
        db_table= 'SubCategory'
        verbose_name = _("SubCategory")
        verbose_name_plural = _("SubCategories")
    

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Name"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name=_("Category"), help_text=_("Select Category"))
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products', verbose_name=_("SubCategory"), null=True, blank=True, help_text=_("Select Category") )
    image = models.ImageField(upload_to='product_images', verbose_name="Image", null=True, blank=True)
    about = models.TextField(null=True, blank=True, verbose_name=_("Info"))
    price  = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(verbose_name=_("Discount"), null=True, blank=True)

    def __str__(self) -> str:
        if self.name:
            return self.name
        else:
            return "Mahsulot"
        
    @property
    def picture(self):
        if self.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%" />'.format(self.image.url))
        else:
            return "Rasm"
    class Meta:
        db_table = 'Product'
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
    
class Order(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, verbose_name=_("Bot User"), to_field='telegram_id')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.name if self.user.name else "Order"
    
    @property
    def all_products(self):
        return sum([item.quantity for item in self.items.all()])
    
    @property
    def all_shop(self):
        return sum([item.shop for item in self.items.all()])
    
    class Meta:
        db_table = 'Order'
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_("Order"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', verbose_name=_("Product"))
    quantity = models.IntegerField(verbose_name=_("Quantity"), default=1)
    
    def __str__(self) -> str:
        return "Xarid"
    
    @property
    def shop(self):
        try: 
            if self.product.discount:
                return (self.product.price - self.product.discount) * self.quantity
            else:
                return self.product.price * self.quantity
        except:
            return 0

    @property
    def product_id(self):
        return self.product.id

    class Meta:
        db_table = 'OrderItem'
        verbose_name = _("OrderItem")
        verbose_name_plural = _("OrderItems")
    

    
