from django import forms
from .models import Room, Device, Switch

# --- Комнаты ---

ROOM_CHOICES = [
    ('Вітальня', '🛋️ Вітальня'),
    ('Кухня', '🍽️ Кухня'),
    ('Спальня', '🛏️ Спальня'),
    ('Ванна', '🛁 Ванна'),
    ('Кабінет', '💻 Кабінет'),
]

ICON_MAP = {
    'Вітальня': '🛋️',
    'Кухня': '🍽️',
    'Спальня': '🛏️',
    'Ванна': '🛁',
    'Кабінет': '💻',
}

ALLOWED_DEVICES_BY_ROOM = {
    'Вітальня': ['tv', 'light', 'climate', 'air_purifier', 'robot_vacuum'],
    'Кухня': ['kettle', 'fridge', 'light', 'climate'],
    'Спальня': ['light', 'climate', 'humidifier', 'thermostat'],
    'Ванна': ['washer', 'light', 'humidity', 'ventilation'],
    'Кабінет': ['light', 'climate', 'tv', 'smart_plug'],
}


class RoomForm(forms.ModelForm):
    name = forms.ChoiceField(choices=ROOM_CHOICES, label="Назва кімнати")

    class Meta:
        model = Room
        fields = ['name']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.icon = ICON_MAP.get(self.cleaned_data['name'], '📦')
        if commit:
            instance.save()
        return instance


# --- Устройства ---

class AddDeviceForm(forms.Form):
    device_type = forms.ChoiceField(
        choices=Device.DEVICE_TYPES,
        widget=forms.HiddenInput()
    )

    def save(self, room):
        device_type = self.cleaned_data['device_type']
        icon = Device.ICONS.get(device_type, '🔧')

        if device_type == 'light':
            count = Device.objects.filter(device_type='light').count() + 1
            name = f"Лампа {count}"
        else:
            name = dict(Device.DEVICE_TYPES).get(device_type, "Пристрій")

        return Device.objects.create(
            room=room,
            name=name,
            device_type=device_type,
            icon=icon,
            is_on=False,
        )


# forms.py

from .models import Switch, Device
from django import forms

class AddSwitchForm(forms.ModelForm):
    linked_lamps = forms.ModelMultipleChoiceField(
        queryset=Device.objects.filter(device_type='light'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Лампи, які керуються"
    )

    class Meta:
        model = Switch
        fields = ['name', 'icon', 'linked_lamps']

    def save(self, room, commit=True):
        instance = super().save(commit=False)
        instance.room = room
        if commit:
            instance.save()
            self.save_m2m()
        return instance

