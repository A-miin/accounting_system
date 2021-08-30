"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from webapp.views.member import test_list
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _("Коомдук Бирикме")
admin.site.site_title = _("Коомдук Бирикме")
admin.site.index_title = _("Коомдук Бирикме")
admin.site.site_url= '/admin/webapp/membershipfee/'
admin.site.enable_nav_sidebar=False

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', test_list),
    path('admin/', admin.site.urls),
    path('', include('webapp.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
