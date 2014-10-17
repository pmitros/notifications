from abc import ABCMeta
from abc import abstractmethod
import collections
import uuid

class kvs:
    ''' Simple class for interfacing a KVS from Python. 

    Keys are strings. Values are JSON dictionaries. Values must support json.dump(). 

    It support multi-gets and multi-sets (d['a','b','c'])

    It allows one to add items without specifying a key. In this case, a key is automatically
    generated and returned. Note that multiple 
    '''
    def __getitem__(self, key):
        if isinstance(key, basestring):
            return self.get(key)
        # TODO: Handle iterables of strings. This is a bit awkward, since 
        # e.g. isinstance("hello", collections.Iterable)  ===>  True
        elif isinstance(key, list):
            if hasattr(self, 'multiget'):
                return self.multiget(key)
            else:
                return (self.get(k) for k in key)
        else:
            raise AttributeError("KVS requires a list or string as a key")

    def __setitem__(self, key, value):
        if isinstance(key, basestring):
            return self.set(key, value)
        elif isinstance(key, list):
            if hasattr(self, 'multiget'):
                return self.multiget(key, value)
            else:
                for (k,v) in zip(key, value):
                    self.set(k, v)
        else:
            raise AttributeError("KVS requires a list or string as a key")

    def __key(self, value, keytype):
        ''' Generate a key for the value. By default, this is the hash of the value. Note that
        '''
        if keytype == "GUID":
            ## *sigh* 
            ## UUID1 generates a unique UUID based on time+MAC+etc. Unfortunately, this leaks MAC addresses, which can lead to security issues. 
            ## UUID4 generates a random UUID. Unfortunately, this can lead to collisions in some settings (especially VMs). 
            ## UUID5 combines them through a SHA hash hopefully giving us something both unique and non-leaky. 
            return uuid.uuid5(uuid.uuid1(), uuid.uuid4().hex).hex
        elif keytype == "HASH":
            hash = hashlib.new('sha')
            hash.update(json.dumps(value, indent=2, sort_keys=True))
            return hash.hexdigest()

    def _additem(self, value, keytype):
        if isinstance(key, dict):
            key = self.__key(value, keytype)
        elif isinstance(key, list):
            key = [self.__key(i, keytype)  for i in value]
        else:
            raise AttributeError("Adding items requires either an item (dict) or a list of items")
        self[key] = value
        return key

    def add_mutable(self, value):
        ''' 
        Add a mutable item or set of items to the KVS. Return their keys. 
        '''
        return self._additem(value, keytype == "GUID")

    def add_immutable(self, value):
        ''' 
        Add an immutable item or set of items to the KVS. 
        Identical items may be stored in the same location. 
        '''
        return self._additem(value, keytype == "SHA")

class in_memory_kvs(kvs):
    def __init__(self):
        self.store = dict()

    def get(self, key):
        return self.store[key]
    
    def set(self, key, value):
        self.store[key] = value

class dynamo_kvs(kvs):
    def __init__(self):
        raise NotImplementedError

    def get(self, key):
        pass

    def set(self, key, value):
        pass

class sql_kvs(kvs):
    def __init__(self):
        raise NotImplementedError

    def get(self, key):
        pass

    def set(self, key, value):
        pass


if __name__ == '__main__': 
    kvs = in_memory_kvs()
    kvs[["hello", "bye"]] = ["Hi", "bye"]
    print kvs["bye"]
    kvs[kvs.add_mutable("Hi")]
