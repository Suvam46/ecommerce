from django.contrib.auth import password_validation
from .models import (
    CustomUser,
    CustomUserManager,
    UserProfile,
    SiteSettings,
    Comment,
    PricingPlan,
)
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from tinymce.widgets import TinyMCE


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Enter your Email"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your Password"}),
    )


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "name",
            "phone",
            "country",
            "image",
            "state",
            "city",
            "newsletter",
            "message_notification",
            "listing_alerts",
        ]


from django import forms
from .models import Banner


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ["image", "alt_text"]


from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "image", "slug"]


from django import forms
from .models import AboutUs


class AboutUsForm(forms.ModelForm):
    introduction = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 30}))

    class Meta:
        model = AboutUs
        fields = ["introduction", "image"]


from django import forms
from .models import TeamMember
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ["name", "position", "image"]

    def __init__(self, *args, **kwargs):
        super(TeamMemberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Save"))


class SiteSettingsForm(forms.ModelForm):
    address = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 30}))
    iframe_map_location = forms.CharField(
        widget=TinyMCE(attrs={"cols": 80, "rows": 30})
    )
    terms_and_conditions = forms.CharField(
        widget=TinyMCE(attrs={"cols": 80, "rows": 30})
    )

    class Meta:
        model = SiteSettings
        fields = [
            "cup_of_coffee",
            "happy_users",
            "ads_posts",
            "total_users",
            "address",
            "email",
            "phone_number",
            "facebook_link",
            "instagram_link",
            "youtube_link",
            "linkedin_link",
            "iframe_map_location",
            "terms_and_conditions",
        ]

    def __init__(self, *args, **kwargs):
        super(SiteSettingsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Save"))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Write your comment here..."}
            ),
        }


from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 30}))

    class Meta:
        model = BlogPost
        fields = ["title", "content", "image"]


from django import forms
from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Enter your Email"}),
    )

    class Meta:
        model = Subscription
        fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Subscription.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email


from django import forms
from .models import BlogTag


class BlogTagForm(forms.ModelForm):
    class Meta:
        model = BlogTag
        fields = ["name"]


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Name",
                "required": "required",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email address",
                "required": "required",
            }
        )
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Subject",
                "required": "required",
            }
        ),
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Phone number"}
        ),
    )
    enquiry = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Write message",
                "required": "required",
            }
        )
    )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number should contain only digits.")
        return phone


from django import forms
from .models import FAQ


class FAQForm(forms.ModelForm):
    answer = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 30}))

    class Meta:
        model = FAQ
        fields = ["question", "answer"]
        widgets = {
            "question": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter question"}
            ),
            "answer": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter answer"}
            ),
        }


class PricingPlanForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 30}))

    class Meta:
        model = PricingPlan
        fields = [
            "title",
            "price",
            "duration_days",
            "description",
            "ad_posting",
            "features_ad_availability",
            "security_guarantee",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "duration_days": forms.NumberInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "ad_posting": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "features_ad_availability": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "security_guarantee": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
