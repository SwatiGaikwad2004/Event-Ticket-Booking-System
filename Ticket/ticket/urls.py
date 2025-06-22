"""
URL configuration for ticket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from home.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name ='home'),
    #  path('', views.home, name='home'),
   path('signup/', signup_view, name='signup'),
   path('login/', login_view, name='login'),
   path('logout/', logout_view, name='logout'),
   path('event/<int:event_id>/', event_detail, name='event_detail'),
   path('book/<int:event_id>/', book_ticket, name='book_ticket'),
   path('my-bookings/', my_bookings, name='my_bookings'),
   path('edit-profile/', edit_profile, name='edit_profile'),
   path('dummy-payment/',dummy_payment, name='dummy_payment'),
   path('host-dashboard/',host_dashboard, name='host_dashboard'),
   path('bookings/<int:event_id>/',view_bookings, name='view_bookings'),
   path('event/<int:event_id>/edit/', edit_event, name='edit_event'),
   path('event/add/', add_event, name='add_event'),
   path('event/<int:event_id>/delete/', delete_event, name='delete_event'),


]
