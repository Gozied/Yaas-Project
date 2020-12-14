"""yaas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from users import views 
from yauctions import views as auctionview

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/<int:pk>/',views.UserView.as_view(), name='create'),
    path('users/',views.UserView.as_view(), name='users'),
    path('listusers/',views.ListUsersViews.as_view(), name='listall'),
    path('login/',views.LoginView.as_view(), name='userlogin'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('auctions/<int:id>/', auctionview.AuctionView.as_view(), name='get auction'),
    path('create/', auctionview.CreateAndListAuctions.as_view(), name='create_auction'),
    

    
    
    
]
