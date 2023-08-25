from django.contrib import admin

from core.billing.models import Receipt, ReceiptItem


class ReceiptItemInline(admin.TabularInline):
    model = ReceiptItem
    extra = 0


class ReceiptAdmin(admin.ModelAdmin):
    inlines = [ReceiptItemInline]
    list_display = ('name', 'email', 'address', 'vat_identification_country', 'vat_identification_number',
                    'total_amount_exclude_vat', 'total_amount_include_vat', 'receipt_link', 'receipt_document_id')
    search_fields = ('name', 'email', 'address', 'vat_identification_country', 'vat_identification_number',
                     'total_amount_exclude_vat', 'total_amount_include_vat', 'receipt_link', 'receipt_document_id')
    

admin.site.register(Receipt, ReceiptAdmin)