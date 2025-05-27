import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Room, Device, Switch
from .forms import RoomForm, AddDeviceForm, ALLOWED_DEVICES_BY_ROOM, AddSwitchForm
from django.template.loader import render_to_string


# Главная страница: список комнат
def home(request):
    rooms = Room.objects.all()
    form = RoomForm()

    # обрабатываем POST прямо тут (вместо отдельной вьюхи)
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'smarthome/home.html', {'rooms': rooms, 'form': form})

def reset_home(request):
    Room.objects.all().delete()
    Device.objects.all().delete()
    return redirect('home')

def device_settings_view(request, device_id):
    device = get_object_or_404(Device, id=device_id)

    html = render_to_string("smarthome/partials/device_settings.html", {'device': device})
    return JsonResponse({'html': html})



# Страница одной комнаты: список устройств + кнопки "добавить устройство"
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    devices = room.devices.all()
    switches = room.switches.prefetch_related('linked_lamps')

    # Типы устройств, которые уже есть
    existing_types = set(devices.values_list('device_type', flat=True))
    room_type = room.name  # название из ROOM_CHOICES

    # Какие типы можно ещё добавить в эту комнату
    allowed_types = ALLOWED_DEVICES_BY_ROOM.get(room_type, [])
    available_types = []
    for dt in Device.DEVICE_TYPES:
        if dt[0] in allowed_types:
            # ❗ лампочки разрешаем всегда
            if dt[0] == 'light' or dt[0] not in existing_types:
                available_types.append(dt)

    # Формы добавления устройств
    add_forms = []
    for type_code, type_label in available_types:
        form = AddDeviceForm(initial={'device_type': type_code})
        add_forms.append({
            'type': type_code,
            'label': type_label,
            'icon': Device.ICONS.get(type_code, '🔧'),
            'form': form
        })
    switch_form = AddSwitchForm()
    return render(request, 'smarthome/room_detail.html', {
        'room': room,
        'devices': devices,
        'switches': switches,  # 💡 обязательно передаём свитчи
        'add_forms': add_forms,
        'switch_form': switch_form,
    })


# Добавить устройство в комнату
def add_device_to_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        device_type = request.POST.get('device_type')
        form = AddDeviceForm({'device_type': device_type})

        if form.is_valid():
            form.save(room=room)

    return redirect('room_detail', room_id=room.id)


@csrf_exempt  # можно заменить на @csrf_protect + csrf_token в JS
def update_device(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Тільки POST, брат")

    try:
        data = json.loads(request.body)
        device_id = data.get('device_id')
        field = data.get('field')
        value = data.get('value')

        device = Device.objects.get(id=device_id)

        # Безопасная установка поля
        if not hasattr(device, field):
            return JsonResponse({'error': 'Нема такого поля'}, status=400)

        # Приведение типа (bool, int, float)
        field_type = type(getattr(device, field))
        if field_type == bool:
            value = value in [True, 'true', '1', 1]
        elif field_type == int:
            value = int(value)
        elif field_type == float:
            value = float(value)
        elif field_type == str:
            value = str(value)

        setattr(device, field, value)
        device.save()

        return JsonResponse({'success': True, 'device_id': device.id, 'field': field, 'new_value': value})

    except Device.DoesNotExist:
        return JsonResponse({'error': 'Девайс не знайдено'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
def add_switch_to_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    form = AddSwitchForm(request.POST)

    if form.is_valid():
        switch = form.save(room = room, commit=False)
        switch.room = room
        switch.save()
        form.save_m2m()
    else:
        print("❌ Invalid switch form:", form.errors)

    return redirect('room_detail', room_id=room.id)

@require_POST
@csrf_exempt
def switch_toggle_view(request, switch_id):
    try:
        switch = Switch.objects.get(id=switch_id)
        lamps = switch.linked_lamps.all()

        if not lamps.exists():
            return JsonResponse({'message': 'Немає ламп до цього вимикача'}, status=400)

        # Проверяем: если все включены — выключить, иначе включить
        all_on = all(lamp.is_on for lamp in lamps)
        new_state = not all_on

        for lamp in lamps:
            lamp.is_on = new_state
            lamp.save()

        return JsonResponse({
            'success': True,
            'switch_id': switch_id,
            'new_state': new_state,
            'message': f"Усі лампи {'увімкнено' if new_state else 'вимкнено'}",
            'last_lamp_id': lamps.last().id  # можеш юзати в JS
        })

    except Switch.DoesNotExist:
        return JsonResponse({'error': 'Вимикач не знайдено'}, status=404)