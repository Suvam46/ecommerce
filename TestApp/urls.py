from django.contrib import admin
from django.urls import path
from TestApp.views import (
    home,
    login,
    user_dashboard,
    register,
    my_ads,
    my_searches,
    fav_ads,
    settings,
    add_favorite,
    remove_favorite,
    aboutus,
    blog_list,
    blog_detail,
    search_results,
    posts_by_tag_view,
    contact_us,
    faq_view,
    view_pricing_plans,
    buy_plan,
)


app_name = "TestApp"

urlpatterns = [
    path("", home, name="home"),
    path("login", login, name="login"),
    path("dashboard", user_dashboard, name="user_dashboard"),
    path("register", register, name="register"),
    path("my_ads", my_ads, name="my_ads"),
    path("my_searches", my_searches, name="my_searches"),
    path("fav_ads/", fav_ads, name="fav_ads"),
    path("ad/<int:ad_id>/add_favorite/", add_favorite, name="add_favorite"),
    path("ad/<int:ad_id>/remove_favorite/", remove_favorite, name="remove_favorite"),
    path("settings", settings, name="settings"),
    path("aboutus", aboutus, name="aboutus"),
    path("blogs/", blog_list, name="blog_list"),
    path("tags/<int:tag_id>/", posts_by_tag_view, name="posts_by_tag"),
    path("blog/<slug:slug>/", blog_detail, name="blog_detail"),
    path("search", search_results, name="search_results"),
    path("contact", contact_us, name="contact_us"),
    path("faq", faq_view, name="faq"),
    path("price_plan", view_pricing_plans, name="view_pricing_plans"),
    path("buy-plan/<int:plan_id>/", buy_plan, name="buy_plan"),
]
