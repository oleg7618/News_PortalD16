from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


# (1)
# (2)
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    # (3)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context