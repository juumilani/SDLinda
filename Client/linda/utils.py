import re

def bin_to_tuple(binary_data, has_op=True):
    if has_op:
        _pattern = '(out|rd|in)_\(\"([^"]*)\"\,\"([^"]*)\"\,\"([^"]*)\"\)'
    else:
        _pattern = '\(\"([^"]*)\"\,\"([^"]*)\"\,\"([^"]*)\"\)'
    m = re.findall(_pattern,binary_data.decode())

    return m

def tuple_to_bin(tuple_data, op):
    _msg_send = '%s_("%s","%s","%s")' % (op, tuple_data[0], tuple_data[1], tuple_data[2])
    return _msg_send.encode()

def list_to_bin(list_data):
    _msg_send = '['
    for tpl in list_data:
        _msg_send += '("%s","%s","%s")' % (tpl[0], tpl[1], tpl[2])
    _msg_send += ']'
    return _msg_send.encode()
