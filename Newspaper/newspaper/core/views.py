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
from .forms import CustomUserCreationForm, CommentForm  
from django.contrib import messages
from django.db.models import Q  



def index(request):
    # Filtrar los artículos marcados como importantes y ordenarlos por fecha de publicación (más recientes primero)
    articles = Article.objects.filter(is_important=True).order_by('-published_date')

    # Configurar paginación para mostrar 4 artículos por página
    paginator = Paginator(articles, 4)
    page_number = request.GET.get('page', 1)  # Obtener el número de página desde los parámetros GET

    # Manejar excepciones en caso de que el número de página no sea válido
    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)  # Si no es un número, mostrar la primera página
    except EmptyPage:
        page = paginator.page(paginator.num_pages)  # Si el número de página es demasiado alto, mostrar la última página

    # Obtener el primer artículo destacado, si lo hay, ordenado por la fecha de publicación
    featured_article = Article.objects.filter(is_featured=True).order_by('-published_date').first()

    # Definir las categorías que queremos mostrar en el índice
    categories_to_show = ['Nacionales', 'Locales', 'Deportes', 'Policiales']
    categories = Category.objects.filter(name__in=categories_to_show)

    # Crear un diccionario para almacenar artículos por categoría, mostrando solo los 3 más recientes de cada una
    articles_by_category = {}
    for category in categories:
        articles_by_category[category.name] = Article.objects.filter(category=category).order_by('-published_date')[:3]

    # Renderizar la página de índice con la información de paginación, artículo destacado y los artículos por categoría
    return render(request, 'index.html', {
        'page': page,
        'featured_article': featured_article,
        'articles_by_category': articles_by_category,
    })


@login_required(login_url='iniciar_sesion')
def category_detail(request, category_name):
    # Obtener la categoría seleccionada o mostrar un error 404 si no existe
    category = get_object_or_404(Category, name=category_name)
    
    # Filtrar los artículos de la categoría seleccionada y ordenarlos por fecha de publicación
    articles = Article.objects.filter(category=category).order_by('-published_date')

    # Configurar la paginación para la categoría
    paginator = Paginator(articles, 4)
    page_number = request.GET.get('page', 1)
    
    # Manejar excepciones de paginación
    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)  # Mostrar primera página si el parámetro no es un número
    except EmptyPage:
        page = paginator.page(paginator.num_pages)  # Mostrar última página si el número es mayor al total de páginas

    # Renderizar la página de detalle de la categoría con la lista de artículos paginados
    return render(request, 'secciones.html', {
        'category': category,
        'page': page,
    })


@login_required(login_url='iniciar_sesion')
def article_detail(request, id):
    # Obtener el artículo por su ID o mostrar error 404 si no existe
    article_detail = get_object_or_404(Article, id=id)
    
    # Renderizar la página de detalles del artículo
    return render(request, 'articulo.html', {'article_detail': article_detail})


def iniciar_sesion(request):
    # Si el método es POST, se procesa el formulario de autenticación
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Obtener el usuario autenticado
            login(request, user)  # Iniciar sesión con el usuario
            
            # Redirigir a la página de administración si es staff o superusuario, sino redirigir al índice
            if user.is_superuser or user.is_staff:
                return redirect('/admin/') 
            else:
                return redirect('index')
        else:
            # Mostrar mensaje de error si las credenciales son incorrectas
            messages.error(request, "Error en el inicio de sesión. Revisa tu nombre de usuario y contraseña.")
    else:
        # Si el método es GET, se muestra el formulario de inicio de sesión vacío
        form = AuthenticationForm()

    # Renderizar la página de inicio de sesión
    return render(request, 'iniciar_sesion.html', {'form': form})


def cerrar_sesion(request):
    # Cerrar la sesión del usuario
    logout(request)
    
    # Redirigir a la página de inicio (índice)
    return redirect('index')


def registrarse(request):
    # Procesar el formulario de registro si el método es POST
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar el nuevo usuario
            messages.success(request, 'Tu cuenta ha sido creada exitosamente. ¡Ya puedes iniciar sesión!')
            return redirect('iniciar_sesion')  # Redirigir al inicio de sesión
        else:
            # Mostrar mensaje de error si el formulario no es válido
            messages.error(request, 'Hubo un error en el registro. Verifica los datos e inténtalo de nuevo.')
    else:
        # Mostrar el formulario vacío si el método es GET
        form = CustomUserCreationForm()

    # Renderizar la página de registro
    return render(request, 'registrarse.html', {'form': form})


@login_required(login_url='iniciar_sesion')
def article_detail_view(request, pk):
    # Obtener el artículo por su PK o mostrar error 404 si no existe
    article = get_object_or_404(Article, pk=pk)
    
    # Obtener los comentarios asociados al artículo
    comments = article.comments.all()
    
    # Inicializar el formulario de comentarios vacío
    form = CommentForm()

    # Si el método es POST, procesar el nuevo comentario
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)  # Crear el comentario sin guardar
            new_comment.article = article  # Asociar el comentario al artículo
            new_comment.user = request.user  # Asociar el comentario al usuario autenticado
            new_comment.save()  # Guardar el comentario
            return redirect('article_detail', pk=article.pk)  # Redirigir a la misma página de detalles del artículo

    # Renderizar la página de detalles del artículo con los comentarios y el formulario
    context = {
        'article_detail': article,
        'comments': comments,
        'form': form,
    }
    return render(request, 'articulo.html', context)




@login_required(login_url='iniciar_sesion')
def buscar_noticias(request):
    query = request.GET.get('q')  # Obtener el término de búsqueda desde los parámetros GET
    resultados = []

    if query:
        # Buscar en los campos 'title', 'lead', y 'body' que contengan el término buscado
        resultados = Article.objects.filter(
            Q(title__icontains=query) | Q(lead__icontains=query) | Q(body__icontains=query)
        ).order_by('-published_date')

    # Renderizar una plantilla de resultados con las noticias encontradas
    return render(request, 'buscar_noticias.html', {'resultados': resultados, 'query': query})