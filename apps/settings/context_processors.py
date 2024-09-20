from apps.settings.models import Setting

def global_settings(request):
    setting = Setting.objects.latest('id')
    return {'setting':setting}