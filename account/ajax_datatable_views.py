from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import User
from django.urls import reverse

class UsersAjaxDatatableView(AjaxDatatableView):
    model = User
    title = 'User'
    initial_order = [["id", "desc"], ]
    length_menu = [[25, 50, 100, -1], [25, 50, 100, "All"]]
    show_column_filters = False

    column_defs = [
        {'name': 'id', 'title': 'Id', 'visible': True, },
        {'name': 'username', 'visible': True},
        {'name': 'email', 'visible': True},
        {'name': 'first_name', 'visible': True},
        {'name': 'last_name', 'visible': True},
        {'name': 'Action', 'visible': True, 'searchable': False}
    ]

    def customize_row(self, row, obj):
        edit_usr_url = reverse('update_user', args=(obj.id,))
        row['Action'] = f"<a href='{edit_usr_url}'>Edit<i class='las la-user-alt text-secondary font-16'></i></a>"