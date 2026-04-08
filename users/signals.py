from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver #receiver helps listens to events and its a decorator
# from django.core.mail import send_mail
from utils.mail import send_smtp_mail



@receiver(post_save, sender=User)
def send_mail_with_template(sender, instance, created, **kwargs):
    print(instance)
    if created:
        # Send mail
        # send_mail(
        #     subject="Welcome to ReadMyBook.com",
        #     message="We are glad to accept you into our platform",
        #     from_email="andinizzy287@gmail.com",
        #     recipient_list=[instance.email],
        #     fail_silently=False
        # )
        send_smtp_mail(
            subject= " Welcome to ReadMyBook.com",
            from_email="andinizzy287@gmail.com",
            to=[instance.email],
            context={
                "header": f"{instance.first_name} {instance.last_name}",
                "description": "We are glad to have you with us.",
                "extra_info": "Let's get started.",
                "show_button": True,
                "button_text": "Get Started",
                "button_link": "http://localhost:3000/onboarding",
            }
        )






