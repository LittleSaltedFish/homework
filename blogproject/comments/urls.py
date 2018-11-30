from django.conf.urls import url

from comments import views

urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment'),
    url(r'^login/$',views.login,name='login'),
    url(r'^dolog/$',views.dolog,name='dolog'),
    url(r'^register/$',views.register,name='register'),
    url(r'^doregister/$',views.doregister,name='doregister'),
    url(r'^verifycode/$', views.yzm, name='yzm'),
    url(r'^liuyanban/$',views.liuyanban,name='liuyanban'),
    url(r'^doliuyan/$',views.doliuyan,name='doliuyan'),
]