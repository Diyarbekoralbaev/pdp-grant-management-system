from django.urls import path
from .views import SignupView, LoginView, RefreshView, ProtectedView, MeView, ChangePasswordView, LogoutView \
    , LogoutAllView, ResetPasswordView, SetNewPasswordView, DeleteUserView, UsersView, UserChangePasswordView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('me/', MeView.as_view(), name='me'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logout-all'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    path('delete-user/', DeleteUserView.as_view(), name='delete-user'),
    path('users/', UsersView.as_view(), name='users'),
    path('user-change-password/', UserChangePasswordView.as_view(), name='user-change-password'),
]
