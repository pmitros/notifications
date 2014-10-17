These are the abstractions used by the notification service. Nothing
here is Django-specific (although several may have an optional Django
ORM implementation).

The abstractions are: 

* Key value store
* Pub/sub queuing service
* 