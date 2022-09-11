from django.urls import path

from account import views
from account import ajax_datatable_views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("manage-users/", views.UserAdminPanelView.as_view(), name="manage_user"),
    path("user/<int:user_id>/edit/", views.UserUpdateView.as_view(), name="update_user"),
    path("add/new-user/", views.AddNewUserView.as_view(), name="add_new_user"),
    path("get-remaining-user/<int:grp_id>/", views.get_remaining_user, name="get_remaining_user"),
    path('ajax_datatable/users/', ajax_datatable_views.UsersAjaxDatatableView.as_view(), name="ajax_datatable_users"),

]
