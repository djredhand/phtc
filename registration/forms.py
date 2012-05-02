"""
Forms and validation code for user registration.

"""


from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from django.db.models import signals

from registration.models import RegistrationProfile


# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = { 'class': 'required' }


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
                                label=_(u'username'))
    sex = forms.CharField(max_length=6,
                          widget=forms.Select(choices=[('Please Select','Please Select'),
                                                       ('male','Male'),
                                                       ('female','Female')])
                          )
    age = forms.CharField(widget=forms.Select(choices=[('Please Select','Please Select'),
                                                       ('Under 20','Under 20 Years'),
                                                       ('20-29','20-29 Years'),
                                                       ('30-39','30-39 Years'),
                                                       ('40-49','40-49 Years'),
                                                       ('50-59','50-59 Years'),
                                                       ('60-69','60-69 Years'),
                                                       ('70 or older','70 Years or Older'),
                                                       ('Prefer not to answer','I prefer not to answer')])
                          )
    origin = forms.CharField(widget=forms.Select(choices=[('Please Select','Please Select'),
                                                       ('yes','Yes'),
                                                       ('no','No'),
                                                       ('Prefer not to answer','I prefer not to answer')])
                          )
    ethnicity = forms.CharField(widget=forms.Select(choices=[('Please Select','Please Select'),
                                                       ('American Indian or Alaskan Native','American Indian or Alaskan Native'),
                                                       ('Asian (including Chinese, Filipino, Japanese, Korean, Asian Indian, or Thai)','Asian (including Chinese, Filipino, Japanese, Korean, Asian Indian, or Thai)'),
                                                       ('Asian (other)','Asian (other)'),
                                                       ('Black or African-American','Black or African-American'),
                                                       ('Native Hawaiian or Pacific Islander','Native Hawaiian or Pacific Islander'),
                                                       ('White','White'),
                                                       ('More Than One Race','More Than One Race'),
                                                       ('Other','Other'),
                                                       ('Prefer not to answer','I prefer not to answer')])
                          )
    disadvantaged = forms.CharField(widget=forms.Select(choices=[('Please Select','Please Select'),
                                                       ('yes','Yes'),
                                                       ('no','No'),
                                                       ('Prefer not to answer','I prefer not to answer')])
                          )
    employment_location = forms.CharField(widget=forms.Select(choices=[('Please Select','Please Select'),
                                                       ('Academia','Academia'),
                                                       ('Federal government','Federal government'),
                                                       ('State government','State government'),
                                                       ('City/County government','City/County government'),
                                                       ('Indian Health/Tribal government','Indian Health/Tribal government'),
                                                       ('Hospitals','Hospitals'),
                                                       ('Community-based Organizations/Non-profit','Community-based Organizations/Non-profit'),
                                                       ('Private Industry','Private Industry'),
                                                       ('Other','Other')])
                          )
    position = forms.CharField(widget=forms.Select(choices=[('Please Select','Please Select'),
                                                       ('Biostatistician','Biostatistician'),
                                                       ('Community health worker','Community health worker'),
                                                       ('Consumer','Consumer'),
                                                       ('Dentist','Dentist'),
                                                       ('Elected government official','Elected government official'),
                                                       ('Emergency management/bioterrorism preparedness','Emergency management/bioterrorism preparedness'),
                                                       ('Environmental health/sanitarian','Environmental health/sanitarian'),
                                                       ('Epidemiology','Epidemiology'),
                                                       ('Health administration','Health administration'),
                                                       ('Health information systems/data analyst','Health information systems/data analyst'),
                                                       ('Health promotion/education','Health promotion/education'),
                                                       ('Home health aide/medical assistant','Home health aide/medical assistant'),
                                                       ('Laboratory sciences','Laboratory sciences'),
                                                       ('Law enforcement','Law enforcement'),
                                                       ('Mental health/substance abuse','Mental health/substance abuse'),
                                                       ('Nurse','Nurse'),
                                                       ('Nutritionist/dietician','Nutritionist/dietician'),
                                                       ('Pharmacist','Pharmacist'),
                                                       ('Physician','Physician'),
                                                       ('Physician assistant','Physician assistant'),
                                                       ('Psychologist','Psychologist'),
                                                       ('Public health law','Public health law'),
                                                       ('Public health policy','Public health policy'),
                                                       ('Social worker','Social worker'),
                                                       ('Support staff member','Support staff member (e.g. administrative assistant, clerk)'),
                                                       ('Teacher/faculty member','Teacher/faculty member'),
                                                       ('Veterinarian','Veterinarian'),
                                                       ('Other','Other')])
                          )
    
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_(u'email address'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'password (again)'))
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
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
    
    def save(self, profile_callback = None):
        """
        Create the new ``User`` and ``RegistrationProfile``, and
        returns the ``User``.
        
        This is essentially a light wrapper around
        ``RegistrationProfile.objects.create_inactive_user()``,
        feeding it the form data and a profile callback (see the
        documentation on ``create_inactive_user()`` for details) if
        supplied.
        
        """
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
                                                                    sex=self.cleaned_data['sex'],
                                                                    age=self.cleaned_data['age'],                                                                    
                                                                    origin=self.cleaned_data['origin'],
                                                                    ethnicity=self.cleaned_data['ethnicity'],
                                                                    disadvantaged=self.cleaned_data['disadvantaged'],
                                                                    employment_location=self.cleaned_data['employment_location'],
                                                                    position=self.cleaned_data['position'],
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['email'],
                                                                    profile_callback=profile_callback)
        
        # Extending the user model with UserProfile
        new_profile = UserProfile(user = new_user, 
                                  sex=self.cleaned_data['sex'],
                                  age=self.cleaned_data['age'],
                                  origin=self.cleaned_data['origin'],
                                  ethnicity=self.cleaned_data['ethnicity'],
                                  disadvantaged=self.cleaned_data['disadvantaged'],
                                  employment_location=self.cleaned_data['employment_location'],
                                  position=self.cleaned_data['position'])
        new_profile.save()
        return new_user
        
class RegistrationFormTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.
    
    """
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={ 'required': u"You must agree to the terms to register" })


class RegistrationFormUniqueEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.
    
    """
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email']


class RegistrationFormNoFreeEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which disallows registration with
    email addresses from popular free webmail services; moderately
    useful for preventing automated spam registrations.
    
    To change the list of banned domains, subclass this form and
    override the attribute ``bad_domains``.
    
    """
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com']
    
    def clean_email(self):
        """
        Check the supplied email address against a list of known free
        webmail domains.
        
        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_(u'Registration using free email addresses is prohibited. Please supply a different email address.'))
        return self.cleaned_data['email']
