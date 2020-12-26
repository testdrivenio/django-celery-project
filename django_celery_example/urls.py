from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("member/", include('tdd.urls')),
    path("", include('polls.urls')),
]
