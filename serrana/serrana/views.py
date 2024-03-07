from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "home/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Define your list of URLs here
        urls = [
            {"url": "/produtos/", "name": "Produtos"},
            {"url": "/login", "name": "Login"},
        ]
        
        context["urls"] = urls
        return context
