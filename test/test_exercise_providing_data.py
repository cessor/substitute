from nose.tools import *
from substitute import *
expect_that = assert_true

class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

def test_substitute_can_mimic_constructor_call():
    '''Substitute - Exercise: Can mimic a constructor call'''
    ctor = Person
    def make_person():
        return ctor('Jen', 32)

    p = make_person()
    assert_true(isinstance(p, Person))
    assert_false(isinstance(p, Substitute))
    assert_equal(p.name, 'Jen')

    ctor = Substitute
    s = make_person()
    assert_true(isinstance(s, Substitute))

def test_data_property():
    '''Substitute - Exercise: Provides data like an object'''
    component = Substitute()  
    component.value = 'hello'
    assert_equal(component.value, 'hello')

def test_data_dict():
    '''Substitute - Exercise: Provides data like a dictionary'''
    component = Substitute()  
    component['value'] = 'hello'
    assert_equal(component['value'], 'hello')

def test_call_returns_data():
    '''Substitute - Exercise (Stub): Method call provides data'''
    component = Substitute()
    component.method.returns(5)
    assert_equal(component.method(), 5)

def test_call_ignores_parameters():
    '''Substitute - Exercise (Stub): Method call provides data, ignores parameters'''
    component = Substitute()
    component.method.returns(8)
    result = component.method(2,3)
    assert_equal(result, 8)

def test_call_matches_parameters():
    '''Substitute - Exercise (Stub): Method call provides data, matches parameters'''
    component = Substitute()
    component.method(3, 4).returns(7)
    result = component.method(3, 4)
    assert_equal(result, 7)

def test_call_cant_match_parameters():
    '''Substitute - Exercise (Stub): Method call provides None for unmatched parameters'''
    component = Substitute()
    component.method(3, 4).returns(7)
    result = component.method(1, 2)
    assert_equal(result, None)

def test_call_matches_parameter_types():
    '''Substitute - Exercise (Stub): Method call provides data, matches parameter types'''
    component = Substitute()
    component.method(int, int).returns(3)
    result = component.method(8, 8)
    assert_equal(result, 3)

def test_call_cant_match_parameter_types():
    '''Substitute - Exercise (Stub): Method call provides None for unmatches parameter types'''
    component = Substitute()
    component.method(int, int).returns(3)
    result = component.method('hello')
    assert_equal(result, None)
    # an int, but not enough of them
    result = component.method(8)
    assert_equal(result, None)
    # an int, but not enough of them
    result = component.method(8, 9, 10)
    assert_equal(result, None)

def test_call_matches_mixed_parameter_types():
    '''Substitute - Exercise (Stub): Method call provides data, matches mixed parameter types'''
    component = Substitute()
    component.method(str, int).returns('aligator5')
    result = component.method('aligator', 5)
    assert_equal(result, 'aligator5')

def test_call_does_not_raise_exception_upon_config():
    '''Substitute - Exercise (Stub): Method does not raise an exception if not called'''
    component = Substitute()
    component.method.raises(Exception)
    # Does not raise

@raises(Exception)
def test_call_raises_exception_if_configured_and_called():
    '''Substitute - Exercise (Stub): Method does raise an exception if called'''
    component = Substitute()  
    component.method.raises(Exception)
    component.method()