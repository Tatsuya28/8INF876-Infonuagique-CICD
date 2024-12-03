from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, User
from django.contrib import messages


def task_list(request):
    if "user_id" in request.session:
        user = User.objects.get(id=request.session["user_id"])
        # tasks = Task.objects.filter(user_id=request.session["user_id"]).order_by('due_date')
        uncompleted_tasks = Task.objects.filter(user_id=request.session["user_id"], completed=False).order_by('due_date')
        completed_tasks = Task.objects.filter(user_id=request.session["user_id"], completed=True).order_by('due_date')


        return render(request, 'tasks/task_list.html', {'uncompleted_tasks': uncompleted_tasks, 'completed_tasks': completed_tasks, 'user': user})

    return redirect('login')



def add_task(request):
    if "user_id" not in request.session:  # Vérifie si l'utilisateur est connecté via la session
        return redirect('login')  # Redirige vers la page de connexion si non connecté

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        due_date = request.POST.get('due_date', None)

        # Récupère l'utilisateur connecté via la session
        user = User.objects.get(id=request.session['user_id'])

        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            user=user  # Associe la tâche à l'utilisateur récupéré via la session
        )
        return redirect('task_list')

    return render(request, 'tasks/add_task.html')


def edit_task(request):
    if "user_id" not in request.session:  # Vérifie si l'utilisateur est connecté via la session
        return redirect('login')  # Redirige vers la page de connexion si non connecté

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = get_object_or_404(Task, id=task_id)

        task.title = request.POST['title']
        task.description = request.POST.get('description', '')
        task.due_date = request.POST.get('due_date', None)
        task.completed = 'completed' in request.POST
        task.save()
        return redirect('task_list')

    elif request.method == 'GET':
        task_id = request.GET.get('task_id')
        if not task_id:
            return redirect('task_list')

        task = get_object_or_404(Task, id=task_id)
        return render(request, 'tasks/edit_task.html', {'task': task})


def delete_task(request):
    if "user_id" not in request.session:  # Vérifie si l'utilisateur est connecté via la session
        return redirect('login')  # Redirige vers la page de connexion si non connecté

    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        task.delete()
    return redirect('task_list')


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Vérifier que l'email n'est pas déjà présent dans la BDD
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        # Verifier si les mots de passe sont identiques
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        hashed_password = make_password(password)

        User.objects.create(name=name, email=email, password=hashed_password)
        messages.success(request, "Inscription réussie ! Vous pouvez maintenant vous connecter.")
        return redirect('login')
    return render(request, 'tasks/register.html')


def login(request):
    if request.method == 'POST':
        input_email = request.POST['email']
        input_password = request.POST['password']

        try:
            registered_user = User.objects.get(email=input_email)

            if check_password(input_password, registered_user.password):
                request.session['user_id'] = registered_user.id
                messages.success(request, "Vous êtes bien connecté!")
                return redirect('task_list')
            else:
                messages.error(request, "Votre identifiant ou mot de passe est incorrect")
        except User.DoesNotExist:
            messages.error(request, "Votre identifiant ou mot de passe est incorrect")

    return render(request, 'tasks/login.html')


def logout(request):
    if "user_id" in request.session:
        del request.session['user_id']
        messages.success(request, "Vous êtes déconnecté avec succès.")
    return redirect('login')
