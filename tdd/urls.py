from django.urls import path

import tdd.views

urlpatterns = [
    path('signup', tdd.views.member_signup, name='member_signup'),
]