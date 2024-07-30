from datetime import datetime
from random import randint
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import EditUserForm, LoginForm, RegisterForm, EditUserForm, ResetPasswordForm, ResetPasswordConfirmForm, ResetPasswordCompleteForm
from .models import Dashbord, Token
from orders.views import payamak



def Login(request):

    if request.user.is_authenticated:
        return redirect('/')
    
    form = LoginForm(request.POST or None)
            
    if form.is_valid():
        username=form.cleaned_data.get('user_name')
        password=form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, 'شما وارد شدید')
            return redirect('/products')
        else:
            form.add_error('user_name', 'نام کاربری یا رمز عبور درست وارد نشده')

        
    context={
        'form':form,
    }

    return render(request, 'login.html', context)


def Register(request):

    if request.user.is_authenticated:
        return redirect('/')
    
    form = RegisterForm(request.POST or None)

    if form.is_valid():

        username=form.cleaned_data.get('user_name')
        email=form.cleaned_data.get('email')
        password=form.cleaned_data.get('password')

        user = User.objects.create_user(username=username, email=email, password=password)
        print(user)
        Dashbord.objects.create(owner_id=user.id, u_name=username)
        messages.success(request, 'حساب شما با موفقیت ثبت شد')

        return redirect('/login')

    context={
        'form':form,
    }

    return render(request, 'register.html', context)


def Logout(request):
    logout(request)
    return redirect('/login')



@login_required(login_url='/login')
def UserMainPage(request):

    user_id = request.user.id
    user = User.objects.get(id=user_id)
    dashbord = Dashbord.objects.filter(owner_id=user_id).first()
    Liked_product = dashbord.liked.all()

    if user is None:
        return redirect('/404')
    if dashbord is None:
        return redirect('/404')

    context = {
        'dashbord' : dashbord
    }        

    return render(request, 'user_dashbord.html', context)



@login_required(login_url='/login')
def EditUserProfile(request):

    user_id = request.user.id
    user = User.objects.get(id=user_id)
    dashbord = Dashbord.objects.get(owner_id=user_id)

    if user is None:
        return redirect('/404')

    form = EditUserForm(request.POST or None, request.FILES or None, request=request, initial={'profile': dashbord.profile,'f_name': user.first_name, 'l_name': user.last_name, 'u_name': user.username, 'ph_number': dashbord.ph_number, 'email': user.email, 'address': dashbord.address})
    
    if form.is_valid():
        profile = form.cleaned_data.get('profile')
        fname = form.cleaned_data.get('f_name')
        lname = form.cleaned_data.get('l_name')
        uname = form.cleaned_data.get('u_name')
        phonenum = form.cleaned_data.get('ph_number')
        email = form.cleaned_data.get('email')
        address = form.cleaned_data.get('address')

        user.first_name = fname
        user.last_name = lname
        user.username = uname
        user.email = email
        user.save()
        print(request.FILES)
        dashbord.profile = profile
        dashbord.f_name = fname
        dashbord.l_name = lname
        dashbord.u_name = uname
        dashbord.email = email
        dashbord.ph_number = phonenum
        dashbord.address = address
        dashbord.save()

        messages.success(request, 'اطلاعات با موفقیت ویرایش شد')
        return redirect('/user')

    context = {
        'form' : form,
    }        

    return render(request, 'user_edit.html', context)


def reset_password(request):
    
    if request.user.is_authenticated:
        return redirect('/')

    form = ResetPasswordForm(request.POST or None)

    if form.is_valid():
        user_name=form.cleaned_data.get('user_name')
        phone_number=form.cleaned_data.get('phone_number')
        user = User.objects.get(username=user_name)
        dashbord = Dashbord.objects.filter(owner_id=user.id).first()
        if dashbord.ph_number == phone_number:
            user_tokens : Token = Token.objects.filter(owner_id=user.id)
            for user_token in user_tokens:
                user_token.expire()
                if user_token.expired==False:
                    return messages.error(request, 'کد برای شما ارسال شده، در صورت عدم دریافت کد پس از چند دقیقه دوباره تلاش کنید')
            token = Token.objects.create(owner_id=user.id, number=randint(10000, 99999), time=datetime.now())
            payamak(dashbord.ph_number, token.number)
            messages.success(request, 'پیامک شما ارسال شد')
            return redirect(f'/reset-password/{token.id}')
        else:
            form.add_error('phone_number', 'شماره تلفن وارد شده با شماره تلفن حساب شما متفاوت است')

    context={
        'form':form,
    }

    return render(request, 'reset_password.html', context)

def reset_password_confirm(request, *args, **kwargs):
    
    if request.user.is_authenticated:
        return redirect('/')

    form = ResetPasswordConfirmForm(request.POST or None)
    token_id = kwargs['tokenid']
    tokens = Token.objects.get_queryset().filter(id = token_id)
    if tokens.count() != 1:
        return redirect('/404')

    token: Token = Token.objects.get(id=token_id)
    token.expire()

    if token.expired == True:
        messages.error(request, 'کد شما باطل شده لطفا دوباره درخواست دهید')
        return redirect('/reset-password')

    if form.is_valid():
        code=form.cleaned_data.get('code')
        if code == token.number:
            messages.success(request, 'گذرواژه جدید خود را وارد کنید')
            return redirect(f'/reset-password/{token_id}/{code}')
        else:
            form.add_error('code', 'کد وارد شده درست نمی باشد')

    context={
        'form':form,
    }
    return render(request, 'reset_password_confirm.html', context)

def reset_password_complete(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('/')

    form = ResetPasswordCompleteForm(request.POST or None)

    token_id = kwargs['tokenid']
    token = Token.objects.get(id=token_id)
    code = kwargs['code']
    user = token.owner
    if token.number == code:
        if form.is_valid():
            password=form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            messages.success(request, 'گذرواژه شما با موفقیت تغییر کرد')
            return redirect(f'/login')

        context={
            'form':form,
        }
        return render(request, 'reset_password_complete.html', context)
    else:
        messages.error(request, 'توکن شما نامعتبر یا باطل است')
        return redirect('/reset-password')