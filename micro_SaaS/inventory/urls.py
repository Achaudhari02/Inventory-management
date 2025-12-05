from django.urls import path
from . import views


urlpatterns = [
    path('',views.dashboard_view, name='dashboard'),
    path('signup/',views.signup_view,name='signup'),
    path('login/',views.login_view,name="login" ),
    path('logout/',views.logout_view,name='logout'),
    path('business/list', views.business_list_view, name='business-list'),
    path('business/switch/<int:business_id>',views.business_switch_view,name="business-switch"),
    path('business/create', views.business_create_view, name='business-create'),
]