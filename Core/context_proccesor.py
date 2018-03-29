def get_last_version(request):
    from Core.models import VersionControl
    return {'version': VersionControl.objects.all().last()}
