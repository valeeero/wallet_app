from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, KYC


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']

class KYCForm(forms.ModelForm):
    class Meta:
        model = KYC
        fields = ['document'] 

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)


class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] 

   
    bio = forms.CharField(widget=forms.Textarea, required=False)
    avatar = forms.ImageField(required=False)

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
            
            UserProfile.objects.create(
                user=user,
                bio=self.cleaned_data.get('bio'),
                avatar=self.cleaned_data.get('avatar')
            )
        return user


