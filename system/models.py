from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class SysContentType(models.Model):
    app_label = models.CharField(max_length=100)
    module = models.CharField(max_length=100, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_content_type'
        unique_together = (('app_label', 'module'),)


class SysMenu(models.Model):
    id = models.IntegerField(primary_key=True)
    par = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    menu_name_cn = models.CharField(max_length=255)
    menu_name_en = models.CharField(max_length=255)
    seq_no = models.IntegerField()
    menu_icon = models.TextField(blank=True, null=True)
    menu_type = models.CharField(max_length=255)
    menu_route = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'sys_menu'


class SysPermission(models.Model):
    par = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    content_type = models.ForeignKey(SysContentType, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    route = models.CharField(unique=True, max_length=255)
    desc = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_permission'


class SysRole(models.Model):
    name = models.CharField(unique=True, max_length=150)
    status = models.IntegerField()
    desc = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_role'


class SysRoleMenu(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(SysRole, models.DO_NOTHING)
    menu = models.ForeignKey(SysMenu, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sys_role_menu'


class SysRolePermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(SysRole, models.DO_NOTHING)
    permission = models.ForeignKey(SysPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sys_role_permissions'


class SysUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sys_user'


class SysUserRoles(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(SysUser, models.DO_NOTHING)
    role = models.ForeignKey(SysRole, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sys_user_roles'
