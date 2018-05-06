# django
from django.utils.translation import activate
from django.views.generic import FormView

# app
from .controllers import PermissionController
from .forms import PermissionForm


class PermissionView(FormView):
    form_class = PermissionForm
    template_name = 'djgpp/permissions.html'

    def form_valid(self, form):
        data = form.cleaned_data['url']
        app_id = data['id']
        language = data['hl']
        controller = PermissionController()
        groups = controller.get(app_id=app_id, language=language)
        context = self.get_context_data(form=form, groups=groups)
        activate(language)
        return self.render_to_response(context)
