from django.urls import path
from .views import OrderCreateView

urlpatterns = [
    path('create_order/', OrderCreateView.as_view(), name='create_order'),
]
