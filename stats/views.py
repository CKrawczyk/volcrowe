from django.shortcuts import render
from django.http import HttpResponse
import rest_framework_filters as filters
from rest_framework import viewsets
from stats.models import *
from stats.serializers import *


class SurveyProjectFilter(filters.FilterSet):
    classifications = filters.AllLookupsFilter(name='total_n_classifications')
    sessions = filters.AllLookupsFilter(name='total_n_sessions')
    days = filters.AllLookupsFilter(name='total_n_unique_days')

    class Meta:
        model = SurveyProject
        fields = ['project', 'classifications', 'sessions']


class UserFilter(filters.FilterSet):
    survey_project = filters.RelatedFilter(
        SurveyProjectFilter, name='survey_project'
    )
    talk_posts = filters.AllLookupsFilter(name='talk_posts')
    classifications = filters.AllLookupsFilter(name='total_n_classifications')
    sessions = filters.AllLookupsFilter(name='total_n_sessions')
    projects = filters.AllLookupsFilter(name='total_n_projects')

    class Meta:
        model = User
        fields = ['country', 'survey_project', 'talk_posts',
                  'classifications', 'sessions', 'projects']


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    filter_class = UserFilter
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class QuestionFilter(filters.FilterSet):
    kind = filters.CharFilter(name='kind__kind')
    category = filters.CharFilter(name='category__category')

    class Meta:
        model = Question
        fields = ['kind', 'category', 'number']


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    filter_class = QuestionFilter
    queryset = Question.objects.all().order_by('number')
    serializer_class = QuestionSerializer


class AnswerFilter(filters.FilterSet):
    question = filters.RelatedFilter(QuestionFilter, name='question')
    user = filters.RelatedFilter(UserFilter, name='user')

    class Meta:
        model = Answer
        fields = ['question', 'user']


class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    filter_class = AnswerFilter
    queryset = Answer.objects.all().order_by('question__number')
    serializer_class = AnswerSerializer
