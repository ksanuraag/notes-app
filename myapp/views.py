from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q

def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('note_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def note_list(request):
    query = request.GET.get('q')  # get the search query from URL
    if query:
        notes = Note.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            user=request.user
        )
    else:
        notes = Note.objects.filter(user=request.user)
    return render(request, 'notelist.html', {'notes': notes, 'query': query})

@login_required
def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note_list')   # FIXED here
    else:
        form = NoteForm()
    return render(request, 'noteform.html', {'form': form})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')   # consistent
    else:
        form = NoteForm(instance=note)
    return render(request, 'noteform.html', {'form': form})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == "POST":
        note.delete()
        return redirect('note_list')
    return render(request, 'notedelete.html', {'note': note})
