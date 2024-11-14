from apps.settings.models import Setting

def global_settings(request):
    try:
        setting = Setting.objects.latest('id')
    except:
        setting = {'title':'not found'}
    return {'setting':setting}