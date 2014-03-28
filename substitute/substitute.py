__all__ = [
    'Substitute',
    'ONCE',
    'TWICE'
]

__author__ = 'Johannes Hofmeister, http://twitter.com/@pro_cessor'
__version__ = '1.0.1'

from nose.tools import *
from complaint import *
from messages import messages


ONCE = 1
TWICE = 2
NEVER = 0

complaints = {
    -1: CalledTooRarelyComplaint,
    1: CalledTooOftenComplaint
}

def _pad(actual, expected):
    actual, expected= str(actual), str(expected)
    padding = max(len(actual), len(expected))
    return actual.ljust(padding), expected.ljust(padding)

def _message_for(complaint, **kwargs):
    message = messages[complaint]
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
        self._kwparameters = {}

    def __call__(self, *args, **kwargs):
        # Raise an exception if configured
        exception = self._configured_exception()
        if exception:
            raise exception(self._name)
        # Register call parameters
        self._parameters = args
        self._kwparameters = kwargs
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

    def _all_types_match(self, expected_types, actual_types):
        equals = lambda (a,b):a==b
        return all(map(equals, zip(expected_types, actual_types)))

    def _superfluous_keys(self, expeced_kwargs, actual_kwargs):
        return set(expeced_kwargs.keys()) ^ set(actual_kwargs.keys())

    def _all_kw_types_match(self, expeced_kwargs, actual_kwargs):
        if self._superfluous_keys(expeced_kwargs, actual_kwargs):
            return False
        return all(expeced_kwargs[key] == actual_kwargs[key] for key in expeced_kwargs.keys())
        
    def _map_types(self, parameters):
        return [type(parameter) for parameter in parameters]

    def _map_types_from_dict(self, dictionary):
        return {a:type(b) for a,b in dictionary.items()} 

    def _map_type_names_from_dict(self, dictionary):
        return dict(map(lambda (a,b): (a,b.__name__), dictionary.items()))

    def _make_string(self, types):
        return ', '.join([t.__name__ for t in types])

    def _make_kw_signature(self, kwargs):
        return '{list}'.format(list=', '.join(['='.join((str(a),str(b))) for a,b in kwargs.items()]))

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

    def was_called_with(self, *args_expected, **kwargs_expected):
        call = self._actual_call()
        if not call:
            raise _make(MissingCallComplaint, name=self._name)

        if args_expected and kwargs_expected:
            raise Exception('Not yet implemented')

        # Args were expected but none were given
        if args_expected and not call._parameters:
            if call._kwparameters:
                kwargs = self._make_kw_signature(call._kwparameters)               
                raise _make(UnexpectedKeywordComplaint, name=self._name, actual=kwargs, expected=args_expected)
            else:
                raise _make(MissingArgumentComplaint, name=self._name, actual=call._parameters, expected=args_expected)                
            # But kwargs were given
            raise _make(ArgumentMissmatchComplaint, name=self._name, actual=call._parameters, expected=args_expected)

        # Kwargs were expected but none were given
        if kwargs_expected and not call._kwparameters:
            kwargs = self._make_kw_signature(kwargs_expected)
            raise _make(MissingKeywordArgumentComplaint, name=self._name, actual=call._parameters, expected=kwargs)

        # Arguments don't match
        if not args_expected == call._parameters:
            raise _make(ArgumentMissmatchComplaint, name=self._name, actual=call._parameters, expected=args_expected)

        # KeywordArguments don't match
        if not kwargs_expected == call._kwparameters:

            if self._superfluous_keys(kwargs_expected, call._kwparameters):
                actual_kwargs = self._make_kw_signature(call._kwparameters)
                expected_kwargs = self._make_kw_signature(kwargs_expected)
                raise _make(MissingKeywordArgumentComplaint, name=self._name, actual=actual_kwargs, expected=expected_kwargs)

            kwargs = self._make_kw_signature(kwargs_expected)
            call_kwargs = self._make_kw_signature(call._kwparameters)
            raise _make(KeywordArgumentMissmatchComplaint, name=self._name, actual=call_kwargs, expected=kwargs)
        # Danger - This is not properly tested!
        return True

    def was_called_with_any(self, *expected_types, **expected_types_kwargs):
        # Check if the configuration works like this:
        # s.method.was_called_with_any(str)
        if expected_types:
            for t in expected_types:
                if not type(t) == type(type):
                    raise ValueError("Please specify a type rather than a value, like 'component.was_called_with_any(str)'")
        if expected_types_kwargs:
            for t in expected_types_kwargs.values():
                if not type(t) == type(type):
                    raise ValueError("Please specify a type rather than a value, like 'component.was_called_with_any(name=str)'")

        call = self._actual_call()
        if not call:
            raise _make(MissingCallComplaint, name=self._name)

        # Args were expected but none were provided
        if expected_types_kwargs and not call._kwparameters:           
            types = self._map_type_names_from_dict(expected_types_kwargs)
            kwargs = self._make_kw_signature(types)
            raise _make(MissingKeywordArgumentComplaint, name=self._name, actual=call._parameters, expected=kwargs)

        # Compare Parameteres
        actual_types = self._map_types(call._parameters)
        if not self._all_types_match(expected_types, actual_types):
            expected_type_names = self._make_string(expected_types)
            actual_type_names = self._make_string(self._map_types(call._parameters))
            values = ', '.join([str(p) for p in call._parameters])
            raise _make(WrongArgumentTypeComplaint, 
                name=self._name, 
                types=expected_type_names, 
                call_parameter_types=actual_type_names, 
                values=values
            )

        # Compare Keyword Argument Type Dictionaries

        # Check if there are different keys first
        if self._superfluous_keys(expected_types_kwargs, call._kwparameters):
            actual_kwargs = self._make_kw_signature(call._kwparameters)
            expected_kwargs = self._make_kw_signature(self._map_type_names_from_dict(expected_types_kwargs))
            raise _make(MissingKeywordArgumentComplaint, name=self._name, actual=actual_kwargs, expected=expected_kwargs)

        # check if the types of the keys match      
        expected_kw_types = expected_types_kwargs
        actual_kw_types = self._map_types_from_dict(call._kwparameters)

        # This does a dictionary match that is not necessary here
        if not self._all_kw_types_match(expected_kw_types, actual_kw_types):
            
            expected_kw_names = self._make_kw_signature(self._map_type_names_from_dict(expected_kw_types))
            actual_kw_names = self._make_kw_signature(self._map_type_names_from_dict(actual_kw_types))
            #values = ', '.join([str(p) for p in call._parameters])
            values = self._make_kw_signature(call._kwparameters)

            raise _make(WrongKeywordArgumentTypeComplaint, 
                 name=self._name, 
                 types=expected_kw_names, 
                 call_parameter_types=actual_kw_names,
                 values=values
            )
        return True

    def was_called_exactly(self, times):
        actual = sum(1 for call in self._parent._calls if call._name == self._name) 
        expected = times

        # If it was expected just once but was never called
        # Raise Missing Call Complaint
        if expected == ONCE and actual == NEVER:
            raise _make(MissingCallComplaint, name=self._name)

        # Compare if it is too often or too rarely
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