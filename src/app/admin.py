from django.contrib import admin
from app.internal.users.presentation.admin import AdminUserAdmin
from app.internal.users.presentation.admin import UserAdmin
from app.internal.bank.presentation.admin import CheckingAccountAdmin
from app.internal.bank.presentation.admin import CardAdmin

admin.site.site_title = "Backend course"
admin.site.site_header = "Backend course"
