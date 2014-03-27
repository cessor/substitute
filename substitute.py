
__all__ = ['Substitute', 'ONCE', 'TWICE', 'MissingCallComplaint', 'CalledTooOftenComplaint', 'CalledTooRarelyComplaint', 'UndesiredCallComplaint', 'ArgumentMissmatchComplaint', 'WrongArgumentTypeComplaint', 'ComparableString']

__author__ = 'Johannes Hofmeister, http://twitter.com/@pro_cessor'
__version__ = '1.0.1'

from nose.tools import *

ONCE = 1
TWICE = 2

class Complaint(Exception):
    pass
class CalledTooOftenComplaint(Complaint):
    pass
class CalledTooRarelyComplaint(Complaint):
    pass
class MissingCallComplaint(Complaint):
    pass
class UndesiredCallComplaint(Complaint):
    pass
class ArgumentMissmatchComplaint(Complaint):
    pass
class WrongArgumentTypeComplaint(Complaint):
    pass

complaints = {
    -1: CalledTooRarelyComplaint,
    1: CalledTooOftenComplaint
}

def _pad(actual, expected):
    actual, expected= str(actual), str(expected)
    padding = max(len(actual), len(expected))
    return actual.ljust(padding), expected.ljust(padding)

_messages = {
    CalledTooRarelyComplaint: """\n\n\tThe method '{name}' was not called often enough!\n
    I expected {expected} calls but the method was called only {actual} time{s}

Expected: {pad_expected} x {name}(...)
Was:      {pad_actual} x {name}(...)
    """,
    CalledTooOftenComplaint: """\n\n\tThe method '{name}' was called too many times!\n
    I expected {expected} calls but the method was called {actual} time{s}

Expected: {pad_expected} x {name}(...)
Was:      {pad_actual} x {name}(...)
    """,
    ArgumentMissmatchComplaint: """\n\n\tThe method '{name}' was called with the wrong arguments!

Expected: {name}{expected} 
Received: {name}{actual}
""",
    MissingCallComplaint: """\n\n\tThe method '{name}' was not called at all!

Expected: 1 x {name}(...)
Was:      0 x {name}(...)
""",
    UndesiredCallComplaint: """\n\n\tThe method '{name}' was called which was unintended!

Expected: 0 x {name}(...)
Was:      1 x {name}(...)
""",
    WrongArgumentTypeComplaint : '''\n\n\tThe method '{name}' was called by the wrong signature!\n
The actual call was was: {name}({values})

Expected: {name}({types})
Received: {name}({call_parameter_types})
'''
}
def _message_for(complaint, **kwargs):
    message = _messages[complaint]
    message = message.format(**kwargs)
    return message

def _make(complaint, **kwargs):
    message = _message_for(complaint, **kwargs)
    return complaint(message)

