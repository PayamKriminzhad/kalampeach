from django import forms
from django.contrib.auth.models import User
from django.core import validators

class UserNewOrderForm(forms.Form):
    product_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )

    count = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'id':"kobs_tracker", 'type':"hidden"}),
        initial=1
    )

class UserNewOrderFormForComponent(forms.Form):
    product_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )

    count = forms.IntegerField(
        widget=forms.HiddenInput(),
    )


class UserLikeForm(forms.Form):
    product = forms.IntegerField(
        widget=forms.HiddenInput(),
    )


class OrderConfirmForm(forms.Form):
    cellphone = forms.CharField(
        widget=forms.TextInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"text", 'name':"name", 'placeholder':"تلفن همراه", 'required':"required", 'data-error':"Name is required."}),
        label='نام کاربری',
        validators=[
            validators.MaxLengthValidator(limit_value=20,
                                          message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(8, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    homephone = forms.CharField(
        widget=forms.TextInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"text", 'name':"name", 'placeholder':"تلفن ثابت", 'required':"required", 'data-error':"Name is required."}),
        label='ایمیل',
    )

    address = forms.CharField(
        widget=forms.TextInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"text", 'name':"name", 'placeholder':"آدرس", 'required':"required", 'data-error':"Name is required."}),
        label='ایمیل',
    )
