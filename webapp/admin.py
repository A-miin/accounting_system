import datetime
from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from webapp.models import Member, Region, Village, MembershipFee, TransferType, Payments
from django.utils.html import mark_safe, format_html
from django.utils.translation import gettext_lazy as _
from django.db.models import Q



# Register your models here.

class IsPayed(admin.SimpleListFilter):
    title = 'Мүчөлүк төлөмдөрдөн'
    parameter_name = 'Мүчөлүк төлөмдөрдөн'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'бошотулган'),
            ('No', 'бошотулбаган'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(membership_fee=True)
        elif value == 'No':
            return queryset.exclude(membership_fee=True)
        return queryset

class Deleted(admin.SimpleListFilter):
    title = 'Мүчөлөр'
    parameter_name = 'Мүчөлөр'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Активдүү'),
            ('No', 'Oчүрүлгөн'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(deleted=None)
        elif value == 'No':
            return queryset.exclude(deleted=None)
        return queryset

class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_tag', 'name', 'phone_number1', 'region', 'village',
                    'membership_payment','delete']
    list_filter = ['region', 'village',Deleted, IsPayed]
    search_fields = ['name', 'surname', 'phone_number1', 'phone_number2', 'whatsapp_number']
    readonly_fields = ('id','image_tag')
    ordering = ('deleted', '-created_at')
    list_display_links = ['name']

    def delete(self,obj):
        return format_html(
            '''
            <a class="btn btn-success" href="{}">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                  <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
                </svg>
            </a>
            <a class="btn btn-primary" href="{}">
                '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-lines-fill" viewBox="0 0 16 16">'\
                    '<path d="M6 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-5 6s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H1zM11 3.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 1-.5-.5zm.5 2.5a.5.5 0 0 0 0 1h4a.5.5 0 0 0 0-1h-4zm2 3a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1h-2zm0 3a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1h-2z"/>'\
                '</svg>'
            </a>
            <a class="btn btn-danger" href="{}">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                  <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
                </svg>
            </a>
            ''',
            reverse('webapp:delete', args=[obj.pk]),
            reverse('webapp:delete', args=[obj.pk]),
            reverse('webapp:delete', args=[obj.pk]),
        )

    delete.short_description = _("Башкаруу")


    def image(self, obj):
        img = obj.images.first()
        if img and img.picture:
            output = f' <a href="{img.picture.url}?w=80&h=50" target="_blank">' \
                     f'<img src="{img.picture.url}?w=80&h=50" ' \
                     f'height=50 width=80/></a>'
        else:
            output = ""
        return mark_safe(output)

class MembershipFeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'amount', 'payed_at', 'transfer_type', 'is_payed']
    list_filter = ['payer', 'payed_at','is_payed']
    search_fields = ['payer', 'amount', 'payed_at','transfer_type']
    readonly_fields = ('id',)
    ordering = ('-created_at',)
    list_display_links = ['full_name']

class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'payer', 'info', 'amount', 'created_at', 'payments_type']
    list_filter = ['type', 'created_at']
    search_fields = ['payer', 'info', 'amount']
    readonly_fields = ('id',)
    ordering = ('-created_at',)
    list_display_links = ['payer']

    def payments_type(self, obj):
        if obj.type=='income':
            output='<p style="color:green">'\
                        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">'\
                          '<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>'\
                          '<path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>'\
                        '</svg>'\
                    '</p>'
        elif obj.type=='expense':
            output = '<p style="color:red">'\
                        '<svg class="text-danger" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dash-circle" viewBox="0 0 16 16">'\
                          '<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>'\
                          '<path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"/>'\
                        '</svg>'\
                    '</p>'
        return mark_safe(output)

admin.site.register(Member, MemberAdmin)
admin.site.register(MembershipFee, MembershipFeeAdmin)
admin.site.register(Payments, PaymentsAdmin)
admin.site.register(Region)
admin.site.register(Village)