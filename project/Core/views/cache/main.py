from django.views import View


class ContextCacheTemplate(View):
    # require: get_dynamic_context and get_static_context

    def get_context(self, page_id: str, *args):
        if self.request.session.get(f'{page_id}_static_context') is None:
            static_context = self.get_static_context(*args)
            self.request.session[f'{page_id}_static_context'] = static_context
        return {**self.request.session[f'{page_id}_static_context'], **self.get_dynamic_context(*args)}