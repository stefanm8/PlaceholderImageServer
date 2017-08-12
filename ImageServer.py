import sys
import os
from django.conf import settings

DEBUG = os.environ.get('DEBUG', 'on') == 'on'

SECRET_KEY = os.environ.get('SECRET_KEY', 'wjx%3na7dratpw=j7qa_&a7dhva&8da46_o%hzvoj7d6h##mj#')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost')

settings.configure(
    ALLOWED_HOSTS = ['127.0.0.1','localhost'],
    DEBUG=DEBUG,
    SECRET_KEY = SECRET_KEY,
    ROOT_URLCONF = __name__,
    MIDDLEWARE_CLASSES=(

        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),

)

from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
import views
def index(request):
    return HttpResponse('heelo World')


application = get_wsgi_application()

urlpatterns = (
    url(r'^$', views.index),
    url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', views.generate_Placeholder, name='placeholder'),

)

if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
