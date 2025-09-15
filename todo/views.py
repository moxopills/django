from django.shortcuts import render
from django.template.defaultfilters import title
from todo.models import Todo
from django.http import Http404

def todo_list(request):
    todo_list = Todo.objects.all().values_list('id','title')
    result =[{'id':todo[0], 'title':todo[1]} for i,todo in enumerate(todo_list)]
    return render(request, 'todo_list.html', {'data':result})

def todo_info(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        info = {
            'title': todo.title,
            'description': todo.description,
            'start_date': todo.start_date,
            'end_date': todo.end_date,
            'is_completed': todo.is_completed,
            'created_at': todo.created_at,
            'update_at': todo.updated_at
        }
        return render(request, 'todo_info.html', {'data': info})
    except Todo.DoesNotExist:
        raise Http404("Todo does not exist")
