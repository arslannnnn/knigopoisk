from django import forms
from .models import Review


class BalanceTopUpForm(forms.Form):
    amount = forms.DecimalField(
        min_value=50,
        max_value=5000,
        decimal_places=2,
        max_digits=8,
        label='Сумма пополнения',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например, 300',
            'step': '50',
        })
    )
    card_number = forms.CharField(
        min_length=12,
        max_length=19,
        label='Номер карты',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1111 2222 3333 4444',
            'inputmode': 'numeric',
        })
    )
    cvv = forms.CharField(
        min_length=3,
        max_length=4,
        label='CVV',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '123',
            'inputmode': 'numeric',
        })
    )

    def clean_card_number(self):
        value = self.cleaned_data['card_number']
        digits = ''.join(char for char in value if char.isdigit())
        if len(digits) < 12:
            raise forms.ValidationError('Введите учебный номер карты: минимум 12 цифр.')
        return digits

    def clean_cvv(self):
        value = self.cleaned_data['cvv']
        if not value.isdigit():
            raise forms.ValidationError('CVV должен состоять только из цифр.')
        return value


class ShippingOrderForm(forms.Form):
    full_name = forms.CharField(
        max_length=200,
        label='Получатель',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван Иванов'})
    )
    phone = forms.CharField(
        max_length=30,
        label='Телефон',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 900 000-00-00'})
    )
    address = forms.CharField(
        label='Адрес доставки',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Город, улица, дом, квартира',
        })
    )
    comment = forms.CharField(
        required=False,
        label='Комментарий',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Например, оставить у двери',
        })
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Напишите ваш отзыв здесь...'
            })
        }
        labels = {
            'rating': 'Ваша оценка',
            'comment': 'Комментарий'
        }
