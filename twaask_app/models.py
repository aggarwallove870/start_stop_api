# from django.db import models
# from django.contrib.auth.models import User
#
# # Create your models here.
#
# class ProjectMember(models.Model):
#
#     member_type = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.member_type
# class DiscountPackage(models.Model):
#     choice = (('', 'Select Discount'),('w','Weekly'),('b','By Weekly'),('m','Monthly'),('q','Quarterly'),('h','Half Yearly'),('y','Yearly'))
#
#     discount_name = models.CharField(choices=choice,unique=True, max_length=100)
#     discount_percentage = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.discount_name
#
# class WebsiteCategory(models.Model):
#
#     website_category = models.CharField(max_length=100 ,unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return str(self.website_category)
#
#
# class WebProduct(models.Model):
#
#     title = models.CharField(max_length=100)
#     price = models.DecimalField(decimal_places=2,max_digits=15)
#     website_link =models.URLField()
#     web_category = models.ForeignKey(WebsiteCategory,on_delete=models.CASCADE)
#     website_image = models.ImageField(blank=True, null=True, upload_to='WebProduct')
#     discount_percentage = models.IntegerField(blank=True,null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return str(self.title)
#
#
# class Package(models.Model):
#
#     package_name = models.CharField(max_length=100)
#     package_price = models.DecimalField(decimal_places=2,max_digits=15)
#     project_member = models.ManyToManyField(ProjectMember)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     # def project_member_name(self):
#     #     return "\n".join([a.member_type for a in self.project_member_set.all()])
#     #
#     # project_member_name.short_description = "project_member"
#
#     def __str__(self):
#         return self.package_name
#
#
#
# class ClientDetail(models.Model):
#
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.user.username
#
# class PurchasedHistory(models.Model):
#     sevice = models.ForeignKey(WebProduct, on_delete=models.CASCADE, blank=True,null=True)
#     package = models.ForeignKey(Package,on_delete=models.CASCADE, blank=True, null=True)
#     client = models.ForeignKey(ClientDetail,on_delete=models.CASCADE)
#     payment_method = models.ForeignKey('PaymentMethod',on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return str(self.client.user.username)
#
# class PaymentMethod(models.Model):
#
#     status = (('', 'Select Any'), ('s', 'Success'), ('u', 'Unsuccess'))
#     payment_choices  = (('P','paytm'),('S','Stripe'))
#     method_type = models.CharField(max_length=2,choices=payment_choices,default='P')
#     payment_status = models.CharField(default='u', choices=status, max_length=2)
#     amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     msg = models.TextField(blank=True, null=True)
#     currency = models.CharField(max_length=5, blank=True, null=True)
#     payment_id = models.CharField(max_length=100, blank=True, null=True)
#     #stripe
#     client_secret = models.CharField(max_length=100,blank=True,null=True)
#     payment_error_id = models.CharField(max_length=100, blank=True, null=True)
#     #paytm
#     paytm_orderid = models.CharField(max_length=100, blank=True,null=True)
#     discount_amount = models.DecimalField(decimal_places=2, max_digits=15, blank=True, null=True)
#     pdf_name = models.CharField(max_length=100, blank=True,null=True)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return str(self.payment_id)
#
#
#
#
# class CustomQuote(models.Model):
#     expected_time = models.DateField(blank=True,null=True)
#     email = models.EmailField()
#     quote_file = models.FileField(blank=True,null=True,upload_to='quote_files')
#     comment = models.TextField(blank=True,null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#
#
#
#
#
#
