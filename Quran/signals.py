from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Invoice, StudentPaymentStatus


@receiver(post_save, sender=Invoice)
def create_payment_status_for_invoice(sender, instance, created, **kwargs):
    if not created:
        return

    # Avoid duplicates because of unique_together(student, month, year)
    StudentPaymentStatus.objects.get_or_create(
        student=instance.student,
        school=instance.school,
        month=instance.month,
        year=instance.year,
        defaults={
            "invoice": instance,
            "is_paid": True,
        }
    )
