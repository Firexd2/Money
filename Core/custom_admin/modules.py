from datetime import datetime, timedelta

from admin_tools.dashboard import modules

from Auth.models import VisitationIp


class StatModule(modules.DashboardModule):
    order = VisitationIp
    title = u'Посещения'

    def is_empty(self):
        return False

    @staticmethod
    def filter_visitation_ip(day):
        now = datetime.now().date()
        return VisitationIp.objects.filter(date__lte=now, date__gte=now - timedelta(days=day)).count()

    def __init__(self, **kwargs):
        super(StatModule, self).__init__(**kwargs)
        self.template = 'custom_admin/stat.html'
        self.today = self.filter_visitation_ip(0)
        self.toweek = self.filter_visitation_ip(7)
        self.tomonth = self.filter_visitation_ip(30)
        self.toall = VisitationIp.objects.all().count()
