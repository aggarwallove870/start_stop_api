# from django.contrib import admin
# from .models import *
#
# # Register your models here.
#
# class ProjectMemberAdmin(admin.ModelAdmin):
#     fields = ['member_type']
#     list_display = ('member_type',)
#
#
# class PackageAdmin(admin.ModelAdmin):
#     fields = ['package_name', 'package_price', 'project_member',]
#     list_display = ('package_name', 'package_price',)
#
# class ClientDetailAdmin(admin.ModelAdmin):
#     fields = ['user']
#     list_display = ('user',)
#
# class PurchasedHistoryAdmin(admin.ModelAdmin):
#     fields = ['client','package','sevice', 'payment_method']
#     list_display = ('client','package','sevice','payment_method')
#
#
#  # fields = ['package', 'client','amount','currency', 'payment_id', 'payment_status', 'client_secret', 'payment_error_id','error_msg']
#  #    list_display = ('package', 'client','amount', 'payment_id', 'payment_status', 'client_secret',)
#
# class WebsiteCategoryAdmin(admin.ModelAdmin):
#     fields = ['website_category']
#     list_display = ('website_category',)
#
# class WebProductAdmin(admin.ModelAdmin):
#     fields = ['title','web_category', 'website_link', 'price','website_image','discount_percentage']
#     list_display = ('title','web_category', 'website_link', 'price',)
#
# class PaymentMethodAdmin(admin.ModelAdmin):
#
#
#     fields = ['payment_status', 'method_type', 'amount','payment_id','currency','client_secret','paytm_orderid','pdf_name','discount_amount']
#     list_display = ('client_name','payment_status', 'method_type', 'amount','payment_id','currency','client_secret','paytm_orderid','pdf_name','discount_amount')
#
#     def client_name(self,obj):
#
#         history = PurchasedHistory.objects.get(payment_method=obj)
#         return history.client.user.username
#
# class CustomQuoteAdmin(admin.ModelAdmin):
#     fields = ['email', 'expected_time', 'comment','quote_file']
#     list_display = ('email', 'expected_time', 'comment',)
#
# class DiscountPackageAdmin(admin.ModelAdmin):
#     fields = ['discount_name', 'discount_percentage']
#     list_display = ('discount_name', 'discount_percentage')
#
#
#
# admin.site.register(ProjectMember,ProjectMemberAdmin)
# admin.site.register(Package,PackageAdmin)
# admin.site.register(ClientDetail,ClientDetailAdmin)
# admin.site.register(PurchasedHistory,PurchasedHistoryAdmin)
# admin.site.register(WebsiteCategory,WebsiteCategoryAdmin)
# admin.site.register(WebProduct,WebProductAdmin)
# admin.site.register(PaymentMethod,PaymentMethodAdmin)
# admin.site.register(CustomQuote,CustomQuoteAdmin)
# admin.site.register(DiscountPackage,DiscountPackageAdmin)