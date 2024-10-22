from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import uuid
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_images/", default="default.png")
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    newsletter = models.BooleanField(default=False)
    message_notification = models.BooleanField(default=False)
    listing_alerts = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username.strip(), email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(
            username, email, password, **extra_fields, is_staff=True
        )


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to="img/", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Ad(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="ads/", null=True, blank=True)

    favorites = models.ManyToManyField(
        CustomUser, related_name="favorite_ads", blank=True
    )

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "ad")  # Ensure a user can favorite an ad only once


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="categories/")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically generate UUID slug if not provided
        if not self.slug:
            self.slug = str(uuid.uuid4())  # Generate a UUID string
        super(Category, self).save(*args, **kwargs)


class Banner(models.Model):
    image = models.ImageField(upload_to="banners/")
    alt_text = models.CharField(max_length=255, default="", blank=True)

    def __str__(self):
        return f"Banner {self.id}"


class SiteSettings(models.Model):
    # Site statistics
    cup_of_coffee = models.PositiveIntegerField(
        default=0, help_text="Number of cups of coffee consumed."
    )
    happy_users = models.PositiveIntegerField(
        default=0, help_text="Number of happy users."
    )
    ads_posts = models.PositiveIntegerField(
        default=0, help_text="Total number of ads posted."
    )
    total_users = models.PositiveIntegerField(
        default=0, help_text="Total number of users registered."
    )

    # Contact and location details
    address = models.TextField(help_text="Physical address of the company.")
    email = models.EmailField(help_text="Contact email.")
    phone_number = models.CharField(max_length=20, help_text="Contact phone number.")

    # Social media links
    facebook_link = models.URLField(blank=True, help_text="Facebook page URL.")
    instagram_link = models.URLField(blank=True, help_text="Instagram profile URL.")
    youtube_link = models.URLField(blank=True, help_text="YouTube channel URL.")
    linkedin_link = models.URLField(blank=True, help_text="LinkedIn profile URL.")

    # Miscellaneous
    iframe_map_location = models.TextField(
        help_text="HTML code for Google Map iframe.", blank=True
    )
    terms_and_conditions = models.TextField(help_text="Terms and Conditions content.")

    def __str__(self):
        return "Site Settings"


class FAQ(models.Model):
    question = models.CharField(
        max_length=255, help_text="The frequently asked question"
    )
    answer = models.TextField(help_text="The answer to the FAQ")

    def __str__(self):
        return self.question


class TeamMember(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the team member")
    position = models.CharField(
        max_length=100, help_text="Job title/position of the team member"
    )
    image = models.ImageField(
        upload_to="team/", help_text="Upload profile picture of the team member"
    )

    def __str__(self):
        return self.name


class AboutUs(models.Model):
    introduction = models.TextField()
    image = models.ImageField(upload_to="about/")

    def __str__(self):
        return self.introduction


class BlogTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="blog_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, default=uuid.uuid4)
    tags = models.ManyToManyField(BlogTag, related_name="posts", blank=True)
    views_count = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse("blog_detail", args=[self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog_post = models.ForeignKey(
        BlogPost, related_name="comments", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.blog_post.title}"


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, blank=True)
    enquiry = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.name} ({self.email})"


from django.db import models


class PricingPlan(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    description = models.TextField()
    ad_posting = models.BooleanField(default=False)
    features_ad_availability = models.BooleanField(default=False)
    security_guarantee = models.BooleanField(default=False)

    def __str__(self):
        return self.title


from django.contrib.auth.models import (
    User,
)  # Assuming you're using the default User model
from django.db import models
from django.utils import timezone
from datetime import timedelta


class PricingPlan(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    ad_posting = models.BooleanField(default=False)
    features_ad_availability = models.BooleanField(default=False)
    security_guarantee = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class UserPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(PricingPlan, on_delete=models.SET_NULL, null=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expiration_date:
            self.expiration_date = timezone.now() + timedelta(
                days=self.plan.duration_days
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s {self.plan.title} Plan"


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import PricingPlan, UserPlan


@login_required
def buy_plan(request, plan_id):
    plan = get_object_or_404(PricingPlan, id=plan_id)

    # Check if the user already has an active plan and delete it
    current_plan = UserPlan.objects.filter(
        user=request.user, expiration_date__gt=timezone.now()
    ).first()
    if current_plan:
        current_plan.delete()

    # Create a new plan for the user
    new_user_plan = UserPlan.objects.create(user=request.user, plan=plan)

    return redirect("user_dashboard")


@login_required
def user_dashboard(request):
    current_plan = UserPlan.objects.filter(
        user=request.user, expiration_date__gt=timezone.now()
    ).first()

    return render(request, "user_dashboard.html", {"current_plan": current_plan})
