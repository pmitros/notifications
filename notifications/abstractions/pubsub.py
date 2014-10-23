import collections
from Queue import Queue, Empty

class InMemoryPubsub:
    '''
    Very minimalistic in-memory pub-sub. This is not designed for
    thread safety, performance, etc., but it is convenient for testing
    and debugging.

    topic, subscriber, and items are strings.

    The structure is simple. There is a dictionary of topics, and a
    dictionary of subscribers. The dictionary keys are strings. The
    entries are lists of queues (Queue.Queue). Went sending to a topic, 
    we send to all the queues in that list. When a subscriber listens, 
    they dequeue from all of the queues they subscribe to. For example, 
    if we have topics t1, t2, t3, and subscriber: 
      s1 subscribed to t1+t2
      s2 subscribed to t1+t2
      s3 subscribed to t3

    We would have: 
      subscribers = {'s1': [q11, q12], 's2':[q21, q22], 's3':[q33]}
      topics = {'t1' : [q11, q21], 't2':[q12, q22], 't3':[q33]}

    Where qnm is a Queue.Queue which connects subcriber n to topic m. 

    An alternative implementation would be to have one queue per 
    subscriber. The queues are independent so that subscribers can 
    independently pull from different topics. This is important for some 
    use cases, such as e-mail digests. 
    '''
    def __init__(self):
        '''
        Created defaultdicts for topics and subscribers. With no
        subscription, we get an empty list.
        '''
        self._subscribers = collections.defaultdict(lambda : list())
        self._topics = collections.defaultdict(lambda : list())

    def subscribe(self, topic, subscriber):
        '''
        Set up a pubsub route.

        Should not be called twice with same topic/subscriber. In 
        the current version, this is a noop, but this is not an interface guarantee. 
        '''
        if self._find_queue(topic, subscriber):
            return
        q = Queue()
        self._subscribers[subscriber].append(q)
        self._topics[topic].append(q)
        
    def unsubscribe(self, topic, subscriber):
        '''
        Remove a pubsub route.

        Should not be called if route doesn't exist (at least until
        we've understood how to build this on other technologies). In
        the current version, this is a noop, but this is not an
        interface guarantee.

        '''
        q = self._find_queue(topic, subscriber)
        if not q:
            return
        self._subscribers[subscriber].remove(q)
        self._topics[topic].remove(q)
        
    def send(self, topic, items):
        '''
        Send items to a given topic.
        '''
        for item in items:
            for queue in self._topics[topic]:
                queue.put(item)

    def subscriptions(self, subscriber):
        '''
        Returns an iteration over the subscribitions for a given subscriber. 
        
        Each subscription can be iterated over to get the items associated with that subscription.
        '''
        for subscription in self._subscribers[subscriber]:
            yield iter(lambda : self._get_queue_item(subscription), None)

    def _get_queue_item(self, queue):
        '''
        Grab an item from a queue. Return None otherwise.
        '''
        try:
            item = queue.get(False)
            return item
        except Empty:
            return None

    def _find_queue(self, topic, subscriber):
        '''
        Find the Queue.Queue routing between topic and subscriber
        '''
        for item in self._topics[topic]:
            if item in self._subscribers[subscriber]:
                return item
        return None

    def _queue_topic(self, queue):
        '''
        Grab the topic associated with a given queue. 
        '''
        for topic in self._topics:
            if queue in self._topics[topic]:
                return topic
        return None

    def _queue_subscriber(self, queue):
        '''
        Grab the subscriber associated with a given queue. 
        '''
        for subscriber in self._subscribers:
            if queue in self._subscribers[subscriber]:
                return subscriber
        return None

 
pubsub = InMemoryPubsub()

if __name__ == '__main__':
    pubsub.subscribe("topic", "client1")
    pubsub.subscribe("topic", "client2")
    pubsub.send("topic", ["Hello"])
    pubsub.send("topic", ["Goodbye"])
    items = list(pubsub.subscriptions("client1"))[0]
    assert list(items) == ['Hello', 'Goodbye']
    items = list(pubsub.subscriptions("client1"))[0]
    assert list(items) == []
    items = list(pubsub.subscriptions("client2"))[0]
    assert list(items) == ['Hello', 'Goodbye']
