from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('userid','username')

    def save(self, commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        
        return user

class UserChangeForm(forms.ModelForm):
    # 관리자 권한
    password=ReadOnlyPasswordHashField()

    class Meta:
        model=User
        fields=('userid','username','password','img','bio','is_active','is_admin')
    
    def clean_password(self):
        return self.initial["password"]


class CustomUserChangeForm(UserChangeForm):
    # 일반 사용자 권한
    class Meta:
        model=get_user_model() # 현재 활성화된 사용자 모델을 반환
        fields=('username','img','bio')
