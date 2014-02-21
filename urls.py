from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from web.views import *
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static


from tastypie.api import Api
from web.api import *


v1_api = Api(api_name='v1')
v1_api.register(UserPendingPoints())


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^api/', include(v1_api.urls)),
                       url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="login"),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'login.html'}, name="logout"),
                       url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name="password_reset"),
                       url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name="password_reset_done"),
                       url(r'^accounts/', include('registration.backends.simple.urls')),
                       )


urlpatterns += patterns('',
                        url(r'^admin/', include(admin.site.urls)),
                        )

urlpatterns += patterns('web.views',
                        url(r'^points/', PointsView.as_view(), name='points'),
                        url(r'^help/', HelpView.as_view(), name='help'),


                        url(r'^newfoot/(?P<obj_id>\d+)/$', FootCreate.as_view(), name='foot_new'),
                        url(r'^editfoot/(?P<pk>\d+)/$', FootUpdate.as_view(), name='foot_edit'),
                        url(r'^deletefoot/(?P<pk>\d+)/$', FootDelete.as_view(), name='foot_delete'),
                        url(r'^listfoot/$', FootList.as_view(), name='foot_list'),

                        url(r'^$', login_required(Home.as_view()), name='home'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)