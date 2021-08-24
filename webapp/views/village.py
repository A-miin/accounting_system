from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DeleteView
from webapp.models import Village

class VillageDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for delete regions.
    """
    model = Village
    template_name = 'delete.html'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect('admin:webapp_village_changelist')
