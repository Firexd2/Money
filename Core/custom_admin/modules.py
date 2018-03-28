# class StatOrderModule(modules.DashboardModule):
#     order = Order.objects
#     title = u'Заказы'
#
#     def is_empty(self):
#         return False
#
#     def filter_status(self, status):
#         return self.order.filter(status=status).count()
#
#     def __init__(self, **kwargs):
#         super(StatOrderModule, self).__init__(**kwargs)
#         self.template = 'modules_for_admin/stat/order.html'
#         self.all = self.order.all().count()
#         self.new = self.filter_status('processed')
#         self.road = self.filter_status('road')
#         self.success = self.filter_status('delivered')