from django import forms
from django.contrib.auth.models import User
from django.core import validators

class CommentForm(forms.Form):

    product_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )

    date = forms.DateField(
        widget=forms.HiddenInput(),
    )

    name = forms.CharField(
        widget=forms.TextInput(attrs={'id':"review_name", 'class':"form_input input_name", 'type':"text", 'name':"name", 'placeholder':"نام*", 'required':"required", 'data-error':"Name is required."}),
        validators=[
            validators.MaxLengthValidator(limit_value=20,
                                          message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(3, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    email = forms.CharField(
        widget=forms.TextInput(attrs={'id':"review_name", 'class':"form_input input_name", 'type':"email", 'name':"email", 'placeholder':"ایمیل*", 'required':"required", 'data-error':"your email is required."}),
        validators=[
            validators.EmailValidator('ایمیل وارد شده معتبر نمیباشد')
        ]
    )

    massage = forms.CharField(
        widget=forms.Textarea(attrs={'id':"review_message", 'class':"input_review", 'name':"message",  'placeholder':"نظر شما", 'rows':"4", 'required data-error':"Please, leave us a review."}),
    )

class CommentFormLogged(forms.Form):

    profile = forms.ImageField(
        widget=forms.HiddenInput()
    )
    
    product_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )

    date = forms.DateField(
        widget=forms.HiddenInput(),
    )

    name = forms.CharField(
        widget=forms.HiddenInput(),
        validators=[
            validators.MaxLengthValidator(limit_value=20,
                                          message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(3, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    email = forms.CharField(
        widget=forms.HiddenInput(),
        validators=[
            validators.EmailValidator('ایمیل وارد شده معتبر نمیباشد')
        ]   
    )

    rate = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'name':"kobs", 'id':"ratingStars"}),
    )

    massage = forms.CharField(
        widget=forms.Textarea(attrs={'id':"review_message", 'class':"input_review", 'name':"message",  'placeholder':"نظر شما", 'rows':"4", 'required data-error':"Please, leave us a review."}),
    )
