from datetime import date

from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'phone', 'email', 'check_in_date', 'check_out_date']
        labels = {
            'name': "Ім'я та прізвище",
            'phone': 'Телефон',
            'email': 'Електронна пошта',
            'check_in_date': 'Заїзд',
            'check_out_date': 'Виїзд',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Олена Коваль', 'autocomplete': 'name'}),
            'phone': forms.TextInput(attrs={'placeholder': '+380 00 000 00 00', 'autocomplete': 'tel', 'type': 'tel'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com', 'autocomplete': 'email'}),
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, room=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room
        # у моделі ці поля необов'язкові, а для бронювання — потрібні
        for name in ('name', 'phone', 'email'):
            self.fields[name].required = True

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get('check_in_date')
        check_out = cleaned.get('check_out_date')

        if check_in and check_in < date.today():
            self.add_error('check_in_date', 'Дата заїзду не може бути в минулому.')

        if check_in and check_out:
            if check_out <= check_in:
                self.add_error('check_out_date', 'Виїзд має бути пізніше за заїзд.')
            elif self.room is not None:
                overlap = Booking.objects.filter(
                    room=self.room,
                    check_in_date__lt=check_out,
                    check_out_date__gt=check_in,
                ).exists()
                if overlap:
                    raise forms.ValidationError('На ці дати номер уже заброньований. Оберіть інші дати.')

        return cleaned