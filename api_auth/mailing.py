from django.contrib.auth.tokens import (
    PasswordResetTokenGenerator,
    default_token_generator,
)
from django.core.mail import BadHeaderError, send_mail
from django.template.context_processors import request
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from six import text_type


class EmailConfirmTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)


email_confirm_token_generator = EmailConfirmTokenGenerator()


def get_email(email_template_name, current_site, user, token_generator):
    pipeline = {
        "email": user.email,
        "domain": current_site.domain,
        "site_name": "Website",
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user,
        "token": token_generator.make_token(user),
        "protocol": "http",
    }
    email = render_to_string(email_template_name, pipeline)
    return email


def send_reset_mail(user, current_site):
    subject = "Password Reset Requested"
    email_template_name = "api_auth/password_reset_email.txt"
    email = get_email(
        email_template_name, current_site, user, email_confirm_token_generator
    )
    try:
        send_mail(
            subject, email, "admin@example.com", [user.email], fail_silently=False
        )
    except BadHeaderError:
        pass


def send_confirm_mail(user, current_site):
    subject = "Email Confirm"
    email_template_name = "api_auth/confirm_email.txt"
    email = get_email(email_template_name, current_site, user, default_token_generator)
    try:
        send_mail(
            subject, email, "admin@example.com", [user.email], fail_silently=False
        )
    except BadHeaderError:
        pass
