from django.contrib import admin

from app.internal.admin.admin_user import AdminUserAdmin
from app.internal.admin.user import UserAdmin
from app.internal.admin.checking_account import CheckingAccountAdmin
from app.internal.admin.card import CardAdmin

admin.site.site_title = "Backend course"
admin.site.site_header = "Backend course"
