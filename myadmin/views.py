from django.shortcuts import render, get_object_or_404, redirect
from TestApp.models import (
    Banner,
    Category,
    AboutUs,
    TeamMember,
    SiteSettings,
    Comment,
    BlogPost,
    Contact,
    FAQ,
    PricingPlan,
)
from TestApp.forms import (
    BannerForm,
    CategoryForm,
    AboutUsForm,
    TeamMemberForm,
    SiteSettingsForm,
    BlogPostForm,
    CommentForm,
    ContactForm,
    FAQForm,
    PricingPlanForm,
)
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
import csv


def index(request):
    return render(request, "admin_panel/index.html")


def view_banner(request):
    banners = Banner.objects.all()

    context = {"banners": banners}
    return render(request, "admin_panel/view_banner.html", context)


def add_banner(request):
    if request.method == "POST":
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse("view_banner"))
    else:
        form = BannerForm()

    return render(request, "admin_panel/add_banner.html", {"form": form})


def edit_banner(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)

    if request.method == "POST":
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            return redirect("view_banner")
    else:
        form = BannerForm(instance=banner)

    return render(
        request, "admin_panel/edit_banner.html", {"form": form, "banner": banner}
    )


def delete_banner(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    if request.method == "POST":
        banner.delete()
        return redirect("view_banner")
    return render(request, "admin_panel/confirm_delete.html", {"banner": banner})


def view_category(request):
    categories = Category.objects.all()
    return render(request, "admin_panel/view_category.html", {"categories": categories})


# View for adding a new category
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse("view_category"))
    else:
        form = CategoryForm()
    return render(request, "admin_panel/add_category.html", {"form": form})


# View for editing an existing category
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect(reverse("view_category"))
    else:
        form = CategoryForm(instance=category)
    return render(request, "admin_panel/edit_category.html", {"form": form})


# View for deleting a category
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        category.delete()
        return redirect(reverse("view_category"))
    return render(request, "admin_panel/delete_category.html", {"category": category})


def edit_aboutus(request):
    # Get the first (and only) AboutUs entry, or create a new one if it doesn't exist
    aboutus, created = AboutUs.objects.get_or_create(
        id=1
    )  # Assuming you will only ever have one entry with ID 1

    if request.method == "POST":
        form = AboutUsForm(request.POST, request.FILES, instance=aboutus)
        if form.is_valid():
            form.save()
            return redirect(
                "edit_aboutus"
            )  # Redirect back to the same edit page after saving
    else:
        form = AboutUsForm(instance=aboutus)

    return render(request, "admin_panel/edit_aboutus.html", {"form": form})


# View Team Members
def view_team(request):
    team_members = TeamMember.objects.all()
    return render(request, "admin_panel/view_team.html", {"team_members": team_members})


# Add a new Team Member
def add_team_member(request):
    if request.method == "POST":
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("view_team")
    else:
        form = TeamMemberForm()
    return render(request, "admin_panel/add_team_member.html", {"form": form})


# Edit an existing Team Member
def edit_team_member(request, team_member_id):
    team_member = get_object_or_404(TeamMember, id=team_member_id)
    if request.method == "POST":
        form = TeamMemberForm(request.POST, request.FILES, instance=team_member)
        if form.is_valid():
            form.save()
            return redirect("view_team")
    else:
        form = TeamMemberForm(instance=team_member)
    return render(request, "admin_panel/edit_team_member.html", {"form": form})


# Delete a Team Member
def delete_team_member(request, team_member_id):
    team_member = get_object_or_404(TeamMember, id=team_member_id)
    if request.method == "POST":
        team_member.delete()
        return redirect("view_team")
    return render(
        request, "admin_panel/delete_team_member.html", {"team_member": team_member}
    )


# View Site Settings
def view_site_settings(request):
    settings_entries = SiteSettings.objects.all()
    return render(
        request,
        "admin_panel/view_site_settings.html",
        {"settings_entries": settings_entries},
    )


