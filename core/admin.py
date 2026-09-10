from django.contrib import admin

from .models import (
    Expense,
    FinancialTransaction,
    Investor,
    Land,
    Project,
    ProjectContribution,
    ProfitDistribution,
    Sale,
)

admin.site.site_header = 'مِلك | إدارة الاستثمار العقاري'
admin.site.site_title = 'مِلك'
admin.site.index_title = 'مركز إدارة المحفظة'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status_badge', 'land', 'start_date', 'capital_display', 'profit_display')
    list_filter = ('status', 'start_date')
    search_fields = ('name', 'land__location')
    list_per_page = 15

    @admin.display(description='الحالة')
    def status_badge(self, obj):
        return obj.get_status_display()

    @admin.display(description='رأس المال')
    def capital_display(self, obj):
        return f'{obj.total_contributions:,.0f} ر.ي'

    @admin.display(description='صافي الربح')
    def profit_display(self, obj):
        return f'{obj.net_profit:,.0f} ر.ي'


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'project_count', 'contribution_display', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_main')
    search_fields = ('name', 'phone', 'email')
    list_per_page = 15

    @admin.display(description='إجمالي المساهمة')
    def contribution_display(self, obj):
        return f'{obj.total_contribution:,.0f} ر.ي'


@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'location', 'area', 'purchase_price', 'seller_name', 'purchased_at')
    search_fields = ('identifier', 'location', 'seller_name')
    list_filter = ('purchased_at',)


@admin.register(ProjectContribution)
class ProjectContributionAdmin(admin.ModelAdmin):
    list_display = ('investor', 'project', 'amount', 'operation_type', 'created_at')
    list_filter = ('operation_type', 'project')
    search_fields = ('investor__name', 'project__name')
    list_per_page = 20


@admin.register(FinancialTransaction)
class FinancialTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'investor', 'project', 'amount', 'balance_after', 'created_at')
    list_filter = ('transaction_type', 'project', 'created_at')
    search_fields = ('investor__name', 'project__name', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'project', 'beneficiary', 'amount', 'payment_method', 'created_at')
    list_filter = ('category', 'payment_method', 'project')
    search_fields = ('category', 'beneficiary', 'project__name')
    list_per_page = 20


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('project', 'unit', 'buyer_name', 'sale_price', 'paid_amount', 'remaining_amount', 'sold_at')
    list_filter = ('payment_method', 'project', 'sold_at')
    search_fields = ('buyer_name', 'unit', 'project__name')
    list_per_page = 20


@admin.register(ProfitDistribution)
class ProfitDistributionAdmin(admin.ModelAdmin):
    list_display = ('investor', 'project', 'contribution_value', 'contribution_percentage', 'profit_amount', 'distributed_at')
    list_filter = ('project', 'distributed_at')
    search_fields = ('investor__name', 'project__name')
    list_per_page = 20
