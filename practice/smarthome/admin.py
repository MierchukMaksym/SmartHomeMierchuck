from django.contrib import admin
from .models import Room, Device


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "icon", "created_at")
    search_fields = ("name",)
    ordering = ("created_at",)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "icon", "device_type", "room", "is_on", "created_at"
    )
    list_filter = ("device_type", "room", "is_on")
    search_fields = ("name", "room__name")
    ordering = ("room", "name")

    fieldsets = (
        ("Загальне", {
            "fields": ("name", "room", "device_type", "icon", "is_on")
        }),
        ("Світло", {
            "classes": ("collapse",),
            "fields": ("brightness",)
        }),
        ("Температура", {
            "classes": ("collapse",),
            "fields": ("temperature", "current_temperature", "target_temperature")
        }),
        ("Вологість / вода", {
            "classes": ("collapse",),
            "fields": ("humidity", "target_humidity", "water_level")
        }),
        ("Повітря", {
            "classes": ("collapse",),
            "fields": ("air_quality", "fan_speed", "ionization", "airflow_speed", "filter_status", "heating")
        }),
        ("Пралка", {
            "classes": ("collapse",),
            "fields": ("wash_mode", "wash_time_left")
        }),
        ("Рух / безпека", {
            "classes": ("collapse",),
            "fields": ("triggered", "recording")
        }),
        ("Розетка / споживання", {
            "classes": ("collapse",),
            "fields": ("power_consumption", "schedule")
        }),
        ("Пилосос", {
            "classes": ("collapse",),
            "fields": ("battery_level", "cleaning_mode", "status")
        }),
        ("Інше", {
            "classes": ("collapse",),
            "fields": ("boiling", "mode")
        }),
    )
