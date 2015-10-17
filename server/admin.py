from django.contrib import admin
from django.utils.html import format_html

from models import Tool, User, Card, Permissions, Log

def username_and_profile(u):
  if u.__class__ == Permissions or u.__class__ == Card or u.__class__ == Log:
    u = u.user
  return u'<a href="https://london.hackspace.org.uk/members/profile.php?id=%d">%s</a>' % (u.id, format_html(u.name))
username_and_profile.short_description = 'Name'
username_and_profile.allow_tags = True
username_and_profile.admin_order_field = 'user'

class ToolAdmin(admin.ModelAdmin):
  readonly_fields = ('inuse', 'inuseby')
  list_display = ('id', 'name', 'status', 'status_message', 'secret', 'inuse', 'inuseby')
  search_fields = ('name','id')
  list_editable = ('status', 'status_message')
  list_filter = ('status',)

class UserAdmin(admin.ModelAdmin):
  fields = (('lhsid', 'name', 'subscribed'),)
  readonly_fields = ('lhsid', 'name', 'subscribed')
  list_display = ('id', 'lhsid', 'username_and_profile', 'subscribed',)
  search_fields = ('name','id')
  list_filter = ('subscribed',)

class CardAdmin(admin.ModelAdmin):
  fields = (('user', 'card_id'),)
  readonly_fields = ('user', 'card_id')
  list_display = ('card_id', username_and_profile,)

class PermissionsAdmin(admin.ModelAdmin):
  fields = (('tool', 'user', 'permission'),)
  list_display = ('tool', username_and_profile, 'permission', 'addedby', 'date')
  list_filter = ('tool', 'permission')

  def save_model(self, request, obj, form, change):
    # this assumes that the user id's of django users
    # matches the id's of hackspace users.
    obj.addedby = User.objects.get(id=request.user.id)
    obj.save()

class LogAdmin(admin.ModelAdmin):
  fields = (('tool', 'user', 'date', 'message'),)
  list_display = ('tool', username_and_profile, 'date', 'message')
  list_filter = ('tool',)
  readonly_fields = ('tool', 'user', 'date', 'message')
  search_fields = ('user',)

admin.site.register(Tool, ToolAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Permissions, PermissionsAdmin)
admin.site.register(Log, LogAdmin)

