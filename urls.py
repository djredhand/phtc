from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
                       (r'^export/$','main.views.exporter'),
                       (r'^import/$','main.views.importer'),
                       (r'^clone/$','main.views.cloner'),

                       ('^accounts/',include('djangowind.urls')),
                       (r'^admin/(.*)', admin.site.root),
                       (r'^munin/total_stands/','main.views.total_stands'),
                       (r'^munin/total_sections/','main.views.total_sections'),
                       (r'^munin/total_standusers/','main.views.total_standusers'),
                       (r'^munin/',include('munin.urls')),
                       (r'^pagetree/',include('pagetree.urls')),
                       (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),
                       (r'^_stand/$','main.views.edit_stand'),
                       (r'^_stand/add/$','main.views.add_stand'),
                       (r'^_stand/users/$','main.views.stand_users'),
                       (r'^_stand/users/(?P<id>\d+)/$','main.views.edit_stand_user'),
                       (r'^_stand/users/add/$','main.views.stand_add_user'),
                       (r'^_stand/users/(?P<id>\d+)/delete/$','main.views.delete_stand_user'),
                       (r'^_stand/groups/$','main.views.stand_groups'),
                       (r'^_stand/groups/add/$','main.views.stand_add_group'),
                       (r'^_stand/groups/(?P<id>\d+)/$','main.views.edit_stand_group'),
                       (r'^_stand/groups/(?P<id>\d+)/delete/$','main.views.delete_stand_group'),
                       (r'^_stand/blocks/$','main.views.manage_blocks'),
                       (r'^_stand/css/$','main.views.css'),
                       (r'^_stand/delete/$','main.views.delete_stand'),
                       (r'^_quiz/',include('quizblock.urls')),
                       (r'^_careermap/',include('careermapblock.urls')),
                       (r'^_fridge/',include('fridgeblock.urls')),
                       (r'^edit/(?P<path>.*)$','forest.main.views.edit_page',{},'edit-page'),
                       (r'^instructor/(?P<path>.*)$','forest.main.views.instructor_page'),
                       (r'^(?P<path>.*)$','forest.main.views.page'),
                       
) 
