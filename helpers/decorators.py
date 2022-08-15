from django.contrib.auth.decorators import user_passes_test

def check_email_status(user):
    return not user.is_email_verified

email_verified = user_passes_test(check_email_status, '/request-verification/', 'next')

def verification_required(viewfunc):
    return email_verified(viewfunc)