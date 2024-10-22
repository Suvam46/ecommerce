# admin.py
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    UserProfile,
    CustomUser,
    Ad,
    Favorite,
    Category,
    Banner,
    SiteSettings,
    FAQ,
    TeamMember,
    AboutUs,
    BlogTag,
    BlogPost,
)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "image_tag", "phone", "country", "state", "city")

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "No image"

    image_tag.short_description = "Profile Image"


# Optionally, customize the admin interface for CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "username",
        "is_active",
        "is_staff",
    )  # Customize display as needed
    search_fields = ("email", "username")


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Ad)
admin.site.register(Favorite)

admin.site.register(Banner)


class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = [
        "cup_of_coffee",
        "happy_users",
        "ads_posts",
        "total_users",
        "email",
        "phone_number",
    ]

    search_fields = ["email", "phone_number"]


admin.site.register(SiteSettings, SiteSettingsAdmin)

admin.site.register(FAQ)


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["name", "position"]
    search_fields = ["name", "position"]


admin.site.register(TeamMember, TeamMemberAdmin)


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ["introduction", "image"]
    search_fields = ["introduction", "image"]


admin.site.register(AboutUs, AboutUsAdmin)

from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    readonly_fields = ("slug",)  # Make slug readonly, as it's auto-generated


admin.site.register(Category, CategoryAdmin)


admin.site.register(BlogPost)

admin.site.register(BlogTag)

from django.contrib import admin
from .models import FAQ
