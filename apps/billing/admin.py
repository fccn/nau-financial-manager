from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from apps.billing.models import SageX3TransactionInformation, Transaction, TransactionItem
from apps.billing.services.transaction_service import TransactionService


class TransactionItemInline(admin.TabularInline):
    model = TransactionItem
    extra = 0


class TransactionAdmin(admin.ModelAdmin):
    inlines = [TransactionItemInline]
    list_display = (
        "transaction_id",
        "client_name",
        "email",
    )
    search_fields = (
        "transaction_id",
        "client_name",
        "email",
    )


admin.site.register(Transaction, TransactionAdmin)


class SageX3TransactionInformationAdmin(admin.ModelAdmin):
    list_display = (
        "transaction",
        "status",
        "retries",
    )
    list_filter = [
        "status",
    ]
    search_fields = (
        "transaction_id",
        "status",
    )

    @admin.action(description="Retry to SageX3")
    def retry_sage_transaction(self, request, queryset):
        for sageX3TransactionInformation in queryset:
            transaction = sageX3TransactionInformation.transaction
            transaction_id = sageX3TransactionInformation.transaction.transaction_id
            if TransactionService(transaction).run_steps_to_send_transaction():
                self.message_user(
                    request,
                    _(
                        "%s transaction was successfully retried.",
                    )
                    % transaction_id,
                    messages.SUCCESS,
                )
            else:
                self.message_user(
                    request,
                    _(
                        "The %s transaction has raised an error while retrying.",
                    )
                    % transaction_id,
                    messages.ERROR,
                )

    actions = [retry_sage_transaction]


admin.site.register(SageX3TransactionInformation, SageX3TransactionInformationAdmin)
