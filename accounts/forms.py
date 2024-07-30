# from tkinter import N
from django import forms
from django.contrib.auth.models import User
from django.core import validators

class EditUserForm(forms.Form):

    profile = forms.ImageField()

    f_name = forms.CharField(
        widget=forms.TextInput(attrs={'id':"review_name", 'class':"form_input input_name", 'type':"text", 'name':"name", 'placeholder':"نام*", 'required':"required", 'data-error':"Name is required."}),
        label='نام',
        validators=[
            validators.MaxLengthValidator(limit_value=20,
                                          message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(4, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    l_name = forms.CharField(
        widget=forms.TextInput(attrs={'id':"review_name", 'class':"form_input input_name", 'type':"text", 'name':"name", 'placeholder':"نام خانوادگی*", 'required':"required", 'data-error':"Name is required."}),
        label='نام خانوادگی',
        validators=[
            validators.MaxLengthValidator(limit_value=20,
                                          message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(4, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    u_name = forms.CharField(
        widget=forms.TextInput(attrs={'id':"review_name", 'class':"form_input input_name", 'type':"text", 'name':"name", 'placeholder':"نام خانوادگی*", 'required':"required", 'data-error':"Name is required."}),
        label='نام خانوادگی',
        validators=[
            validators.MaxLengthValidator(limit_value=20,
                                          message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(4, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    ph_number = forms.CharField(
        widget=forms.TextInput(attrs={'id':"review_name", 'class':"form_input input_name", 'type':"text", 'name':"name", 'placeholder':"تلفن همراه*", 'required':"required", 'data-error':"Name is required."}),
        label='نام',
        validators=[
            validators.MaxLengthValidator(limit_value=20,
                                          message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(8, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    email = forms.CharField(
        widget=forms.TextInput(attrs={'id':"review_name", 'class':"form_input input_name", 'type':"text", 'name':"name", 'placeholder':"ایمیل*", 'required':"required", 'data-error':"Name is required."}),
        label='نام',
        validators=[
            validators.EmailValidator('ایمیل وارد شده معتبر نمیباشد')
        ]
    )

    address = forms.CharField(
        widget=forms.TextInput(attrs={'id':"review_name", 'class':"form_input input_name", 'type':"text", 'name':"name", 'placeholder':"آدرس*", 'required':"required", 'data-error':"Name is required."}),
        label='آدرس'
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EditUserForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        userid = self.request.user.id
        email = self.cleaned_data.get('email')
        other_user = User.objects.filter(email=email).first()
        if other_user is not None and not other_user.id==userid:
            raise forms.ValidationError('ایمیل وارد شده تکراری میباشد')

        if len(email) > 35:
            raise forms.ValidationError('تعداد کاراکترهای ایمیل باید کمتر از 35 باشد')

        return email

    def clean_user_name(self):
        userid = self.request.user.id
        user_name = self.cleaned_data.get('user_name')
        other_user = User.objects.filter(username=user_name).first()

        if other_user is not None and not other_user.id==userid:
            raise forms.ValidationError('این کاربر قبلا ثبت نام کرده است')

        return user_name




class LoginForm(forms.Form):
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"text", 'name':"name", 'placeholder':"نام کاربری", 'required':"required", 'data-error':"Name is required."}),
        label='نام کاربری'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"password",'name':"name", 'placeholder':"رمز عبور", 'required':"required", 'data-error':"Name is required."}),
        label='کلمه ی عبور'
    )

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        is_exists_user = User.objects.filter(username=user_name).exists()
        if not is_exists_user:
            raise forms.ValidationError('کاربری با مشخصات وارد شده ثبت نام نکرده است')

        return user_name


class RegisterForm(forms.Form):
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"text", 'name':"name", 'placeholder':"نام کاربری", 'required':"required", 'data-error':"Name is required."}),
        label='نام کاربری',
        validators=[
            validators.MaxLengthValidator(limit_value=20,
                                          message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(8, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    email = forms.CharField(
        widget=forms.TextInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"text", 'name':"name", 'placeholder':"ایمیل", 'required':"required", 'data-error':"Name is required."}),
        label='ایمیل',
        validators=[
            validators.EmailValidator('ایمیل وارد شده معتبر نمیباشد')
        ]
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"password",'name':"name", 'placeholder':"رمز عبور", 'required':"required", 'data-error':"Name is required."}),
        label='کلمه ی عبور'
    )

    re_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"password", 'name':"name", 'placeholder':"تکرار رمز عبور", 'required':"required", 'data-error':"Name is required."}),
        label='تکرار کلمه ی عبور'
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exists_user_by_email = User.objects.filter(email=email).exists()
        if is_exists_user_by_email:
            raise forms.ValidationError('ایمیل وارد شده تکراری میباشد')

        if len(email) > 20:
            raise forms.ValidationError('تعداد کاراکترهای ایمیل باید کمتر از 20 باشد')

        return email

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        is_exists_user_by_username = User.objects.filter(username=user_name).exists()

        if is_exists_user_by_username:
            raise forms.ValidationError('این کاربر قبلا ثبت نام کرده است')

        return user_name

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        print(password)
        print(re_password)

        if password != re_password:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')

        return password


class ResetPasswordForm(forms.Form):

    user_name = forms.CharField(
        widget=forms.TextInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"text", 'name':"name", 'placeholder':"نام کاربری", 'required':"required", 'data-error':"Name is required."}),
        label='نام کاربری'
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"text", 'name':"name", 'placeholder':"شماره همراه", 'required':"required", 'data-error':"Name is required."}),
        label='شماره همراه'
    )

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        is_exists_user = User.objects.filter(username=user_name).exists()
        if not is_exists_user:
            raise forms.ValidationError('نام کاربری اشتباه وارد شده')
        return user_name

class ResetPasswordConfirmForm(forms.Form):
    
    code = forms.CharField(
        widget=forms.TextInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"text", 'name':"name", 'placeholder':"کد ارسال شده", 'required':"required", 'data-error':"Name is required."}),
        label='کد ارسال شده'
    )

class ResetPasswordCompleteForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"password",'name':"name", 'placeholder':"رمز عبور", 'required':"required", 'data-error':"Name is required."}),
        label='کلمه ی عبور',
        validators=[
            validators.MaxLengthValidator(limit_value=20,
                                          message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(8, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    re_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id':"input_name", 'class':"form_input input_name input_ph", 'type':"password", 'name':"name", 'placeholder':"تکرار رمز عبور", 'required':"required", 'data-error':"Name is required."}),
        label='تکرار کلمه ی عبور'
    )

    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')
        return password