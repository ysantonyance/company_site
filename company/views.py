from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Branch, Employee, IceCreamDonation, News, Task


def _parse_optional_int(value):
    if value is None:
        return None
    value = value.strip()
    return int(value) if value else None


def _parse_optional_date(value):
    if value is None:
        return None
    value = value.strip()
    return value or None


def index(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create_branch':
            Branch.objects.create(
                name=request.POST.get('name', '').strip(),
                city=request.POST.get('city', '').strip(),
                address=request.POST.get('address', '').strip(),
                opened_year=_parse_optional_int(request.POST.get('opened_year')),
                is_open=request.POST.get('is_open') == 'on',
            )
            messages.success(request, 'Филиал успешно добавлен!')

        elif action == 'update_branch':
            branch = get_object_or_404(Branch, id=request.POST.get('branch_id'))
            branch.name = request.POST.get('name', '').strip()
            branch.city = request.POST.get('city', '').strip()
            branch.address = request.POST.get('address', '').strip()
            branch.opened_year = _parse_optional_int(request.POST.get('opened_year'))
            branch.is_open = request.POST.get('is_open') == 'on'
            branch.save()
            messages.success(request, f'Данные филиала «{branch.name}» обновлены!')

        elif action == 'delete_branch':
            branch = get_object_or_404(Branch, id=request.POST.get('branch_id'))
            name = branch.name
            branch.delete()
            messages.success(request, f'Филиал «{name}» удалён.')

        elif action == 'create_employee':
            branch_id = request.POST.get('branch_id')
            branch = get_object_or_404(Branch, id=branch_id) if branch_id else None
            Employee.objects.create(
                full_name=request.POST.get('full_name', '').strip(),
                position=request.POST.get('position', '').strip(),
                branch=branch,
                salary=request.POST.get('salary'),
                is_active=request.POST.get('is_active') == 'on',
            )
            messages.success(request, 'Работник успешно добавлен!')

        elif action == 'update_employee':
            employee = get_object_or_404(Employee, id=request.POST.get('employee_id'))
            branch_id = request.POST.get('branch_id')
            employee.full_name = request.POST.get('full_name', '').strip()
            employee.position = request.POST.get('position', '').strip()
            employee.branch = get_object_or_404(Branch, id=branch_id) if branch_id else None
            employee.salary = request.POST.get('salary')
            employee.is_active = request.POST.get('is_active') == 'on'
            employee.save()
            messages.success(request, f'Данные работника «{employee.full_name}» обновлены!')

        elif action == 'delete_employee':
            employee = get_object_or_404(Employee, id=request.POST.get('employee_id'))
            full_name = employee.full_name
            employee.delete()
            messages.success(request, f'Работник «{full_name}» удалён.')

        elif action == 'create_news':
            author_id = request.POST.get('author_id')
            author = get_object_or_404(Employee, id=author_id) if author_id else None
            News.objects.create(
                title=request.POST.get('title', '').strip(),
                content=request.POST.get('content', '').strip(),
                author=author,
                is_published=request.POST.get('is_published') == 'on',
            )
            messages.success(request, 'Новость успешно опубликована!')

        elif action == 'update_news':
            news_item = get_object_or_404(News, id=request.POST.get('news_id'))
            author_id = request.POST.get('author_id')
            news_item.title = request.POST.get('title', '').strip()
            news_item.content = request.POST.get('content', '').strip()
            news_item.author = get_object_or_404(Employee, id=author_id) if author_id else None
            news_item.is_published = request.POST.get('is_published') == 'on'
            news_item.save()
            messages.success(request, f'Новость «{news_item.title}» обновлена!')

        elif action == 'delete_news':
            news_item = get_object_or_404(News, id=request.POST.get('news_id'))
            title = news_item.title
            news_item.delete()
            messages.success(request, f'Новость «{title}» удалена.')

        elif action == 'create_donation':
            branch_id = request.POST.get('branch_id')
            branch = get_object_or_404(Branch, id=branch_id) if branch_id else None
            donor_name = (request.POST.get('donor_name') or '').strip() or 'Аноним'
            flavor = (request.POST.get('ice_cream_flavor') or '').strip() or 'Пломбир'
            IceCreamDonation.objects.create(
                donor_name=donor_name,
                amount=request.POST.get('amount'),
                ice_cream_flavor=flavor,
                branch=branch,
            )
            messages.success(request, 'Донат на мороженое записан!')

        elif action == 'update_donation':
            donation = get_object_or_404(IceCreamDonation, id=request.POST.get('donation_id'))
            branch_id = request.POST.get('branch_id')
            donation.donor_name = (request.POST.get('donor_name') or '').strip() or 'Аноним'
            donation.amount = request.POST.get('amount')
            donation.ice_cream_flavor = (request.POST.get('ice_cream_flavor') or '').strip() or 'Пломбир'
            donation.branch = get_object_or_404(Branch, id=branch_id) if branch_id else None
            donation.save()
            messages.success(request, f'Запись о донате #{donation.id} обновлена!')

        elif action == 'delete_donation':
            donation = get_object_or_404(IceCreamDonation, id=request.POST.get('donation_id'))
            donation_id = donation.id
            donation.delete()
            messages.success(request, f'Запись о донате #{donation_id} удалена.')

        elif action == 'create_task':
            assignee = get_object_or_404(Employee, id=request.POST.get('assignee_id'))
            Task.objects.create(
                title=request.POST.get('title', '').strip(),
                assignee=assignee,
                priority=int(request.POST.get('priority', 1)),
                deadline=_parse_optional_date(request.POST.get('deadline')),
                is_done=request.POST.get('is_done') == 'on',
            )
            messages.success(request, 'Задача создана!')

        elif action == 'update_task':
            task = get_object_or_404(Task, id=request.POST.get('task_id'))
            task.title = request.POST.get('title', '').strip()
            task.assignee = get_object_or_404(Employee, id=request.POST.get('assignee_id'))
            task.priority = int(request.POST.get('priority', 1))
            task.deadline = _parse_optional_date(request.POST.get('deadline'))
            task.is_done = request.POST.get('is_done') == 'on'
            task.save()
            messages.success(request, f'Задача «{task.title}» обновлена!')

        elif action == 'delete_task':
            task = get_object_or_404(Task, id=request.POST.get('task_id'))
            title = task.title
            task.delete()
            messages.success(request, f'Задача «{title}» удалена.')

        return redirect('company_panel')

    branches = Branch.objects.prefetch_related('employees', 'donations').all().order_by('-id')
    employees = Employee.objects.select_related('branch').prefetch_related('tasks', 'news_posts').all().order_by('-id')
    news_list = News.objects.select_related('author').all().order_by('-id')
    donations = IceCreamDonation.objects.select_related('branch').all().order_by('-id')
    tasks = Task.objects.select_related('assignee').all().order_by('-id')

    return render(request, 'admin.html', {
        'branches': branches,
        'employees': employees,
        'news_list': news_list,
        'donations': donations,
        'tasks': tasks,
    })