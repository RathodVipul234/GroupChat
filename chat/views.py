from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, CreateView
from chat.forms import GroupForm
from django.views.decorators.csrf import csrf_exempt
from chat.models import Group, Messages
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.


class CreateGroup(CreateView):
    form_class = GroupForm
    template_name = "chat/create_group.html"
    success_url = "/"
    
    def form_valid(self ,form):
        obj = form.save(commit=False)
        obj.admin = self.request.user
        obj.save()
        form.save_m2m()

        return redirect(self.success_url)

@csrf_exempt
def add_new_user_in_group(request,grp_id):
    grp = Group.objects.get(id=grp_id)
    user = User.objects.get(email=request.POST.get("new_user"))
    grp.members.add(user)
    return redirect("/")



def chat_room(request, room_slug):
    grp = Group.objects.get(slug=room_slug)
    chat_history = Messages.objects.filter(group = grp).order_by("created_at")
    return render(request, "chat/chat.html", {"grp" : grp, "chat_history":chat_history})

def delete_group(request, room_slug):
    grp = Group.objects.get(slug=room_slug)
    if grp.admin == request.user:
        grp.delete()
        msg = "group deleted successfully."
    else:
        msg = "you do not have access to delete this group"
    messages.success(request, msg)
    return redirect("/")