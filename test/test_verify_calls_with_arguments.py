from nose.tools import *
from substitute import *
expect_that = assert_true

# arg = Argument
# kwarg = Keyword Argument

def test_expect_received_data():
    '''Substitute - Verify (args): Method was called with data'''
    component = Substitute()
    component.method('hello')
    expect_that(component.method.received('hello'))

def test_expect_received_type():
    '''Substitute - Verify (args): Method was called with type'''
    component = Substitute()
    component.method('hello')
    expect_that(component.method.received_any(str))

@raises(MissingCallComplaint)
def test_was_never_called_fails():
    '''Substitute - Verify (args): Method was never called (data)'''
    component = Substitute()
    expect_that(component.method.received('hello'))

@raises(MissingCallComplaint)
def text_expect_was_never_called_fails_2():
    '''Substitute - Verify (args): Method was never called (type)'''
    component = Substitute()
    expect_that(component.method.received_any(str))

@raises(UnexpectedKeywordComplaint)
def test_expect_received_unexpected_keyword_fails():
    '''Substitute - Verify (args): Method was called with unexpected kwarg'''
    component = Substitute()
    component.method(name='hello')
    expect_that(component.method.received('hello'))

@raises(ArgumentMissmatchComplaint)
def test_expect_received_wrong_data_fails():
    '''Substitute - Verify (args): Method was called with wrong data'''
    component = Substitute()
    component.method('hello, honey')
    expect_that(component.method.received('hello'))

@raises(WrongArgumentTypeComplaint)
def test_expect_received_wrong_type_fails():
    '''Substitute - Verify (args): Method was called with wrong type'''
    component = Substitute()
    component.method(5)
    expect_that(component.method.received_any(str))

@raises(WrongArgumentTypeComplaint)
def test_expect_received_wrong_signature_fails():
    '''Substitute - Verify (args): Method was called with wrong signature'''
    component = Substitute()
    component.method(5, 'hello', {})
    expect_that(component.method.received_any(str, dict))

## 

## HERE!!!

##
@raises(MissingArgumentComplaint)
def test_expect_received_no_argument_fails():
    '''Substitute - Verify (args): Method was called without arguments'''
    component = Substitute()
    component.method()
    expect_that(component.method.received('hello'))




@raises(ValueError)
def test_bad_configuration_of_calling_with_keyword_argument_fails():
    component = Substitute()
    expect_that(component.method.received_any(name='value'))

@raises(ValueError)
def test_bad_configuration_of_calling_with_argument_fails():
    '''Substitute: Notifies about bad configuration if a value is used rather than a type'''
    component = Substitute()
    expect_that(component.method.received_any('value'))

class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

def test_substitute_can_mimic_constructor_call():
    '''Substitute: Can mimic a constructor call'''
    ctor = Person
    def make_person():
        return ctor('Jen',32)

    p = make_person()
    assert_true(isinstance(p, Person))
    assert_false(isinstance(p, Substitute))
    assert_equal(p.name, 'Jen')

    ctor = Substitute
    s = make_person()
    assert_true(isinstance(s, Substitute))