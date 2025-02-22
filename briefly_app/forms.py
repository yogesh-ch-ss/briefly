from django import forms
from .models import CATEGORY_CHOICES, BrieflyUser, Category, UserCategory
from .models import COUNTRY_CHOICES


class CategoryForm(forms.Form):
    categories = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )

    def save(self, user, commit=True):
        selected_categories = self.cleaned_data['categories']
        UserCategory.objects.filter(UserID=user).delete()
        for category_name in selected_categories:
            category = Category.objects.get(CategoryName=category_name)
            UserCategory.objects.create(UserID=user, CategoryID=category)

class BrieflyUserSignupForm(forms.ModelForm):
    password_confirmation = forms.CharField(widget=forms.PasswordInput())
    categories = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = BrieflyUser
        fields = ['username', 'email', 'password', 'password_confirmation', 'country', 'categories']
        widgets = {
            'password': forms.PasswordInput(),
            'country': forms.Select(choices=COUNTRY_CHOICES),
        }
        initial = {
            'country': 'YourDefaultCountryCode',  # Replace 'YourDefaultCountryCode' with the desired default country code
        }
        help_texts = {
            'username': None,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            selected_categories = self.cleaned_data['categories']
            for category_name in selected_categories:
                category, created = Category.objects.get_or_create(CategoryName=category_name)
                UserCategory.objects.create(UserID=user, CategoryID=category)
        return user

class BrieflyUserProfileForm(forms.ModelForm):
    categories = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = BrieflyUser
        fields = ['username', 'email', 'country', 'categories']
        widgets = {
            'country': forms.Select(choices=COUNTRY_CHOICES),
        }
        help_texts = {
            'username': None,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        if user:
            user_categories = UserCategory.objects.filter(UserID=user).values_list('CategoryID__CategoryName', flat=True)
            self.fields['categories'].initial = list(user_categories)
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['country'].initial = user.country
            
    
class BrieflyUserLoginForm(forms.ModelForm):
    class Meta:
        model = BrieflyUser
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        help_texts = {
            'username': None,
        }
        
