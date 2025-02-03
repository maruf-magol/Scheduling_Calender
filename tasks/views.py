import calendar
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

# Home page view with calendar integration
def home(request):
    today = date.today()
    year, month = today.year, today.month
    cal = calendar.Calendar(firstweekday=5)  # Saturday as the first day

    # Generate days in the current month
    days = []
    for week in cal.monthdatescalendar(year, month):
        week_data = []
        for day in week:
            tasks = Task.objects.filter(due_date=day)  # Fetch tasks for this date
            week_data.append({
                "date": day.day if day.month == month else "",  # Show only current month days
                "past": day < today,
                "today": day == today,
                "tasks": tasks
            })
        days.append(week_data)

    # Get the current day name and formatted date
    current_day = today.strftime("%A")  # Get weekday name
    current_date = today.strftime("%B %d, %Y")  # Get formatted date (e.g., February 5, 2025)

    not_completed_tasks = Task.objects.filter(completed=False)
    completed_tasks = Task.objects.filter(completed=True)

    context = {
        'not_completed_tasks': not_completed_tasks,
        'completed_tasks': completed_tasks,
        'calendar': days,  # Passing calendar data to template
        'current_day': current_day,  # Pass weekday name
        'current_date': current_date,  # Pass formatted date
    }
    return render(request, 'tasks/home.html', context)

# Add New Task page view
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home page after saving the task
    else:
        form = TaskForm()
    
    return render(request, 'tasks/add_task.html', {'form': form})

# Detail view for a specific task
def task_details(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        if 'mark_as_done' in request.POST:
            task.completed = True
            task.save()
            return redirect('home')
        elif 'delete' in request.POST:
            task.delete()
            return redirect('home')
        elif 'save_changes' in request.POST:
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('task_details', task_id=task.id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_details.html', {'task': task, 'form': form})
