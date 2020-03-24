from django import forms 
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class':'form-control form-control-lg',
                'placeholder':'enter email id'
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control form-control-lg',
                'placeholder':'enter password'
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control form-control-lg',
                'placeholder':'confirm password'
            }
        )
    )
    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self,*args,**kwargs):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email__contains = email)
        if qs.exists():
            raise forms.ValidationError('Email has already been registerd')
        else:
            return email

    def clean_password1(self,*args,**kwargs):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords did not match')
        else:
            return password2

    def save(self,commit=True):
        user = super(RegisterForm,self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class':'form-control form-control-lg',
                'placeholder':'enter your email'
            }
        )
    )

    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'class':'form-control form-control-lg',
                'placeholder':'enter your password'
            }
        )
    )

    def clean(self,*args,**kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        qs = User.objects.filter(email__iexact=email)
        if not qs.exists():
            raise forms.ValidationError('User does not exists ')
        user_obj = qs.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError('Invalid Credentials')
        self.cleaned_data['user_obj'] = user_obj
        return super(LoginForm,self).clean(*args,**kwargs)
