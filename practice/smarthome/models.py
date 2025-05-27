# smarthome/models.py

from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default="🛋️")  # эмоджи або назва іконки
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    DEVICE_TYPES = [
        ('kettle', 'Чайник'),
        ('fridge', 'Холодильник'),
        ('tv', 'Телевізор'),
        ('washer', 'Пральна машина'),
        ('light', 'Освітлення'),
        ('climate', 'Клімат-контроль'),
        ('motion_sensor', 'Датчик руху'),
        ('gas_sensor', 'Датчик загазованості'),
        ('smoke_sensor', 'Датчик диму'),
        ('camera', 'Камера'),
        ('humidifier', 'Зволожувач повітря'),
        ('air_purifier', 'Очищувач повітря'),
        ('thermostat', 'Термостат'),
        ('smart_plug', 'Розумна розетка'),
        ('robot_vacuum', 'Робот-пилосос'),
        ('ventilation', 'Бризер / вентиляція'),
    ]

    ICONS = {
        'kettle': '☕',
        'fridge': '🧊',
        'tv': '📺',
        'washer': '🧺',
        'light': '💡',
        'climate': '🌡️',
        'motion_sensor': '🎯',
        'gas_sensor': '🛢️',
        'smoke_sensor': '🔥',
        'camera': '🎥',
        'humidifier': '💧',
        'air_purifier': '🌀',
        'thermostat': '🌞',
        'smart_plug': '🔌',
        'robot_vacuum': '🤖',
        'ventilation': '🌬️',
    }

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, blank=True)  # emoji or custom
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES)
    is_on = models.BooleanField(default=False)

    # Общие / используемые поля для состояний
    brightness = models.PositiveIntegerField(null=True, blank=True)              # light
    temperature = models.FloatField(null=True, blank=True)                       # fridge, sensors
    target_temperature = models.FloatField(null=True, blank=True)               # thermostat, climate
    current_temperature = models.FloatField(null=True, blank=True)              # thermostat
    humidity = models.FloatField(null=True, blank=True)                          # humidifier
    target_humidity = models.FloatField(null=True, blank=True)                  # humidifier
    water_level = models.FloatField(null=True, blank=True)                      # humidifier
    air_quality = models.CharField(max_length=50, null=True, blank=True)        # air_purifier
    fan_speed = models.PositiveIntegerField(null=True, blank=True)              # air_purifier, ventilation
    ionization = models.BooleanField(null=True, blank=True)                     # humidifier, air_purifier
    filter_status = models.CharField(max_length=50, null=True, blank=True)      # air_purifier, ventilation
    airflow_speed = models.PositiveIntegerField(null=True, blank=True)          # ventilation
    heating = models.BooleanField(null=True, blank=True)                        # ventilation, climate
    boiling = models.BooleanField(null=True, blank=True)                        # kettle
    wash_mode = models.CharField(max_length=50, null=True, blank=True)          # washer
    wash_time_left = models.PositiveIntegerField(null=True, blank=True)         # washer
    triggered = models.BooleanField(null=True, blank=True)                      # sensors
    recording = models.BooleanField(null=True, blank=True)                      # camera
    battery_level = models.PositiveIntegerField(null=True, blank=True)          # robot_vacuum
    cleaning_mode = models.CharField(max_length=50, null=True, blank=True)      # robot_vacuum
    status = models.CharField(max_length=50, null=True, blank=True)             # robot_vacuum
    power_consumption = models.FloatField(null=True, blank=True)                # smart_plug
    schedule = models.JSONField(null=True, blank=True)                          # smart_plug, thermostat
    mode = models.CharField(max_length=50, null=True, blank=True)               # climate, thermostat

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.icon and self.device_type in self.ICONS:
            self.icon = self.ICONS[self.device_type]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.icon} {self.name} ({self.get_device_type_display()})"

    # models.py
class Switch(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='switches')
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default='🔘')
    linked_lamps = models.ManyToManyField(Device, related_name='controlled_by',
                                          limit_choices_to={'device_type': 'light'})

    def __str__(self):
        return f"{self.icon} {self.name}"

