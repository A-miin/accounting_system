from django.contrib import admin
from django.urls import reverse
from rangefilter.filters import DateRangeFilter

from webapp.models import Member, Region, Village, MembershipFee, Payments
from django.utils.html import mark_safe, format_html
from django.utils.translation import gettext_lazy as _


# Register your models here.

class IsPayed(admin.SimpleListFilter):
    title = _('Мүчөлүк төлөмдөрдөн')
    parameter_name = 'Мүчөлүк төлөмдөрдөн'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('бошотулган')),
            ('No', _('бошотулбаган')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(membership_fee=True)
        elif value == 'No':
            return queryset.filter(membership_fee=False)
        return queryset


class Deleted(admin.SimpleListFilter):
    title = _('Мүчөлөр')
    parameter_name = 'Мүчөлөр'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Активдүү')),
            ('No', _('Өчүрүлгөн')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(deleted=None)
        elif value == 'No':
            return queryset.exclude(deleted=None)
        return queryset


class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'name', 'phone_number1', 'region', 'village',
                    'membership_payment', 'delete']
    list_filter = ['region', 'village', Deleted, IsPayed]
    search_fields = ['name', 'surname', 'phone_number1', 'phone_number2', 'whatsapp_number']
    readonly_fields = ('id', 'created_at')
    ordering = ('deleted', '-created_at')
    list_display_links = ['name']

    def image(self, obj):
        img = obj.avatar
        if img:
            output = f' <a href="{img.url}?w=80&h=50" target="_blank">' \
                     f'<img src="{img.url}?w=80&h=50" ' \
                     f'height=80 width=80/></a>'
        else:
            output = ""
        return mark_safe(output)
    image.short_description = _("Сүрөтү")



    def delete(self, obj):
        return format_html(
            '''
            <a class="btn btn-success" href="{}" style="color: orange" >
                <svg  xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                  <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                  <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
                </svg>
            </a>
            <a class="btn btn-primary" href="{}" style="color:green">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-lines-fill" viewBox="0 0 16 16">
                  <path d="M6 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-5 6s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H1zM11 3.5a.5.5 0 0 1 .5-.5h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 1-.5-.5zm.5 2.5a.5.5 0 0 0 0 1h4a.5.5 0 0 0 0-1h-4zm2 3a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1h-2zm0 3a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1h-2z"/>
                </svg>
            </a>
            <a class="btn btn-danger" href="{}" style="color:red">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                  <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
                </svg>
            </a>
            ''',
            reverse('admin:webapp_member_change', args=[obj.pk]),
            reverse('admin:webapp_member_change', args=[obj.pk]),
            reverse('webapp:delete', args=[obj.pk]),
        )

    delete.short_description = _("Башкаруу")


class MembershipFeeAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ['id', 'full_name', 'amount', 'payed_at', 'transfer_type', 'is_payed']
    list_filter = ['payer','payed_at', ('payed_at', DateRangeFilter), 'is_payed']
    search_fields = ['payer', 'amount', 'payed_at', 'transfer_type']
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)
    list_display_links = ['full_name']

    def full_name(self, obj):
        return f'{obj.payer.name} {obj.payer.surname}'

    full_name.short_description = _("Мүчө")

class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'payer', 'info', 'amount', 'created_at', 'payments_type']
    list_filter = ['type', 'created_at', ('created_at', DateRangeFilter)]
    search_fields = ['payer', 'info', 'amount']
    readonly_fields = ('id',)
    ordering = ('-created_at',)
    list_display_links = ['payer']

    def payments_type(self, obj):
        if obj.type == 'income':
            output = '<p style="color:green">' \
                     '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16">' \
                     '<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>' \
                     '<path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>' \
                     '</svg>' \
                     '</p>'
        elif obj.type == 'expense':
            output = '<p style="color:black">' \
                     '<svg class="text-danger" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dash-circle" viewBox="0 0 16 16">' \
                     '<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>' \
                     '<path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"/>' \
                     '</svg>' \
                     '</p>'
        return mark_safe(output)


class VillageInline(admin.TabularInline):
    model = Village
    fields = ('name',)


class RegionAdmin(admin.ModelAdmin):
    inlines = (VillageInline,)
    list_display = ['id', 'name', 'delete']
    list_filter = ['name', ]
    search_fields = ['id', 'name']
    readonly_fields = ('id',)
    list_display_links = ['name', ]
    fields = ('id', 'name')


    def delete(self, obj):
        return format_html(
            '''
            <a class="btn btn-success" href="{}" style="color: orange" >
                <svg  xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                  <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                  <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
                </svg>
            </a>
            <a class="btn btn-success" style="color:red" href="{}">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                  <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
                </svg>
            </a>
            ''',
            reverse('admin:webapp_region_change', args=[obj.pk]),
            reverse('webapp:region-delete', args=[obj.pk]),
        )

    delete.short_description = _("Башкаруу")


class VillageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'region', 'delete']
    list_filter = ['region', ]
    search_fields = ['id', 'name']
    readonly_fields = ('id',)
    list_display_links = ['name', ]

    def delete(self, obj):
        return format_html(
            '''
            <a class="btn btn-success" href="{}" style="color: orange" >
                <svg  xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                  <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                  <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
                </svg>
            </a>
            <a class="btn btn-success" style="color:red" href="{}">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash-fill" viewBox="0 0 16 16">
                  <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/>
                </svg>
            </a>
            ''',
            reverse('admin:webapp_village_change', args=[obj.pk]),
            reverse('webapp:village-delete', args=[obj.pk]),
        )

    delete.short_description = _("Башкаруу")


admin.site.register(Member, MemberAdmin)
admin.site.register(MembershipFee, MembershipFeeAdmin)
admin.site.register(Payments, PaymentsAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Village, VillageAdmin)
