from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from django.conf import settings
from django_authopenid.models import UserAssociation
try:
    from openid.yadis import xri
except ImportError:
    from yadis import xri
import re
from registration.models import RegistrationProfile
attrs_dict = { 'class': 'required' }
#class OpenidSigninForm(forms.Form):
#    """ signin form """
#    openid_url = forms.CharField(max_length=255, 
#            widget=forms.widgets.TextInput(attrs={'class': 'required openid'}),
#            label=_("OpenID URL"))
#    
#    def clean_openid_url(self):
#        """ test if openid is accepted """
#        if 'openid_url' in self.cleaned_data:
#            openid_url = self.cleaned_data['openid_url']
#            if xri.identifierScheme(openid_url) == 'XRI' and getattr(
#                settings, 'OPENID_DISALLOW_INAMES', False
#                ):
#                raise forms.ValidationError(_('i-names are not supported'))
#            return self.cleaned_data['openid_url']
#
#attrs_dict = { 'class': 'required login' }
#username_re = re.compile(r'^\w+$')
#
#class OpenidRegisterForm(forms.Form):
#    username = forms.CharField(max_length=30, 
#            widget=forms.widgets.TextInput(attrs=attrs_dict))
#    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, 
#        maxlength=200)), label=_('Email address'))
#    
#    def __init__(self, *args, **kwargs):
#        super(OpenidRegisterForm, self).__init__(*args, **kwargs)
#        self.user = None
#    
#    def clean_username(self):
#        if 'username' in self.cleaned_data:
#            if not username_re.search(self.cleaned_data['username']):
#                raise forms.ValidationError(_("Usernames can only contain \
#                    letters, numbers and underscores"))
#            try:
#                user = User.objects.get(
#                        username__exact = self.cleaned_data['username']
#                )
#            except User.DoesNotExist:
#                return self.cleaned_data['username']
#            except User.MultipleObjectsReturned:
#                raise forms.ValidationError(u'There is already more than one \
#                    account registered with that username. Please try \
#                    another.')
#            self.user = user
#            raise forms.ValidationError(_("This username is already \
#                taken. Please choose another."))
#            
#    def clean_email(self):
#        if 'email' in self.cleaned_data:
#            try:
#                user = User.objects.get(email = self.cleaned_data['email'])
#            except User.DoesNotExist:
#                return self.cleaned_data['email']
#            except User.MultipleObjectsReturned:
#                raise forms.ValidationError(u'There is already more than one \
#                    account registered with that e-mail address. Please try \
#                    another.')
#            raise forms.ValidationError(_("This email is already \
#                registered in our database. Please choose another."))
#
#class AssociateOpenID(forms.Form):
#    """ new openid association form """
#    openid_url = forms.CharField(max_length=255, 
#            widget=forms.widgets.TextInput(attrs={'class': 'required openid'}),
#            label=_("OpenID URL"))
#
#    def __init__(self, user, *args, **kwargs):
#        super(AssociateOpenID, self).__init__(*args, **kwargs)
#        self.user = user
#            
#    def clean_openid_url(self):
#        """ test if openid is accepted """
#        if 'openid_url' in self.cleaned_data:
#            openid_url = self.cleaned_data['openid_url']
#            if xri.identifierScheme(openid_url) == 'XRI' and getattr(
#                settings, 'OPENID_DISALLOW_INAMES', False
#                ):
#                raise forms.ValidationError(_('i-names are not supported'))
#                
#            try:
#                rel = UserAssociation.objects.get(openid_url__exact=openid_url)
#            except UserAssociation.DoesNotExist:
#                return self.cleaned_data['openid_url']
#            
#            if rel.user != self.user:
#                raise forms.ValidationError(_("This openid is already \
#                    registered in our database by another account. Please choose another."))
#                    
#            raise forms.ValidationError(_("You already associated this openid to your account."))
#
#class OpenidDissociateForm(OpenidSigninForm):
#    """ form used to dissociate an openid. """
#    openid_url = forms.CharField(max_length=255, widget=forms.widgets.HiddenInput())

class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should either preserve the base ``save()`` or implement
    a ``save()`` which accepts the ``profile_callback`` keyword
    argument and passes it through to
    ``RegistrationProfile.objects.create_inactive_user()``.
    
    """
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_(u'Username'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_(u'Email address'))
    first_name=forms.CharField(max_length=30,label=_(u'First Name'))
    last_name=forms.CharField(max_length=30,label=_(u'Last Name'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'Password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'Password (again)'))
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['Username'])
        except User.DoesNotExist:
            return self.cleaned_data['Username']
        raise forms.ValidationError(_(u'This username is already taken. Please choose another.'))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data
    
    def save(self, profile_callback=None):
        """
        Create the new ``User`` and ``RegistrationProfile``, and
        returns the ``User``.
        
        This is essentially a light wrapper around
        ``RegistrationProfile.objects.create_inactive_user()``,
        feeding it the form data and a profile callback (see the
        documentation on ``create_inactive_user()`` for details) if
        supplied.
        
        """
        
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['Username'],
                                                                    first_name=self.cleaned_data['first_name'],
                                                                    last_name=self.cleaned_data['last_name'],
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['Email'],
                                                                    profile_callback=profile_callback)
        return new_user

####################################
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    
class DetailsForm(forms.Form):
    first_name=forms.CharField()
    last_name=forms.CharField()
    email=forms.EmailField()
    
class RegisterForm(forms.Form):
    username=forms.CharField()
#    headpic=forms.ImageField()
    first_name=forms.CharField()
    last_name=forms.CharField()
    email=forms.EmailField()
    password1=forms.CharField(widget=forms.PasswordInput,label="Password")
    password2=forms.CharField(widget=forms.PasswordInput,label="Confirm Password")
    
    def clean_username(self):
        username=self.cleaned_data['username']
        if not re.match("^[a-zA-Z_]*$", username):
            raise forms.ValidationError("Username can only contain characters and Underscore ( _ )")
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("A user with that username already exists")
    
    def clean_password2(self):
        password1=self.cleaned_data.get('password1','')
        password2=self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError("The two password fields must match")
        return password2
class ChangePassForm(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput)
    new_password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    
    def clean_confirm_password(self):
        password1=self.cleaned_data.get('new_password','')
        password2=self.cleaned_data['confirm_password']
        if password1 !=password2:
            raise forms.ValidationError("New password and Confirm Password fields do not match")
        return password2
#    
#    def clean_old_password(self):
#        password=self.cleaned_data['old_password']
#        try:
#            User.objects.get()
        
    