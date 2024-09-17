from django.shortcuts import render, redirect
from .forms import UserProfileForm, DepositForm, WithdrawForm, RegisterForm, KYCForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Notification, Offer, UserProfile, Wallet, KYC

def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form})

@login_required(login_url='/accounts/login/')
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notifications.html', {'notifications': user_notifications})

@login_required(login_url='/accounts/login/')
def wallet(request):
    user = request.user
    wallet, created = Wallet.objects.get_or_create(user=user)
    
    context = {
        'wallet': wallet,
    }
    return render(request, 'wallet.html', context)

@login_required(login_url='/accounts/login/')
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            request.user.wallet.deposit(amount)
            return redirect('wallet')
    else:
        form = DepositForm()
    return render(request, 'deposit.html', {'form': form})

@login_required(login_url='/accounts/login/')
def apply_offer(request, code):
    try:
        offer = Offer.objects.get(code=code, active=True)
        offer.apply(request.user.wallet)
        return redirect('wallet')
    except Offer.DoesNotExist:
        return redirect('wallet', error='Invalid code')
    
@login_required(login_url='/accounts/login/')
def withdraw(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            try:
                request.user.wallet.withdraw(amount)
                return redirect('wallet')
            except ValueError as e:
                return render(request, 'withdraw.html', {'form': form, 'error': str(e), 'wallet': request.user.wallet})
    else:
        form = WithdrawForm()
    return render(request, 'withdraw.html', {'form': form, 'wallet': request.user.wallet})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required(login_url='/accounts/login/')
def kyc_view(request):
    user_kyc, created = KYC.objects.get_or_create(user=request.user) 

    if request.method == 'POST':
        form = KYCForm(request.POST, request.FILES, instance=user_kyc)  
        if form.is_valid():
            form.save()
            return redirect('kyc')  
    else:
        form = KYCForm(instance=user_kyc)

    return render(request, 'kyc.html', {'form': form, 'kyc': user_kyc})
