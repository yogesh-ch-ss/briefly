from django import forms
from .models import CATEGORY_CHOICES, BrieflyUser, Category, UserCategory
from .models import COUNTRY_CHOICES


class BrieflyUserSignupForm(forms.ModelForm):
    class Meta:
        model = BrieflyUser
        fields = ['username', 'email', 'password', 'country']
        widgets = {
            'password': forms.PasswordInput(),
            'country': forms.Select(choices=COUNTRY_CHOICES),
        }
        widgets = {
            'password': forms.PasswordInput(),
        }
        help_texts = {
            'username': None,
        }

class BrieflyUserLoginForm(forms.ModelForm):
    class Meta:
        model = BrieflyUser
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

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