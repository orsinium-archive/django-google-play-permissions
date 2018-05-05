# django
from django.utils.translation import activate
from django.views.generic import FormView

# app
from .forms import PermissionForm
from .managers import PermissionManager
from .utils import group_by_parents


class PermissionView(FormView):
    form_class = PermissionForm
    template_name = 'djgpp/permissions.html'

    def form_valid(self, form):
        data = form.cleaned_data['url']
        app_id = data['id']
        language = data['hl']
        permission_manager = PermissionManager()
        permissions = permission_manager.get(app_id=app_id, language=language)
        groups = group_by_parents(permissions)
        context = self.get_context_data(form=form, groups=groups)
        activate(language)
        return self.render_to_response(context)
