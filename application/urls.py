"""
URL configuration for application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView

from apps.logins.views import RegisterView, ForgetPasswdResetView, SendSmsCodeView, APPMobileSMSLoginView, \
    UsernamePassWordLoginView
from apps.users.views import SetUserNicknameView, ChangeAvatarView, uploadImagesView
from mysystem.views.login import LoginView, CaptchaView
from utils.swagger import CustomOpenAPISchemaGenerator

schema_view = get_schema_view(
    openapi.Info(
        title="django-crypto-backend API",
        default_version='v1',
        # description="Test description",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@snippets.local"),
        # license=openapi.License(name="BSD License"),
    ),
    # public 如果为False，则只包含当前用户可以访问的端点。True返回全部
    public=True,
    permission_classes=(permissions.AllowAny,),  # 可以允许任何人查看该接口
    # permission_classes=(permissions.IsAuthenticated) # 只允许通过认证的查看该接口
    generator_class=CustomOpenAPISchemaGenerator,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # api文档地址(正式上线需要注释掉)
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^api/lyapi(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='api-schema-json'),
    path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # 管理后台的标准接口
    path('api/system/', include('mysystem.urls')),
    path('api/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/captcha/', CaptchaView.as_view()),

    # ========================================================================================= #
    # ********************************** 前端微服务API用户接口************************************ #
    # ========================================================================================= #
    # 登录
    path('api/app/login/', UsernamePassWordLoginView.as_view(), name='app端手机号密码登录认证'),
    path('api/app/register/', RegisterView.as_view(), name='app端手机号注册'),
    path('api/app/sendsms/', SendSmsCodeView.as_view(), name='app端手机号发送短信验证码'),
    path('api/app/mobilelogin/', APPMobileSMSLoginView.as_view(), name='app端手机号短信登录认证'),

    # 用户信息
    path('api/app/restpassword/', ForgetPasswdResetView.as_view(), name='app端手机号重置密码'),
    path('api/app/setnickname/', SetUserNicknameView.as_view(), name='app端修改昵称'),
    path('api/app/changeavatar/', ChangeAvatarView.as_view(), name='app端回收员修改头像'),
    path('api/app/uploadimage/', uploadImagesView.as_view(), name='app端上传图片'),
]
