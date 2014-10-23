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
    def __str__(self):
        return self.category+':'+self.name

class Notification():
    attribute_list = ['type','renderings','email','name']

    def __init__(self, type=None, target=None, renderings=None):
        ## Properties the sender sets.
        self.type = type
        self.renderings = renderings
        ## Properties the runtime may set
        ## This is user information so notification engines know where to route the notification
        self.email = None
        self.name = None

    def serialize(self):
        return serialize_class(self, Notification.attribute_list)

    def deserialize(cls, json_dict):
        n = Notification()
        return deserialize_class(n, json_dict, Notification.attribute_list)

    def topic(self):
        h = hashlib.new('sha') # TODO: Add salt if on SQS?
        h.update("\t".join(self.target))
        h.update("\n")
        h.update("\t".join(self.type))
        return h.hexdigest()

    def mark_as_read(notification):
        pass

    def mark_as_read(notification):
        pass


def route(type, target):
    pass

class NotificationType():
    def __init__(self, helptext, name, routing_hints):
        self.helptext = helptext
        self.name = name
        self.routing_hints = routing_hints
        self.id = "\t".join(helptext)

    def notify(self, target, renderings):
        pass
        #pubsub.send()
        #pubsub.send(Notification(self.name, target, ))

def get_notification_type(name):
    return None

def register_notification_type(helptext, name, routing_hints):
    n = NotificationType(helptext, name, routing_hints)
    return n

def subscriptions():
    pass

def notifications(user):
    pass

def unread_notifications(user):
    pass

def subscribe(channel, channel_info):
    '''
    Get Add a subscription to the system if not there. Other
    '''
    pass

## Set up routing
def create_routes():
    pass

## Set up handlers
es = get_subscription("email")
if not es:
    es = subscribe("email")
eb = get_subscription("browser")
if not eb:
    eb = subscribe("browser")

## Example of how this would be used
create_routes()

## Send two notifications
notification_type = ["social", "chat"]
n = get_notification_type(notification_type)
if not n:
    n = register_notification_type("Bob wants to chat with you", ["social", "chat"], {'duration':'ephemeral'})
n.notify("pmitros", renderings = {'short-text' : 'Bob wants to chat with you'})
n.notify("pmitros", renderings = {'short-text' : 'Jill wants to chat with you'})

## Receive notifications
for user in es.users:
    print "Digest for ", user.username
    for notification in user.notifications:
        print notification
