from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import ContactForm
from .models import Contact
from dynamics.models import SiteSetting


def contact_us(request):

    form = ContactForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        title = form.cleaned_data.get('title')
        massage = form.cleaned_data.get('massage')

        Contact.objects.create(name=name, email=email, title=title, massage=massage)
        messages.success(request, 'پیام شما با موفقیت ارسال شد')

    setting = SiteSetting.objects.first()

    context={
        'form': form,
        'setting': setting
    }

    return render(request, 'contactus.html', context)