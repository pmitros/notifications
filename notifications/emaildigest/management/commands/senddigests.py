from django.core.management.base import BaseCommand

def email_body(item):
    for x in ['email','long-html','long-text','shoty-html','short-text']:
        if x in item.renderings:
            return item.renderings[x]
    raise AttributeError("Notification *must* hand a short-text.")

class Command(BaseCommand):
    option_list = BaseCommand.option_list
    help = "Send e-mail digests. This should be in a daily cron"

    def handle(self, **options):
        for subscription in subscriptions():
            items = list(subscription)
            if len(items) < 1:
                continue
            email = "\n".join(email_body(item) for item in items)
            subject = "Your daily digest!"
            email = items[0].email
            name = items[0].name
            send_mail(subject, body, "{name} <{email}>".format(name=name, email=email), [], fail_silently = True)
