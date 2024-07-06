from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add/', views.add_tender, name='add_tender'),
    path('update/<int:pk>/', views.update_tender, name='update_tender'),
    path('delete/<int:pk>/', views.delete_tender, name='delete_tender'),
    
    path('',views.home,name='home'),
    path('search/',views.search, name='search'),
    path('signup',views.signup,name='signup'),
    path('login',views.handlelogin,name='login'),
    path('logout',views.handlelogout,name='logout'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('tender/', views.tender_list, name='tender_list'),
    path('tender/<int:tender_id>/', views.tender_detail, name='tender_detail'),
    path('tender/<int:tender_id>/bid/', views.place_bid, name='place_bid'),
    # path('category',views.category,name='category'),
    #path('send_email_winner/<int:tender_id>/', views.send_email_winner, name='send_email_winner'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)