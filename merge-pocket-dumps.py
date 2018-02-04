#!/usr/bin/python3
import json
import sys

def make_object(status, complete, lst, err, search_meta, since):
    ''' Make a new object (a complete Pocket API response) '''
    return {'status':status, 'complete':complete, 'list':lst, 'error':err, 'search_meta':search_meta, 'since':since}

def add_to_list(tobj, sobj):
    ''' Mutates tobj to have all keys sobj has which tobj initially does not have. sobj is not modified '''
    for key in sobj.keys():
        if not (key in tobj.keys()):
            tobj[key] = sobj[key]

def merge_two_objects(obj1, obj2):
    ''' Create a new object (a complete Pocket API response) which is the union of the two input objects, date set to the latter '''
    since = obj1['since']
    if obj2['since'] > since:
        since = obj2['since']
    rlst = obj1['list']
    add_to_list(rlst, obj2['list'])
    return make_object(1, 1, rlst, None, {'search_type':'normal'}, since)

def make_dummy():
    ''' Create a dummy object (a complete Pocket API response) '''
    return make_object(0, 0, {}, None, None, 0)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("usage: {} [pocket.json...] > all-pocket-data.json".format(sys.argv[0]))
        sys.exit(0)
    dummy = make_dummy()
    for fname in sys.argv[1:]:
        with open(fname) as inf:
            dummy = merge_two_objects(dummy, json.load(inf))
    json.dump(dummy, sys.stdout, sort_keys=True)
    sys.exit(0)
