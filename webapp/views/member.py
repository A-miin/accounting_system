from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import (
    ListView,
    DeleteView
)
from django.db.models import Q
from django.utils.http import urlencode

from webapp.models import Member
from webapp.form import SearchForm


class IndexView(ListView):
    template_name = 'index.html'
    model = Member
    context_object_name = 'members'
    ordering = ('deleted', '-created_at')

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(IndexView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_data:
            queryset = queryset.filter(
                Q(name__icontains=self.search_data) |
                Q(surname__icontains=self.search_data) |
                Q(phone_number1__icontains=self.search_data) |
                Q(phone_number2__icontains=self.search_data) |
                Q(whatsapp_number__icontains=self.search_data)
            )
        return queryset

    def get_search_data(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search_value']
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        if self.search_data:
            context['query'] = urlencode({'search_value': self.search_data})

        return context


class MemberDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for delete members.
    """
    model = Member
    template_name = 'delete.html'

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deleted = timezone.now()
        self.object.save()
        return redirect('admin:webapp_member_changelist')

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def test_list(request):
    return redirect('admin:webapp_membershipfee_changelist')