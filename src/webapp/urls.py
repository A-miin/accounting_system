from django.urls import path, include
from webapp.views import IndexView, MemberDeleteView, RegionDeleteView, VillageDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/delete/',MemberDeleteView.as_view(), name='delete'),
    path('region/<int:pk>/delete/',RegionDeleteView.as_view(), name='region-delete'),
    path('village/<int:pk>/delete/',VillageDeleteView.as_view(), name='village-delete'),
]