# Edit an existing Site Settings entry
def edit_site_settings(request):
    settings = get_object_or_404(SiteSettings)
    if request.method == "POST":
        form = SiteSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect("view_site_settings")
    else:
        form = SiteSettingsForm(instance=settings)
    return render(request, "admin_panel/edit_site_settings.html", {"form": form})


def blog_list(request):
    blogs = BlogPost.objects.all()
    return render(request, "admin_panel/manage_blogs.html", {"blogs": blogs})


def blog_add(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("view_blog")
    else:
        form = BlogPostForm()
    return render(
        request, "admin_panel/manage_blog_form.html", {"form": form, "action": "Add"}
    )


def blog_edit(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("view_blog")
    else:
        form = BlogPostForm(instance=post)
    return render(
        request, "admin_panel/manage_blog_form.html", {"form": form, "action": "Edit"}
    )


def blog_delete(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.method == "POST":
        post.delete()
        return redirect("view_blog")
    return render(
        request, "admin_admin/manage_blog_confirm_delete.html", {"post": post}
    )


def view_comments(request):
    comments = Comment.objects.all()
    return render(request, "admin_panel/view_comments.html", {"comments": comments})


def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully!")
            return redirect("view_comments")
    else:
        form = CommentForm(instance=comment)

    return render(
        request, "admin_panel/edit_comment.html", {"form": form, "comment": comment}
    )


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
        return redirect("view_comments")
    return render(request, "admin_panel/delete_comment.html", {"comment": comment})


def view_contacts(request):
    contacts = Contact.objects.all()
    return render(request, "admin_panel/view_contacts.html", {"contacts": contacts})


def edit_contact(request, id):
    contact = get_object_or_404(Contact, id=id)

    if request.method == "POST":

        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact updated successfully!")
            return redirect("view_contacts")
        else:
            messages.error(request, "Please correct the errors below.")
    else:

        form = ContactForm(instance=contact)

    return render(
        request, "admin_panel/edit_contact.html", {"form": form, "contact": contact}
    )


def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    contact.delete()
    messages.success(request, "Contact deleted successfully!")
    return redirect("view_contacts")


def download_contacts_csv(request):
    contacts = Contact.objects.all()
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="contacts.csv"'

    writer = csv.writer(response)
    writer.writerow(["Name", "Email", "Subject", "Phone", "Enquiry", "Created At"])
    for contact in contacts:
        writer.writerow(
            [
                contact.name,
                contact.email,
                contact.subject,
                contact.phone,
                contact.enquiry,
                contact.created_at,
            ]
        )

    return response


def view_faq(request):
    faqs = FAQ.objects.all()
    return render(request, "admin_panel/view_faq.html", {"faqs": faqs})


def add_faq(request):
    if request.method == "POST":
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("view_faq")
    else:
        form = FAQForm()
    return render(request, "admin_panel/add_faq.html", {"form": form})


def edit_faq(request, id):
    faq = get_object_or_404(FAQ, id=id)
    if request.method == "POST":
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            return redirect("view_faq")
    else:
        form = FAQForm(instance=faq)
    return render(request, "admin_panel/edit_faq.html", {"form": form, "faq": faq})


def delete_faq(request, id):
    faq = get_object_or_404(FAQ, id=id)
    faq.delete()
    return redirect("view_faq")


def view_pricing_plans(request):
    plans = PricingPlan.objects.all()
    return render(request, "admin_panel/view_pricing_plans.html", {"plans": plans})


def add_pricing_plan(request):
    if request.method == "POST":
        form = PricingPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("view_pricing_plans")
    else:
        form = PricingPlanForm()
    return render(request, "admin_panel/add_pricing_plan.html", {"form": form})


def edit_pricing_plan(request, id):
    plan = get_object_or_404(PricingPlan, id=id)
    if request.method == "POST":
        form = PricingPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect("view_pricing_plans")
    else:
        form = PricingPlanForm(instance=plan)
    return render(
        request, "admin_panel/edit_pricing_plan.html", {"form": form, "plan": plan}
    )


def delete_pricing_plan(request, id):
    plan = get_object_or_404(PricingPlan, id=id)
    plan.delete()
    return redirect("view_pricing_plans")
