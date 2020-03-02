from django.urls import path
from . import views
from django.conf.urls import url, include

urlpatterns = [
    path('menu_add_get_update_delete/',views.MenuAddView.as_view()),
    path('role_add_get_update_delete/',views.RoleAddView.as_view()),
    path('menu_list_wo_pagination/',views.MenuListView.as_view()),
    path('menu_only_parent_list/',views.MenuOnlyParentListView.as_view()),
    path('admin_user_create/',views.AdminUserCreateView.as_view()),
    path('admin_user_list/',views.AdminUserListView.as_view()),
    path('menu_parent_list/',views.AdminUserListView.as_view()),
    path('role_list_wo_pagination/',views.RoleListView.as_view()),
    path('app_user_list/',views.AppUserListView.as_view()),
    path('app_user_activate/<pk>/',views.AppUserActivateView.as_view()),

]