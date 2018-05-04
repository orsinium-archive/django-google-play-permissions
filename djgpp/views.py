# django
from django.views.generic import FormView
from .forms import PermissionForm
from .managers import PermissionManager


class PermissionView(FormView):
    form_class = PermissionForm
    template_name = 'djgpp/permissions.html'

    def form_valid(self, form):
        data = form.cleaned_data['url']
        app_id = data['id']
        language = data['hl']
        permission_manager = PermissionManager()
        permissions = permission_manager.get(app_id=app_id, language=language)
        context = self.get_context_data(form=form, permissions=permissions)
        return self.render_to_response(context)
