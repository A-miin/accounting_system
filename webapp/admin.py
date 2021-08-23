from django.contrib import admin
from webapp.models import Member, Region, Village
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_tag', 'name', 'phone_number1', 'region', 'village']
    list_filter = ['region', 'village','deleted']
    search_fields = ['name', 'surname', 'phone_number1', 'phone_number2', 'whatsapp_number']
    readonly_fields = ('id','image_tag')

    def get_queryset(self, request):
        queryset = super(MemberAdmin,self).get_queryset(request)
        queryset = queryset.order_by('deleted')
        return queryset

admin.site.register(Member, MemberAdmin)
admin.site.register(Region)
admin.site.register(Village)
