from .forms import RegistroUsuarioForm
from django.contrib.auth.views import LoginView, LogoutView
#from django.contrib.auth import logout
from django.views.generic import CreateView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import Group
 
from .models import Usuario
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..posts.models import Comentario, Post
from django.contrib.auth.views import PasswordResetDoneView, PasswordChangeDoneView
# Create your views here.

class RegistrarUsuario(CreateView):
    template_name = 'registration/registrar.html'
    form_class = RegistroUsuarioForm
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registro exitoso. Porfavor, inicia sesión.')
        group = Group.objects.get(name='Registrado')
        self.object.groups.add(group)        
        return redirect('apps.usuario:registrar')

class LoginUsuario(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        messages.success(self.request, 'Iniciaste sesión')
        
        return reverse('apps.usuario:login')


class LogoutUsuario(LogoutView):
    template_name = 'registration/logout.html'
    
    
    def get_success_url(self):
        messages.success(self.request, 'Logout Exitoso')
        
        return reverse('apps.usuario:logout')
    
# Lo demas del apunte


class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    Temples_name ='usuario/usuario_list.html'
    context_object_name = 'usuario'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset =queryset.exclude(is_superuser=True)
        return queryset
    
class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    templete_name ='usuario/eliminar_usuario.html'
    success_url = reverse_lazy('apps.usuario:usuario_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        colaborador_group = Group.objects.get(name='Coloborador')
        es_coloborador = colaborador_group in self.object.group.all()
        context["es_coloborador"] = es_coloborador
        return context
    
    def post(self, request, *args, **kwargs):
        eliminar_comentario = request.POST.get('eliminar_comentario', False)
        eliminar_post = request.POST.get('eliminar_post', False)
        self.object = self.get_object()
        if eliminar_comentario:
            Comentario.object.filter(usuario=self.object).delete()
        
        if eliminar_post:
            Post.object.filter(autor=self.object).delete()
        messages.success(request, f'Usuario{self.object.username} eliminar correctamente')
        return self.delete(request, *args, **kwargs)


#Lo saque de internet para resetear la contraseña

# class PasswordResetDoneView(PasswordResetDoneView):
#    template_name = 'registration/password_reset_done.html'  





