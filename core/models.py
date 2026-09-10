from django.db import models
from django.db.models import Sum


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Investor(TimeStampedModel):
	name = models.CharField(max_length=150, verbose_name='الاسم')
	phone = models.CharField(max_length=30, blank=True, verbose_name='الهاتف')
	email = models.EmailField(blank=True, verbose_name='البريد الإلكتروني')
	is_main = models.BooleanField(default=False, verbose_name='المستثمر الرئيسي')
	is_active = models.BooleanField(default=True, verbose_name='نشط')

	class Meta:
		ordering = ['name']
		verbose_name = 'مساهم'
		verbose_name_plural = 'المساهمون'

	def __str__(self):
		return self.name

	@property
	def total_contribution(self):
		return self.contributions.aggregate(total=Sum('amount'))['total'] or 0

	@property
	def project_count(self):
		return self.contributions.values('project_id').distinct().count()


class Land(TimeStampedModel):
	identifier = models.CharField(max_length=80, unique=True, verbose_name='معرف الأرض')
	location = models.CharField(max_length=200, verbose_name='الموقع')
	area = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='المساحة')
	purchase_price = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='سعر الشراء')
	seller_name = models.CharField(max_length=150, verbose_name='البائع')
	purchased_at = models.DateTimeField(verbose_name='تاريخ الشراء')
	notes = models.TextField(blank=True, verbose_name='ملاحظات')

	class Meta:
		ordering = ['-purchased_at']
		verbose_name = 'أرض'
		verbose_name_plural = 'الأراضي'

	def __str__(self):
		return f'{self.identifier} - {self.location}'


class Project(TimeStampedModel):
	class Status(models.TextChoices):
		PLANNING = 'planning', 'تخطيط'
		BUILDING = 'building', 'قيد الإنشاء'
		READY = 'ready', 'جاهز للبيع'
		SOLD = 'sold', 'تم البيع'
		CLOSED = 'closed', 'مغلق'

	name = models.CharField(max_length=180, verbose_name='اسم المشروع')
	land = models.OneToOneField(Land, on_delete=models.PROTECT, related_name='project', verbose_name='الأرض')
	start_date = models.DateField(verbose_name='تاريخ البداية')
	end_date = models.DateField(blank=True, null=True, verbose_name='تاريخ الانتهاء')
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNING, verbose_name='الحالة')
	main_investor_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=30, verbose_name='نسبة المستثمر الرئيسي')
	notes = models.TextField(blank=True, verbose_name='ملاحظات')

	class Meta:
		ordering = ['-created_at']
		verbose_name = 'مشروع'
		verbose_name_plural = 'المشاريع'

	def __str__(self):
		return self.name

	@property
	def total_contributions(self):
		return self.contributions.aggregate(total=Sum('amount'))['total'] or 0

	@property
	def total_expenses(self):
		return self.expenses.aggregate(total=Sum('amount'))['total'] or 0

	@property
	def total_sales(self):
		return self.sales.aggregate(total=Sum('sale_price'))['total'] or 0

	@property
	def net_profit(self):
		return self.total_sales - self.total_expenses

	@property
	def main_investor_profit(self):
		return self.net_profit * self.main_investor_percentage / 100


class ProjectContribution(TimeStampedModel):
	investor = models.ForeignKey(Investor, on_delete=models.PROTECT, related_name='contributions', verbose_name='المساهم')
	project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='contributions', verbose_name='المشروع')
	amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='المبلغ')
	operation_type = models.CharField(max_length=30, default='مساهمة', verbose_name='نوع العملية')
	notes = models.TextField(blank=True, verbose_name='ملاحظات')

	class Meta:
		ordering = ['-created_at']
		verbose_name = 'مساهمة في مشروع'
		verbose_name_plural = 'مساهمات المشاريع'


class FinancialTransaction(TimeStampedModel):
	class Type(models.TextChoices):
		DEPOSIT = 'deposit', 'إيداع'
		WITHDRAWAL = 'withdrawal', 'سحب'
		CONTRIBUTION = 'contribution', 'مساهمة'
		PROFIT = 'profit', 'توزيع أرباح'
		EXPENSE = 'expense', 'مصروف'
		SALE = 'sale', 'بيع'

	investor = models.ForeignKey(Investor, on_delete=models.PROTECT, related_name='transactions', null=True, blank=True, verbose_name='المساهم')
	project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='transactions', null=True, blank=True, verbose_name='المشروع')
	transaction_type = models.CharField(max_length=20, choices=Type.choices, verbose_name='نوع العملية')
	amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='المبلغ')
	balance_before = models.DecimalField(max_digits=14, decimal_places=2, default=0, verbose_name='الرصيد قبل العملية')
	balance_after = models.DecimalField(max_digits=14, decimal_places=2, default=0, verbose_name='الرصيد بعد العملية')
	notes = models.TextField(blank=True, verbose_name='ملاحظات')

	class Meta:
		ordering = ['-created_at']
		verbose_name = 'عملية مالية'
		verbose_name_plural = 'العمليات المالية'


class Expense(TimeStampedModel):
	project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='expenses', verbose_name='المشروع')
	category = models.CharField(max_length=100, verbose_name='نوع التكلفة')
	beneficiary = models.CharField(max_length=150, verbose_name='المستفيد')
	amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='المبلغ')
	payment_method = models.CharField(max_length=60, verbose_name='طريقة الدفع')
	notes = models.TextField(blank=True, verbose_name='ملاحظات')

	class Meta:
		ordering = ['-created_at']
		verbose_name = 'مصروف'
		verbose_name_plural = 'المصروفات'

	def __str__(self):
		return f'{self.category} - {self.project.name} - {self.amount:,.0f} ر.ي'


class Sale(TimeStampedModel):
	project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='sales', verbose_name='المشروع')
	unit = models.CharField(max_length=100, blank=True, verbose_name='الوحدة')
	buyer_name = models.CharField(max_length=150, verbose_name='المشتري')
	sale_price = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='سعر البيع')
	paid_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, verbose_name='المدفوع')
	remaining_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, verbose_name='المتبقي')
	payment_method = models.CharField(max_length=60, verbose_name='طريقة الدفع')
	sold_at = models.DateTimeField(verbose_name='تاريخ البيع')
	notes = models.TextField(blank=True, verbose_name='ملاحظات')

	class Meta:
		ordering = ['-sold_at']
		verbose_name = 'عملية بيع'
		verbose_name_plural = 'المبيعات'

	def __str__(self):
		unit_name = self.unit or 'بيع المشروع بالكامل'
		return f'{unit_name} - {self.buyer_name} - {self.sale_price:,.0f} ر.ي'


class ProfitDistribution(TimeStampedModel):
	investor = models.ForeignKey(Investor, on_delete=models.PROTECT, related_name='profit_distributions', verbose_name='المساهم')
	project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='profit_distributions', verbose_name='المشروع')
	contribution_value = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='قيمة المساهمة')
	contribution_percentage = models.DecimalField(max_digits=7, decimal_places=3, verbose_name='نسبة المساهمة')
	profit_amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='الربح المستحق')
	distributed_at = models.DateTimeField(verbose_name='تاريخ التوزيع')

	class Meta:
		ordering = ['-distributed_at']
		verbose_name = 'توزيع أرباح'
		verbose_name_plural = 'توزيعات الأرباح'

	def __str__(self):
		return f'{self.investor.name} - {self.project.name} - {self.profit_amount:,.0f} ر.ي'

# Create your models here.
