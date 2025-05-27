from django.urls import path
from user_app.api.views import registeration, logout, GetUserInformation, UserPasswordChange, GetUserPendingAdList, GetUserRejectedAdList
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', registeration, name='user-register'),
    path('login/', obtain_auth_token, name='user-login'),
    path('logout/', logout, name='user-logout'),

    path('user/<int:num>/', GetUserInformation.as_view(), name='user-detail'),
    path('user/<int:num>/password/change/', UserPasswordChange.as_view(), name='user-password-change'),

    path('user/<int:num>/pending/ad/list/', GetUserPendingAdList.as_view(), name='user-pending-ad-list'),
    path('user/<int:num>/rejected/ad/list/', GetUserRejectedAdList.as_view(), name='user-rejected-ad-list'),
    
]
