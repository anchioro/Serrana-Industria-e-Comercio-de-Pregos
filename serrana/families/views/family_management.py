from django.db.models import Q, Max, OuterRef
from django.shortcuts import get_object_or_404, redirect
from families.models.family import Family, FamilyAction
from families.forms.family import FamilyForm, FamilyContactInformationForm
from families.forms.action import FamilyActionForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class FamilyListView(LoginRequiredMixin, ListView):
    model = Family
    paginate_by = 25
    template_name = "families/index.html"

    # def get_queryset(self):
    #     latest_actions_subquery = FamilyAction.objects.filter(
    #         product_id=OuterRef("id")
    #     ).values("product_id").annotate(
    #         latest_action=Max("created_at")
    #     ).values("latest_action")
        
    #     queryset = Family.objects.annotate(
    #         latest_action=latest_actions_subquery
    #     ).order_by("-latest_action").distinct()
        
    #     return queryset
    
class FamilySearchView(LoginRequiredMixin, ListView):
    model = Family
    paginate_by = 25
    template_name = "families/index.html"
    ordering = "-id"
    
    def get_queryset(self):
        search_value = self.request.GET.get("q").strip()
        
        if search_value:
            Family.objects.filter(
                Q(family_manager__icontains=search_value)
            ).order_by("-id")
            
        else:
            latest_actions_subquery = FamilyAction.objects.filter(
                product_id=OuterRef("id")
            ).values("product_id").annotate(
                latest_action=Max("created_at")
            ).values("latest_action")
            
            queryset = Family.objects.annotate(
                latest_action=latest_actions_subquery
            ).order_by("-latest_action").distinct()
            
            return queryset

class FamilyInformationView(LoginRequiredMixin, DetailView):
    model = Family
    template_name = "families/information.html"
    slug_field = "slug"

    def get_queryset(self):
        return Family.objects.filter(slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["product"] = product
        return context

class FamilyCreateView(LoginRequiredMixin, CreateView):
    model = Family
    form_class = FamilyForm
    contact_form_class = FamilyContactInformationForm
    template_name = "families/create.html"
    success_url = reverse_lazy("families:index")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form" not in context:
            context["form"] = self.form_class(self.request.GET)
        if "contact_form" not in context:
            context["contact_form"] = self.contact_form_class(self.request.GET)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(self.form_class)
        contact_form = self.get_form(self.contact_form_class)
        if form.is_valid() and contact_form.is_valid():
            return self.form_valid(form, contact_form)
        else:
            return self.form_invalid(form, contact_form)

    def form_valid(self, form, contact_form):
        form.instance.created_by = self.request.user
        form.instance.is_active = True
        self.object = form.save()
        contact_form.instance.family = self.object
        contact_form.save()
        return super().form_valid(form)

    def form_invalid(self, form, contact_form):
        return self.render_to_response(
            self.get_context_data(form=form, contact_form=contact_form))
    
class FamilyUpdateView(LoginRequiredMixin, UpdateView):
    model = Family
    form_class = FamilyForm
    template_name = "families/update.html"
    success_url = reverse_lazy("families:index")
    
class FamilyDeleteView(LoginRequiredMixin, DeleteView):
    model = Family
    success_url = reverse_lazy("families:index")

class FamilyActionView(LoginRequiredMixin, CreateView):
    model = FamilyAction
    form_class = FamilyActionForm
    template_name = "families/action.html"
    
    def get_success_url(self):
        slug = self.object.family.slug
        return reverse_lazy("families:history", kwargs={"slug": slug})
    
    def form_valid(self, form):
        family = get_object_or_404(Family, slug=self.kwargs["slug"])
        
        form.instance.family = family
        form.instance.created_by = self.request.user
        
        return super().form_valid(form)
    
    def get_queryset(self):
        return Family.objects.filter(slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        family = self.get_object()
        context["family"] = family
        return context
    
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     product = get_object_or_404(Family, slug=self.kwargs["slug"])
    #     kwargs["product"] = product
    #     return kwargs

def toggle_completion(request, action_id):
    action = get_object_or_404(FamilyAction, pk=action_id)
    
    action.is_finished = not action.is_finished
    action.save()
    
    return redirect("families:history", slug=action.family.slug)


class FamilyHistoryView(LoginRequiredMixin, ListView):
    model = FamilyAction
    paginate_by = 25
    template_name = "families/history.html"


    def get_queryset(self):
        return FamilyAction.objects.filter(family__slug=self.kwargs["slug"]).order_by("-created_at")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        family = get_object_or_404(Family, slug=self.kwargs["slug"])
        
        context["family"] = family
        return context
