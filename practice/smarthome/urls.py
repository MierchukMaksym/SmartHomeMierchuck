from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reset/', views.reset_home, name='reset_home'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('room/<int:room_id>/add-device/', views.add_device_to_room, name='add_device_to_room'),
    path('device/update/', views.update_device, name='update_device'),
    path('device/settings/<int:device_id>/', views.device_settings_view, name='device_settings'),
    path('room/<int:room_id>/add-switch/', views.add_switch_to_room, name='add_switch_to_room'),
    path('switch/toggle/<int:switch_id>/', views.switch_toggle_view, name='switch_toggle'),




]
