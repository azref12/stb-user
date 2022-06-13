from django.urls import path
from django.conf.urls import url
from . import views_user, views_changepass
from . import views_activation
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .custome_jwt import LogoutView, MyTokenObtainPairView

urlpatterns = [
    
    path ('user/', views_user.UserActive),
    # url(r'user/$', views_user.UserActive),
    url(r'activation/$', views_activation.UserActivation),
    url(r'changepassword/$', views_changepass.UserPass),
    url(r'login/$', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'login/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'logout/', LogoutView.as_view(), name='auth_logout')
    
]