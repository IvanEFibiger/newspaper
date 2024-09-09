from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import CustomUserCreationForm
from django.contrib import messages



def index(request):
    # Obtener todos los artículos ordenados por fecha de publicación más reciente
    articles = Article.objects.filter(is_important=True).order_by('-published_date')

    # Paginador: 4 artículos por página
    paginator = Paginator(articles, 4)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    # Artículo destacado
    featured_article = Article.objects.filter(is_featured=True).order_by('-published_date').first()

    # Filtrar artículos por categoría (4 artículos por cada una)
    categories = ['Mundo', 'Nacionales', 'Deportes', 'Policiales', 'Varias']
    articles_by_category = {}
    for category_name in categories:
        category = Category.objects.get(name=category_name)
        articles_by_category[category_name] = Article.objects.filter(category=category).order_by('-published_date')[:3]

    return render(request, 'index.html', {
        'page': page,  # Página actual para los artículos paginados
        'featured_article': featured_article,  # Artículo destacado
        'articles_by_category': articles_by_category,  # Artículos por categoría
    })



@login_required(login_url='iniciar_sesion')
def category_detail(request, category_name):
    # Obtener la categoría específica
    category = get_object_or_404(Category, name=category_name)
    articles = Article.objects.filter(category=category).order_by('-published_date')

    # Paginador: 4 artículos por página
    paginator = Paginator(articles, 4)
    page_number = request.GET.get('page', 1)
    
    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'secciones.html', {
        'category': category,
        'page': page,
    })




@login_required(login_url='iniciar_sesion')
def article_detail(request, id):
    # Obtener el artículo correspondiente usando el ID
    article_detail = get_object_or_404(Article, id=id)
    return render(request, 'articulo.html', {'article_detail': article_detail})


def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirigir según el tipo de usuario
            if user.is_superuser or user.is_staff:
                return redirect('/admin/') 
            else:
                return redirect('index')  

        else:
            messages.error(request, "Error en el inicio de sesión. Revisa tu nombre de usuario y contraseña.")
    else:
        form = AuthenticationForm()

    return render(request, 'iniciar_sesion.html', {'form': form})



def cerrar_sesion(request):
    logout(request)  
    return redirect('index') 



def registrarse(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu cuenta ha sido creada exitosamente. ¡Ya puedes iniciar sesión!')
            return redirect('iniciar_sesion')
        else:
            messages.error(request, 'Hubo un error en el registro. Verifica los datos e inténtalo de nuevo.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registrarse.html', {'form': form})