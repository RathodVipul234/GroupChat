from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import UpdateView, CreateView

from django.contrib import messages

from django.shortcuts import render, redirect

from django.contrib.auth import logout

from account.forms import LoginForm, UpdateUser, AddNewUser
from chat.models import Group
from django.template.loader import render_to_string, get_template
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            search_param = request.GET.get("search")
            if search_param:
                context['groups'] = Group.objects.filter(
                    Q((Q(admin = self.request.user) & Q(name__contains=search_param)) |

                    Q((Q(members__in = [self.request.user,]) & Q(name__contains=search_param)))
                )
            ).distinct().order_by("-name")
            else:
                context['groups'] = Group.objects.filter(
                    Q(admin = self.request.user) | Q(members__in = [self.request.user,])
                ).distinct().order_by("-name")

        return self.render_to_response(context)

def get_remaining_user(request,grp_id):
    context = dict()
    
    grp = Group.objects.get(id=grp_id)
    members_id = grp.members.all().values("id")
    rmaining_users = User.objects.exclude(id__in=members_id).exclude(id=grp.admin.id)

    context["grp"] = grp
    context["members_id"] = members_id
    context["rmaining_users"] = rmaining_users
    html = render_to_string('add_member.html', context)
    
    return JsonResponse({'html':html, 'status':200})


class LoginView(FormView):
    template_name = "account/login.html"
    form_class = LoginForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "User logged in successfully.")
        return redirect('home')


class LogoutView(FormView):
    def get(self, *args, **kwargs):
        logout(self.request)
        messages.success(self.request, "User logged out successfully.")
        return redirect('/')


class UserAdminPanelView(TemplateView):
    template_name = "users.html"

class AddNewUserView(CreateView):
    form_class = AddNewUser
    template_name = "account/add_user.html"
    success_url = "/manage-users"

class UserUpdateView(UpdateView):
    model = User
    form_class = UpdateUser
    template_name = "account/update_user.html"
    success_url = "/manage-users"
    slug_field = "id"
    slug_url_kwarg = "user_id"

