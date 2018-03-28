from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from admin_tools.menu import items, Menu


class CustomMenu(Menu):

    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
        ]

    def init_with_context(self, context):

        return super(CustomMenu, self).init_with_context(context)
