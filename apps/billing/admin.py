from django.contrib import admin

from apps.billing.models import Receipt, ReceiptItem


class ReceiptItemInline(admin.TabularInline):
    model = ReceiptItem
    extra = 0


class ReceiptAdmin(admin.ModelAdmin):
    inlines = [ReceiptItemInline]
    list_display = (
        "transaction_id",
        "client_name",
        "email",
        "address_line_1",
        "address_line_2",
        "city",
        "postal_code",
        "state",
        "country_code",
        "vat_identification_number",
        "vat_identification_country",
        "total_amount_exclude_vat",
        "total_amount_include_vat",
        "currency",
    )
    search_fields = (
        "transaction_id",
        "client_name",
        "email",
        "address_line_1",
        "address_line_2",
        "city",
        "postal_code",
        "state",
        "country_code",
        "vat_identification_number",
        "vat_identification_country",
        "total_amount_exclude_vat",
        "total_amount_include_vat",
        "currency",
    )


admin.site.register(Receipt, ReceiptAdmin)
