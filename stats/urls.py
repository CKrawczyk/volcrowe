from django.conf.urls import include, url
import stats.views as views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='User')
router.register(r'questions', views.QuestionViewSet)
router.register(r'counts', views.QuestionCountSet, base_name='Counts')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'user/counts', views.UserCountSet.as_view(), name='user-counts'),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
        ),
]
