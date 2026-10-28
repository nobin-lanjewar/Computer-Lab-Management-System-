from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView


class ProtectedDeleteView(DeleteView):
    def form_valid(self, form):
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(
                self.request,
                "This record is still in use and cannot be deleted.",
            )
        else:
            messages.success(self.request, "Record deleted.")
        return HttpResponseRedirect(self.get_success_url())
