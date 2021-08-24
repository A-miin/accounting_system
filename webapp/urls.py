from django.urls import path, include
from webapp.views import IndexView, MemberDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/delete/',MemberDeleteView.as_view(), name='delete'),
]