class CallableOrValue(object):
    def __init__(self, parent, name):
        self._parent = parent
        self._name = name
        self._parameters = []

    def __call__(self, *args, **kwargs):
        # Raise an exception if configured
        exception = self._configured_exception()
        if exception:
            raise exception(self._name)
        # Register call parameters
        self._parameters = args
        self._register_call_for_later_checking()
        
        # Return configured values
        if self._has_return_values():
            return self._return_configured_values(args)     
        # Continue configuration
        return self

    def _configured_exception(self):
        return self._parent._exception_types.get(self._name, None)

    def _register_call_for_later_checking(self):
        self._parent._calls.append(self)

    def _has_return_values(self):
        return self._name in self._parent._data.keys()

    def _return_configured_values(self, current_call_parameters):
        canned_data = self._canned_data()
        # s.method.returns(123)
        if self._should_always_return(canned_data):
            return canned_data
        # s.method(1,2).returns(3)
        values = self._data_for_values(canned_data)
        if values: 
            return values
        # s.method(int, int).returns(3)
        types = self._map_types(current_call_parameters)
        values = self._data_for_types(canned_data, types)
        if values:
            return values
        return None

    def _should_always_return(self, return_data):
        return not (isinstance(return_data, dict) and '__returndata__' in return_data.keys())

    def _canned_data(self):
        return self._parent._data.get(self._name, None)

    def _data_for_values(self, return_data):
        return return_data.get(self._parameters, None)

    def _data_for_types(self, return_data, types):
        return return_data.get(tuple(types), None)

    # Configuration
    def raises(self, exception_type):
        # Configure the future call to raise an exception
        self._parent._exception_types[self._name] = exception_type

    def returns(self, data):
        # Check whether the data should only be returned for specific parameters
        # like in method(1,2).returns(3)
        if self._parameters:
            data = {
                '__returndata__': '__returndata__',
                self._parameters: data
            }
        self._parent._data[self._name] = data


    def _actual_calls(self):
        return (call for call in self._parent._calls if call._name == self._name)

    def _any_calls(self):
        return any(self._actual_calls())

    def _actual_call(self):
        try:
            return next(self._actual_calls())
        except: 
            return None

    def _all_types_match(self, expected_types, actual_parameters):
        actual_types = self._map_types(actual_parameters)
        equals = lambda (a,b):a==b
        return all(map(equals, zip(expected_types, actual_types)))

    def _map_types(self, parameters):
        return [type(parameter) for parameter in parameters]

    def _make_string(self, types):
        return ', '.join([t.__name__ for t in types])

    # Assertions
    @property
    def was_called(self):
        if not self._any_calls():
            raise _make(MissingCallComplaint, name=self._name)
        return True
    
    @property
    def was_not_called(self):
        if self._any_calls():
            raise _make(UndesiredCallComplaint, name=self._name)
        return True

    def was_called_with(self, *obj):
        call = self._actual_call()
        if not call:
            raise _make(MissingCallComplaint, name=self._name)

        if not call._parameters == obj:
            raise _make(ArgumentMissmatchComplaint, name=self._name, actual=call._parameters, expected=obj)
        # Danger - This is not properly tested!
        return obj == call._parameters

    def was_called_with_any(self, *expected_types):
        # Check if the configuration works like this:
        # s.method.was_called_with_any(str)
        for t in expected_types:
            if not type(t) == type(type):
                raise ValueError("Please specify a type rather than a value, like 'component.was_called_with_any(str)'")

        call = self._actual_call()

        if not call:
            raise _make(MissingCallComplaint, name=self._name)

        if not self._all_types_match(expected_types, call._parameters):
            expected_type_names = self._make_string(expected_types)
            actual_type_names = self._make_string(self._map_types(call._parameters))
            values = ', '.join([str(p) for p in call._parameters])
            raise _make(WrongArgumentTypeComplaint, 
                name=self._name, 
                types=expected_type_names, 
                call_parameter_types=actual_type_names, 
                values=values
            )
        return True

    def was_called_exactly(self, times):
        actual = sum(1 for call in self._parent._calls if call._name == self._name) 
        expected = times
        complaint = complaints.get(cmp(actual, expected), None)
        if complaint: 
            pad_actual, pad_expected = _pad(actual, expected)
            plural = ('s' if actual > 1 else '')
            raise _make(complaint, 
                name=self._name, 
                expected=expected, 
                actual=actual, 
                s=plural, 
                pad_actual=pad_actual, 
                pad_expected=pad_expected
            )
        return True

    received = was_called_with
    received_any = was_called_with_any

class Substitute(object):
    def __init__(self, *args, **kwargs):
        self._calls = []
        self._data = {}
        self._properties = {}
        self._exception_types = {}

    def __getattr__(self, name):
        return CallableOrValue(self, name)

    def __getitem__(self, name):
        return self._properties[name]

    def __setitem__(self, name, value):
        self._properties[name] = value

class Compare(object):
    def __init__(self, str):
        self._content = str
    
    def equal(self, s):
        assert_equal(self._content, s)

class ComparableString(str):
    def __init__(self, content):
        super(ComparableString)
        self.should = Compare(content)