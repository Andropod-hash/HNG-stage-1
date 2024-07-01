from django.urls import path
from .views import temperature

urlpatterns = [
    path('temp/', temperature, name='temp'),
    # path(r'swagger/', schema_view),  # Swagger API documentation
]