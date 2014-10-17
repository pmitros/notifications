import hashlib
from collections import namedtuple

class NotificationTarget(namedtuple('Target', ['category', 'name'])):
    '''
    Target of a notification. 
    category is typically a "user"
    name is typically a username

    In the future, category could be cohort, class, etc.
    '''
    pass

def queuename(notification):
    h = hashlib.new('sha')
    # TODO: Add salt if on SQS?
    h.update("\t".join(notification.target))
    h.update("\n")
    h.update("\t".join(notification.type))
    return h.hexdigest()

class Notification():
    def __init__(self, type, target, renderings):
        ## Properties the sender sets.
        self.type = type
        self.target = target
        self.renderings = renderings
        ## Properties the runtime may set
        ## This is user information so notification engines know where to route the notification
        self.email = None
        self.name = None

class NotificationType():
    def __init__(self, help, description, routing_hints):
        self.help = help
        self.description = description
        self.routing_hints = routing_hints
        self.id = "\t".join(help)

def subscriptions():
    return ["a", "b", "c"]

def notify(Notification):
    pass

def notifications(user):
    pass

def unread_notifications(user):
    pass

def mark_as_read(notification):
    pass

def mark_as_read(notification):
    pass
