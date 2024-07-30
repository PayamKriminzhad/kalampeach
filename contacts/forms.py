from django import forms
from django.contrib.auth.models import User
from django.core import validators


class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"text", 'name':"name", 'placeholder':"نام", 'required':"required", 'data-error':"Name is required."}),
        label='نام کاربری',
        validators=[
            validators.MaxLengthValidator(limit_value=20, message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(4, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    email = forms.CharField(
        widget=forms.TextInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"text", 'name':"name", 'placeholder':"ایمیل", 'required':"required", 'data-error':"Name is required."}),
        label='ایمیل',
        validators=[
            validators.EmailValidator('ایمیل وارد شده معتبر نمیباشد')
        ]
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"text",'name':"name", 'placeholder':"موضوع", 'required':"required", 'data-error':"Name is required."}),
        label='کلمه ی عبور'
    )

    massage = forms.CharField(
        widget=forms.Textarea(attrs={'id':"input_message", 'class':"input_ph input_message", 'name':"message", 'placeholder':"پیام", 'rows':"3", 'required data-error':"Please, write us a message."}),
        label='تکرار کلمه ی عبور'
    )

