from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls.static import static
import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'd_test.views.index', name='index'),
    # url(r'^dtest/', include('d_test.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^ajax/edit/', 'd_test.views.ajax_edit', name='cell_ajax_edit'),
    url(r'^ajax/get_values/', 'd_test.views.get_values', name='ajax_get_values'),
)

