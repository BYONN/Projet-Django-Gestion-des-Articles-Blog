from django.forms import TypedChoiceField
from unicodedata import category
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Article, Commentaire, Utilisateur, TypeContenu
from django.shortcuts import get_object_or_404
from django.db.models import Q
# Create your views here.

def home(request):
    return render(request, 'home.html')

def articles(request):
    getarticles = Article.objects.all()
    categories = TypeContenu.objects.all()

    query = request.GET.get('recherche','')
    categorie_id = request.GET.get('categorie', '')

    if query:
        getarticles = getarticles.filter(Q(titre__icontains=query) | Q(user__username__icontains=query))
    
    if categorie_id:
        getarticles = getarticles.filter(type_contenu_id = categorie_id)
    if request.user.is_authenticated:
        if request.user.role == 'Lecteur':
            getarticles = getarticles.filter(statut='Publié').order_by('-date_creation')
        else:
            getarticles = getarticles.order_by('-date_creation')
    else:
        getarticles = getarticles.filter(statut='Publié').order_by('-date_creation')
    
    context = {'articles':getarticles,
                'categories': categories,
                'selected_cat' : int(categorie_id) if categorie_id else None  
              }

    return render(request, 'articles.html',context)

def myarticles(request):
    getarticles = Article.objects.filter(user = request.user).order_by('-date_creation')
    if not request.user.role == 'Auteur' and not request.user.is_superuser:
            messages.error(request, 'Vous n\'avez pas le droit à acceder cet page')
            return redirect('home')
    context = {
        'articles' : getarticles
    }

    return render(request, 'mesarticles.html', context)

def article(request, article_id):
    getarticle = Article.objects.get(id=article_id)
    comments = Commentaire.objects.filter(article=article_id).order_by('-date_creation')
    context = {'article':getarticle,'comments':comments}
    return render(request, 'article.html',context)

def commentadd(request, article_id):
    if request.method == "POST":
        comment = Commentaire()
        comment.article = Article.objects.get(id=article_id)
        comment.user = request.user
        comment.texte = request.POST['texte']
        comment.save()
    return redirect('article', article_id=article_id)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
            return render(request, 'login.html')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        emailaddress = request.POST['email']
        pass_word = request.POST['password']
        pass_word2 = request.POST['password2']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        if Utilisateur.objects.filter(username=user_name).exists():
            messages.error(request, 'Un compte avec ce nom d\'utilisateur existe déja!')
            return render(request, 'register.html')

        if pass_word != pass_word2:
           messages.error(request, 'Le mot de passe ne correspond pas')
           return render(request, 'register.html')

        user = Utilisateur.objects.create_user(
            username=user_name,
            email=emailaddress,
            password = pass_word,
            first_name = first_name,
            last_name = last_name
        )

        messages.success(request, 'Compte créé avec succès! Veuillez vous connecter')
        return redirect('login')

    return render(request, 'register.html')

def profile(request, user_name):
    utilisateur = get_object_or_404(Utilisateur,username=user_name)

    if request.method == 'POST' and request.user == utilisateur:
        utilisateur.biographie = request.POST.get('biographie', '')
        utilisateur.save()
        messages.success(request, 'Biographie mise à jour avec succés!')
        return redirect('profile',user_name=utilisateur.username)

    user_articles = Article.objects.filter(user=utilisateur).order_by('-date_creation')

    context = {
        'utilisateur' : utilisateur,
        'articles' : user_articles
    }

    return render(request, 'profile.html', context)

def addarticle(request):
    if not request.user.is_authenticated or (request.user.role != 'Auteur' and not request.user.is_superuser):
        messages.error(request, "Vous n'avez pas la permission de créer un article.")
        return redirect('home')

    if request.method == 'POST':
        titre = request.POST['titre']
        contenu = request.POST['contenu']
        type_id = request.POST['type_contenu']
        statut = request.POST['statut']

        articletype = TypeContenu.objects.get(id=type_id)

        newarticle = Article(titre=titre,
        contenu = contenu,
        type_contenu = articletype,
        statut = statut,
        user = request.user)
        newarticle.save()

        return redirect('article',article_id = newarticle.id)
    
    categories = TypeContenu.objects.all()
    context = {'categories': categories}
    return render(request, 'addarticle.html', context)

def editarticle(request, article_id):
    getarticle = get_object_or_404(Article,id=article_id)

    if request.user != getarticle.user and not request.user.is_superuser:
        messages.error(request, "Vous ne pouvez pas modifier cet article.")
        return redirect('home')
    
    if request.method == 'POST':
        getarticle.titre = request.POST['titre']
        getarticle.contenu = request.POST['contenu']
        getarticle.statut = request.POST['statut']

        type_id = request.POST['type_contenu']
        getarticle.type_contenu = TypeContenu.objects.get(id=type_id)

        getarticle.save()

        messages.success(request, 'Article modifié avec succès!')
        return redirect('article',article_id=getarticle.id)

    categories = TypeContenu.objects.all()
    context = {
        'article': getarticle,
        'categories': categories
    }
    return render(request,'editarticle.html',context)

def deletearticle(request, article_id):
    getarticle = get_object_or_404(Article, id=article_id)

    if request.user != getarticle.user and not request.user.is_superuser:
        messages.error(request, "Vous ne pouvez pas supprimer cet article.")
        return redirect('home')

    getarticle.delete()

    messages.success(request, 'Article supprimé avec succès!')

    return redirect('myarticles')
