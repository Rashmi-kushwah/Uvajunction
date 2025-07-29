"""
URL configuration for Uvajunction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views  # ← myapp aapka app ka naam hai
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.guest_login_view, name='guest_login'),
    path('', views.home, name='home'), 
    path('signin/', views.sign_in, name='sign_in'),
    path('logout/',views.logout_view, name='logout'),
    path('register-newuser/',views.new_user_register_view, name='new_user_register'),
    path('register/', views.create_account, name='create_account'),
   
    path('product-list/', views.product_list_view, name='product_list'),
    path('homepage/', views.homepage_view, {'app_menu': 'Home'}, name='homepage_view'),
    path('homepage/<str:app_menu>/', views.homepage_view, name='homepage_view_dynamic'),
    path('product-detail/<str:Product_id>/', views.product_detail_view, name='product_detail_view'),
    path('remove-cart/', views.RemoveCartItem_view, name='remove_cart_item'),
     path('get-profile/', views.get_profile_view, name='get_profile_view'),
    path('update-profile/', views.update_profile_view, name='update_profile_view'),
    path('Addcart/', views.Addcart_view, name='Addcart_view'),
    path('cart/',views.cart_list_view, name='cart_list_view'),
    path('checkout/',views.checkout_view, name='checkout_view'),
    path('address-list/',views.addresses_list_view, name='addresses_list_view'),
    path('Add-address/',views.Add_address_view, name='Add_address_view'),
    path('set-address/',views.Set_address_view, name='Set_address_view'),
    path('delete-address/',views.delete_address_view, name='delete_address'),
    path('edit-address/',views.edit_address_view, name='edit_address'),
    path('setting/',views.setting_view, name='setting_view'),
    path('Business/',views.Business_view, {'app_menu': 'Home'}, name='Business_view'),
    path('get-team-count/',views.get_team_count, name='get_team_count'),
    # path('team-level-count/',views.TeamLevelCount_view, name='TeamLevelCount_view'),
    # path('team-level-count/<int:level>/',views.TeamLevelCount_view, name='TeamLevelCount_view'),
    # urls.py
    path('team-level-count/<int:level>/<str:package>/',views.TeamLevelCount_view, name='TeamLevelCount_view'),
    path('today-team-level-count/<str:package>/',views.today_TeamLevelCount_view, name='today_TeamLevelCount'),

    path("search-team-user/",views.search_team_user_view, name="search_team_user"),
    path("team-rank/",views.team_rank_view, name="team_rank_view"),
    path("today-Team-count/",views.today_Team_count, name="today_Team_count"),
    path("Product-category/",views.Product_Category_view, name="Product_Category"),
    # path("marquee/",views.marquee_context, name="marquee_context"),
    # path("testimonials/", views.get_testimonials_view, name="get_testimonials"),
    path("Add-testimonials/", views.Add_testimonials_view, name="Add_testimonials"),
    path("PopupImage/", views.PopupImage_view, name="PopupImage_view"),
    path("notification/", views.get_notification_view, name="get_notification_view"),
    path("delete-notification/", views.delete_notification_view, name="delete_notification"),
    # path("active-testimonials/", views.active_testimonials_view, name="active_testimonials"),



    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)