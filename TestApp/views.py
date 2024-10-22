from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from TestApp.forms import LoginForm, SubscriptionForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser, UserProfile, Ad
from django.contrib.auth import get_user_model
from .models import (
    Category,
    Banner,
    SiteSettings,
    TeamMember,
    AboutUs,
    BlogPost,
    BlogTag,
    FAQ,
)
from django.core.paginator import Paginator
from django.db.models import Q


def home(request):
    categories = Category.objects.all()
    banners = Banner.objects.all()
    site_settings = SiteSettings.objects.first()
    context = {
        "categories": categories,
        "banners": banners,
        "site_settings": site_settings,
    }
    return render(request, "index.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("TestApp:user_dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required
def user_dashboard(request):
    user = request.user  # This will be an instance of CustomUser
    current_plan = UserPlan.objects.filter(
        user=request.user, expiration_date__gt=timezone.now()
    ).first()
    try:
        profile = UserProfile.objects.get(user=user)  # Get the user profile
    except UserProfile.DoesNotExist:
        profile = None  # Handle the case where the profile does not exist
    ads = Ad.objects.filter(user=user)  # Filter based on the 'user' field
    context = {
        "user": user,
        "profile": profile,
        "ads": ads,
        "current_plan": current_plan,
    }
    return render(request, "dashboard.html", context)


from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .models import CustomUser
from .forms import RegistrationForm


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the username or email already exists
        if CustomUser.objects.filter(username=username).exists():
            return render(
                request, "register.html", {"form_errors": "Username already exists."}
            )

        if CustomUser.objects.filter(email=email).exists():
            return render(
                request, "register.html", {"form_errors": "Email already exists."}
            )

        # Create the user if the username and email are unique
        user = CustomUser.objects.create_user(
            username=username, email=email, password=password
        )
        user.save()
        auth_login(request, user)  # Log the user in after registration
        return redirect("TestApp:user_dashboard")

    return render(request, "register.html")


@login_required
def my_ads(request):
    ads = Ad.objects.filter(
        user=request.user
    )  # Fetch ads related to the logged-in user
    return render(
        request,
        "dashboard_my_ads.html",
        {
            "user": request.user,
            "ads": ads,
        },
    )


def my_searches(request):
    return render(request, "dashboard_my_searches.html")


# views.py
from django.shortcuts import render
from .models import Ad, Favorite


def fav_ads(request):
    user = request.user  # Get the logged-in user
    ads = Ad.objects.filter(favorite__user=user)  # Use the Favorite model

    context = {
        "user": user,
        "ads": ads,
    }
    return render(request, "dashboard_fav_ads.html", context)


def add_favorite(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    ad.favorites.add(request.user)  # Add the user to the favorites
    return redirect("dashboard_fav_ads")  # Redirect to the favorite ads page


def remove_favorite(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    ad.favorites.remove(request.user)  # Remove the user from the favorites
    return redirect("dashboard_fav_ads")  # Redirect to the favorite ads page


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ProfileForm
from .models import UserProfile
from django.shortcuts import render, redirect


@login_required
def settings(request):
    user_profile = request.user.userprofile

    if request.method == "POST":
        # Handle profile update (including image upload)
        contact_form = ProfileForm(request.POST, request.FILES, instance=user_profile)

        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, "Profile updated successfully!")
        else:
            messages.error(request, "Error updating profile.")

        if "image" in request.FILES:
            user_profile.image = request.FILES["image"]
            user_profile.save()
            messages.success(request, "Profile image updated successfully!")

        # Handle phone number update
        if "phone" in request.POST:
            user_profile.phone = request.POST.get("phone")
            user_profile.save()
            messages.success(request, "Phone number updated successfully!")

        # Handle password change
        if "old_password" in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully!")
            else:
                messages.error(request, "Error changing password.")

        # Handle email change
        if "email" in request.POST:
            new_email = request.POST.get("email")
            request.user.email = new_email
            request.user.save()
            messages.success(request, "Email updated successfully!")

        # Handle account deletion
        if "delete_account" in request.POST:
            request.user.delete()
            messages.success(request, "Your account has been deleted.")
            return redirect("TestApp:home")  # Redirect to home or any other page

    # Initialize forms with existing data
    contact_form = ProfileForm(instance=user_profile)
    password_form = PasswordChangeForm(request.user)

    return render(
        request,
        "dashboard_setting.html",
        {
            "contact_form": contact_form,
            "password_form": password_form,
            "user_profile": user_profile,
        },
    )


def aboutus(request):
    site_settings = SiteSettings.objects.first()
    banners = Banner.objects.all()
    team_members = TeamMember.objects.all()
    about_us_section = AboutUs.objects.first()

    context = {
        "site_settings": site_settings,
        "banners": banners,
        "team_members": team_members,
        "about_us_section": about_us_section,
    }
    return render(request, "aboutus.html", context)


from .models import BlogPost, Comment
from .forms import CommentForm


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    comments = post.comments.all()

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_post = post
            comment.save()
            return redirect("TestApp:blog_detail", slug=slug)
    else:
        form = CommentForm()

    return render(
        request,
        "blogdetail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
        },
    )


from .forms import SubscriptionForm, BlogTagForm


def blog_list(request):

    blog_posts = BlogPost.objects.all().order_by("-created_at")
    categories = Category.objects.all()
    tags = BlogTag.objects.all()

    paginator = Paginator(blog_posts, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query = request.GET.get("s", "")
    search_results = blog_posts

    if query:

        search_results = blog_posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing!")
            return redirect("TestApp:blog_list")
    else:
        form = SubscriptionForm()

    context = {
        "page_obj": page_obj,
        "blog_posts": blog_posts,
        "categories": categories,
        "tags": tags,
        "search_results": search_results,
        "query": query,
        "form": form,
    }
    return render(request, "blog.html", context)


def posts_by_tag_view(request, tag_id):
    tag = get_object_or_404(BlogTag, id=tag_id)
    posts = tag.posts.all()
    context = {
        "tag": tag,
        "posts": posts,
    }
    return render(request, "posts_by_tag.html", context)


from django.shortcuts import get_object_or_404, redirect, render
from .models import BlogPost, Comment, Category, BlogTag
from .forms import CommentForm, SubscriptionForm


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    post.views_count += 1
    post.save(update_fields=["views_count"])

    comments = post.comments.all()

    categories = Category.objects.all()
    tags = BlogTag.objects.all()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_post = post
            comment.save()
            return redirect("TestApp:blog_detail", slug=slug)

        subscription_form = SubscriptionForm(request.POST)
        if subscription_form.is_valid():

            subscription_form.save()
            messages.success(request, "Successfully subscribed!")
            return redirect("TestApp:blog_detail", slug=slug)
    else:
        form = CommentForm()
        subscription_form = SubscriptionForm()

    return render(
        request,
        "blogdetail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "subscription_form": subscription_form,
            "categories": categories,
            "tags": tags,
        },
    )


# from .models import BlogPost, Comment
# from .forms import CommentForm


# def blog_detail(request, slug):
#     post = get_object_or_404(BlogPost, slug=slug)

#     post.views_count += 1
#     post.save(update_fields=["views_count"])

#     comments = post.comments.all()
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.blog_post = post
#             comment.save()
#             return redirect("TestApp:blog_detail", slug=slug)
#     else:
#         form = CommentForm()

#     return render(
#         request,
#         "blogdetail.html",
#         {
#             "post": post,
#             "comments": comments,
#             "form": form,
#         },
#     )


from django.shortcuts import render
from django.db.models import Q
from .models import BlogPost
from django.core.paginator import Paginator


def search_results(request):
    query = request.GET.get("s", "")  # Get the search query from the URL
    blog_posts = BlogPost.objects.all()  # Fetch all blog posts for the paginator

    if query:
        # Filter blog posts based on the search query (in title or content)
        blog_posts = blog_posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    paginator = Paginator(blog_posts, 2)  # Show 2 blog posts per page
    page_number = request.GET.get("page")  # Get the page number from the URL
    page_obj = paginator.get_page(
        page_number
    )  # Get the blog posts for the current page

    context = {
        "page_obj": page_obj,
        "query": query,  # The search query, for re-display in the search bar
    }
    return render(
        request, "search_results.html", context
    )  # Render the template with context


from .forms import ContactForm
from .models import Contact


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():

            Contact.objects.create(
                name=form.cleaned_data.get("name"),
                email=form.cleaned_data.get("email"),
                subject=form.cleaned_data.get("subject"),
                phone=form.cleaned_data.get("phone"),
                enquiry=form.cleaned_data.get("enquiry"),
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect("TestApp:contact_us")
        else:
            messages.error(
                request, "There was an error in your submission. Please check the form."
            )
    else:
        form = ContactForm()

    return render(request, "contactus.html", {"form": form})


def faq_view(request):
    faqs = FAQ.objects.all()
    return render(request, "faq.html", {"faqs": faqs})


from .models import PricingPlan
from .forms import PricingPlanForm


def view_pricing_plans(request):
    plans = PricingPlan.objects.all()
    return render(request, "price_plan.html", {"plans": plans})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import PricingPlan, UserPlan


@login_required
def buy_plan(request, plan_id):
    plan = get_object_or_404(PricingPlan, id=plan_id)

    current_plan = UserPlan.objects.filter(
        user=request.user, expiration_date__gt=timezone.now()
    ).first()
    if current_plan:
        current_plan.delete()

    # Create a new plan for the user
    new_user_plan = UserPlan.objects.create(user=request.user, plan=plan)

    return redirect("TestApp:user_dashboard")
