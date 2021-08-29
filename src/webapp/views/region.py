from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import  DeleteView

from webapp.models import Region


class RegionDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for delete region.
    """
    model = Region
    template_name = '../templates/delete.html'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect('admin:webapp_region_changelist')
