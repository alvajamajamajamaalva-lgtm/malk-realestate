from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Expense, FinancialTransaction, Investor, Project, Sale


@login_required
def dashboard(request):
	projects = Project.objects.select_related('land').all()
	context = {
		'projects': projects[:6],
		'project_count': projects.count(),
		'investor_count': Investor.objects.filter(is_main=False).count(),
		'total_capital': projects.aggregate(total=Sum('contributions__amount'))['total'] or 0,
		'total_expenses': Expense.objects.aggregate(total=Sum('amount'))['total'] or 0,
		'total_sales': Sale.objects.aggregate(total=Sum('sale_price'))['total'] or 0,
		'transactions': FinancialTransaction.objects.select_related('investor', 'project')[:8],
	}
	context['net_profit'] = context['total_sales'] - context['total_expenses']
	return render(request, 'core/dashboard.html', context)


@login_required
def project_list(request):
	projects = Project.objects.select_related('land').all()
	return render(request, 'core/project_list.html', {'projects': projects})


@login_required
def investor_list(request):
	investors = Investor.objects.filter(is_main=False).all()
	return render(request, 'core/investor_list.html', {'investors': investors})


@login_required
def transaction_list(request):
	transactions = FinancialTransaction.objects.select_related('investor', 'project').all()
	return render(request, 'core/transaction_list.html', {'transactions': transactions})
from django.shortcuts import render

# Create your views here.
