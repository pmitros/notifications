'''
Helpers for converting between JSON objects and Python classes
'''

def serialize_class(o, attribute_list):
    '''
    Dump the object to a JSON dictionary. attribute_list is the list of relevant attributes. 
    '''
    json_dict ={}
    for a in attribute_list:
        json_dict[a] = getattr(o, a, None)
    return json_dict

def deserialize_class(o, json_dict, attribute_list):
    '''
    Update object from a JSON dictionary. attribute_list is the list of allowed attributes. 
    '''
    for a in json_dict:
        if a not in attribute_list:
            warnings.warn("Unknown attribute {a}. This most likely means a versioning issue, but it may be a suspicious operation.".format(a=a) )
        setattr(o, a, json_dict[a])
    return json_dict

# Tests
if __name__ == '__main__':
    class foo:
        bif = None
        bar = None
        biz = None

    source = foo()
    dest = foo()
    source.bif = 7
    source.bar = 5
    source.biz = 8

    j = serialize_class(source, ['bif', 'bar', 'unk'])
    deserialize_class(dest, j, ['bif', 'bar', 'unk'])
    assert [dest.bif, dest.bar, dest.biz] == [7,5,None]



