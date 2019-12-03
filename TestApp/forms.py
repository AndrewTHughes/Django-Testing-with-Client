from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class FriendForm(forms.Form):
    username_a = forms.CharField(label='Username A:')
    username_b = forms.CharField(label='Username B:')

    def clean(self):
        cleaned_data = super().clean()
        username_a = cleaned_data.get('username_a')
        username_b = cleaned_data.get('username_b')
        if username_a and username_b:
            users_a = User.objects.filter(username=username_a)
            users_b = User.objects.filter(username=username_b)
            if len(users_a) != 1:
                raise forms.ValidationError('Username A is faulty')
            if len(users_b) != 1:
                raise forms.ValidationError('Username B is faulty')
            if username_a == username_b:
                raise forms.ValidationError('Usernames must be different')
        return cleaned_data
