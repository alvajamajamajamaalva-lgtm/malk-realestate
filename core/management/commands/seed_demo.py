from datetime import date, datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import (
    Expense,
    FinancialTransaction,
    Investor,
    Land,
    Project,
    ProjectContribution,
    Sale,
)


class Command(BaseCommand):
    help = 'إنشاء بيانات تجريبية بسيطة لنظام الاستثمار العقاري'

    def handle(self, *args, **options):
        main_investor, _ = Investor.objects.get_or_create(
            name='أحمد إبراهيم',
            defaults={'phone': '0500000000', 'is_main': True},
        )
        first_investor, _ = Investor.objects.get_or_create(
            name='محمد العتيبي',
            defaults={'phone': '0500000001'},
        )
        second_investor, _ = Investor.objects.get_or_create(
            name='سارة القحطاني',
            defaults={'phone': '0500000002'},
        )

        land_one, _ = Land.objects.get_or_create(
            identifier='أرض-001',
            defaults={
                'location': 'حي الياسمين - الرياض',
                'area': Decimal('650'),
                'purchase_price': Decimal('900000'),
                'seller_name': 'شركة العقار الحديث',
                'purchased_at': timezone.make_aware(datetime(2024, 1, 10, 10, 0)),
            },
        )
        land_two, _ = Land.objects.get_or_create(
            identifier='أرض-002',
            defaults={
                'location': 'حي الملقا - الرياض',
                'area': Decimal('800'),
                'purchase_price': Decimal('1200000'),
                'seller_name': 'مؤسسة الواجهة',
                'purchased_at': timezone.make_aware(datetime(2024, 3, 5, 11, 30)),
            },
        )

        project_one, _ = Project.objects.get_or_create(
            name='عمارة النخيل السكنية',
            defaults={
                'land': land_one,
                'start_date': date(2024, 2, 1),
                'status': Project.Status.READY,
                'main_investor_percentage': Decimal('30'),
            },
        )
        project_two, _ = Project.objects.get_or_create(
            name='فلل الندى',
            defaults={
                'land': land_two,
                'start_date': date(2024, 4, 1),
                'status': Project.Status.BUILDING,
                'main_investor_percentage': Decimal('30'),
            },
        )

        contributions = [
            (first_investor, project_one, Decimal('780000')),
            (second_investor, project_one, Decimal('540000')),
            (first_investor, project_two, Decimal('420000')),
            (second_investor, project_two, Decimal('250000')),
        ]
        for investor, project, amount in contributions:
            ProjectContribution.objects.get_or_create(
                investor=investor,
                project=project,
                amount=amount,
                defaults={'operation_type': 'مساهمة أولية'},
            )

        Expense.objects.get_or_create(
            project=project_one,
            category='تكاليف البناء',
            beneficiary='شركة أساس للمقاولات',
            amount=Decimal('950000'),
            defaults={'payment_method': 'تحويل بنكي'},
        )
        Expense.objects.get_or_create(
            project=project_two,
            category='مواد بناء',
            beneficiary='مؤسسة البناء المتين',
            amount=Decimal('680000'),
            defaults={'payment_method': 'حوالة'},
        )

        sale, _ = Sale.objects.get_or_create(
            project=project_one,
            unit='الشقة 101',
            defaults={
                'buyer_name': 'خالد المطيري',
                'sale_price': Decimal('1250000'),
                'paid_amount': Decimal('750000'),
                'remaining_amount': Decimal('500000'),
                'payment_method': 'دفعة أولى',
                'sold_at': timezone.make_aware(datetime(2024, 9, 15, 9, 0)),
            },
        )

        FinancialTransaction.objects.get_or_create(
            investor=first_investor,
            project=project_one,
            transaction_type=FinancialTransaction.Type.CONTRIBUTION,
            amount=Decimal('780000'),
            defaults={'notes': 'مساهمة أولية في عمارة النخيل'},
        )
        FinancialTransaction.objects.get_or_create(
            investor=second_investor,
            project=project_two,
            transaction_type=FinancialTransaction.Type.CONTRIBUTION,
            amount=Decimal('250000'),
            defaults={'notes': 'مساهمة أولية في فلل الندى'},
        )
        FinancialTransaction.objects.get_or_create(
            project=project_one,
            transaction_type=FinancialTransaction.Type.SALE,
            amount=sale.paid_amount,
            defaults={'notes': 'دفعة بيع الشقة 101'},
        )

        self.stdout.write(self.style.SUCCESS('تم تجهيز البيانات التجريبية بنجاح.'))
        self.stdout.write('المشاريع: عمارة النخيل السكنية، فلل الندى')
        self.stdout.write('يمكنك فتح لوحة الإدارة لإضافة أو تعديل البيانات.')
