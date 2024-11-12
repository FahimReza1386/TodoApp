from core.celery import app
from time import sleep
from .models import Todo
from accounts.models import User

@app.task
def del_ticked_task():
    todo=Todo.objects.filter(Ticked=True)
    todo.delete()
    return True



# Run Beat By Docker

# docker-compose exec backend sh -c "celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler"