from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('login',views.handlelogin,name='login'),
    path('logout',views.handlelogout,name='logout'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('goal',views.goal,name='goal'),
    path('contact',views.contact,name='contact'),
    path('tender/', views.tender_list, name='tender_list'),
    path('tender/<int:tender_id>/', views.tender_detail, name='tender_detail'),
    path('tender/<int:tender_id>/bid/', views.place_bid, name='place_bid'),
    #path('send_email_winner/<int:tender_id>/', views.send_email_winner, name='send_email_winner'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)