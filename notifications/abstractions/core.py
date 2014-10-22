import json
import hashlib
from collections import namedtuple

from json_helpers import serialize_class, deserialize_class

from pubsub import pubsub

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
        self.renderings = renderings
        ## Properties the runtime may set
        ## This is user information so notification engines know where to route the notification
        self.email = None
        self.name = None

    def serialize(self):
        return json.dumps({'type':self.type, 
                           'renderings':self.renderings,
                           'email':self.email,
                           'name':self.name})


def route(type, target):
    pass

class NotificationType():
    def __init__(self, helptext, name, routing_hints):
        self.helptext = helptext
        self.name = name
        self.routing_hints = routing_hints
        self.id = "\t".join(helptext)

    def notify(self, target, renderings):
        #if not pubsub.route_exists(route(target, type)):
        #    route_notification(route(target, type))
        
        pubsub.put(Notification(self.name, target, ))

def register_notification_type(helptext, name, routing_hints):
    n = NotificationType(helptext, name, routing_hints)
    return n

def subscriptions():
    pass

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


## Set up routing
def create_routes():
    pass

#create_routes()
#n = register_notification_type("Bob wants to chat with you", ["social", "chat"], {'duration':'ephemeral'})
#n.notify("pmitros", renderings = {'short-text' : 'Someone wants to char with you'})
