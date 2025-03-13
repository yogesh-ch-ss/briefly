from django import forms
from .models import CATEGORY_CHOICES, BrieflyUser, Category, UserCategory
from .models import COUNTRY_CHOICES
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
            'country': 'us',
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
                UserCategory.objects.create(User=user, Category=category)
        return user

class BrieflyUserProfileForm(forms.ModelForm):
    categories = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True  # Make the field required
    )

    class Meta:
        model = BrieflyUser
        fields = ['username', 'email', 'country', 'categories']
        widgets = {
            'country': forms.Select(choices=COUNTRY_CHOICES),
        }
        initial = {
            'country': 'us',
        }
        help_texts = {
            'username': None,
        }

    def clean(self):
        cleaned_data = super().clean()
        selected_categories = cleaned_data.get('categories')
        if not selected_categories or len(selected_categories) < 1:
            self.add_error('categories', "You must select at least one category")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        if user:
            user_categories = UserCategory.objects.filter(User=user).values_list('Category__CategoryName', flat=True)
            self.fields['categories'].initial = list(user_categories)
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['country'].initial = user.country
            self.fields['username'].required = True
            self.fields['email'].required = True
            self.fields['country'].required = True
            self.fields['categories'].required = True


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
        
class QuestionForm(forms.Form):
    email = forms.EmailField(required=True)
    question = forms.CharField(widget=forms.Textarea, required=True)
    class Meta:
        help_texts = {
            'email': "Enter your email address.",
            'question': "Enter your question.",
        }
    widgets = {
        'question': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
    }