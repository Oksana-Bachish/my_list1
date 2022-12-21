from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryFrom
from django.contrib.auth.decorators import login_required


def index(request):
    """Домашняя страница приложения Superlists"""
    return render(request, 'Superlists_1/index.html')


@login_required
def topics(request):
    """Выводит список тем"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'Superlists_1/topics.html', context)


@login_required
def topic(request, topic_id):
    """Выводит одну тему и все ее записи"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'Superlists_1/topic.html', context)


@login_required
def new_topic(request):
    """Определяет новую форму"""
    if request.method != 'POST':
        # Данные не отправялись создается пустая строка
        form = TopicForm
    else:
        # Отправлены данные POST, обработать данные
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('Superlists_1:topics')
    # Вывести пустую строку или недействительную форму
    context = {'form': form}
    return render(request, 'Superlists_1/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # Данные не отправялись создается пустая строка
        form = EntryFrom
    else:
        # Отправлены данные POST, обработать данные
        form = EntryFrom(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('Superlists_1:topic', topic_id=topic_id)
    # Вывести пустую строку или недействительную форму
    context = {'topic': topic, 'form': form}
    return render(request, 'Superlists_1/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи
        form = EntryFrom(instance=entry)
    else:
        # Отправка данных POST; обработать данные
        form = EntryFrom(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('Superlists_1:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'Superlists_1/edit_entry.html', context)
