from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class SignupForm(forms.Form):
    username         = forms.CharField(error_messages={'required': u'Please enter a username', 'invalid': u'Please enter a valid username'})
    email            = forms.EmailField(error_messages={'required': u'Please enter your email address', 'invalid': u'Email is invalid'})
    password         = forms.CharField(error_messages={'required': u'Please enter a password', 'invalid': u'Password should be atleast 8 characters long'})
    confirm_password = forms.CharField(error_messages={'required': u'Please confirm your password', 'invalid': u'Password mismatch'})

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'%s already exists' % username)
    
    def clean_password(self):
        passwd = self.cleaned_data['password']

        if len(passwd) < 8:
            raise forms.ValidationError(u'Password should be atleast 8 characters long')

        return passwd

    def clean_confirm_password(self):
        passwd = self.cleaned_data['password']
        con_passwd = self.cleaned_data['confirm_password']

        if passwd != con_passwd:
            raise forms.ValidationError(u'Password mismatch')

        return con_passwd

    def authenticate(self, request):
        if self.is_valid():
            user = User.objects.create_user(username=self.cleaned_data['username'],
                                            email=self.cleaned_data['email'],
                                            password=self.cleaned_data['password'])
            if user:
                user = authenticate(username=user.username, password=user.password)  # This is necessary for setting flags
                if user and user.is_active:
                    login(request, user)

            return user
        else:
            return None


class LoginForm(forms.Form):
    username = forms.CharField(error_messages={'required': u'Please enter a username', 'invalid': u'Please enter a valid username'})
    password = forms.CharField(error_messages={'required': u'Please enter a password', 'invalid': u'Password should be atleast 8 characters long'})

    def authenticate(self, request):
        user = None
        if self.is_valid():
            user = authenticate(
                                    username=self.cleaned_data['username'], 
                                    password=self.cleaned_data['password']
                               )

            if user and user.is_active:
                login(user, request)
       
        return user


class UserDetailsForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    date_of_birth = forms.DateField(required=False)
    image = forms.ImageField(required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return username
            raise forms.ValidationError(u'%s already exists' % username)

    def save(self, profile_instance):
        user_changed = False
        profile_changed = False
        if profile_instance:
            # Update username and email
            if self.cleaned_data['username']:
                profile_instance.user.username = self.cleaned_data['username']
                user_changed = True
            if self.cleaned_data['email']:
                profile_instance.user.email = self.cleaned_data['email']
                user_changed = True
            
            # Save changes
            if user_changed:
                profile_instance.user.save()
                profile_changed = True

            # Update DOB. Image is handled seperately
            if self.cleaned_data['date_of_birth']:
                profile_instance.date_of_birth = self.cleaned_data['date_of_birth']
                profile_changed = True

            if profile_changed:
                profile_instance.save()


