from django.urls import path
from mi_app.views import index

urlpatterns = [
    path('', index, name='index'),
]