import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.views import generic as views
from cm_api.resources import SubscriberResource

class ProfileAdminView (views.TemplateView):
    template_name = 'cm/profile_admin.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileAdminView, self).get_context_data(**kwargs)

        subscriber = self.request.user.subscriber
        context['subscriber'] = subscriber

        subscriber_data = SubscriberResource().serialize(subscriber)
        context['subscriber_data'] = json.dumps(
            subscriber_data, cls=DjangoJSONEncoder)

        return context


class LandingPageView (views.View):

    def get(self, request):
        return render(request, 'cm/index.html', {})
