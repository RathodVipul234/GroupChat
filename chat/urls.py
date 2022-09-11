from django.urls import path
from chat import views
urlpatterns = [
    path("create-group/", views.CreateGroup.as_view(), name="create_group"),
    path("add/new-user-in-grp/<int:grp_id>/", views.add_new_user_in_group, name="add_new_user_in_grp"),
    path("chat_room/<slug:room_slug>/", views.chat_room, name="chat_room"),
    path("group/<slug:room_slug>/delete/", views.delete_group, name="delete_grp"),
]
