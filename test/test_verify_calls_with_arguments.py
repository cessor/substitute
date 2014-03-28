from nose.tools import *
from substitute import *
from substitute.complaint import *
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

@raises(MissingArgumentComplaint)
def test_expect_received_no_argument_fails():
    '''Substitute - Verify (args): Method was called without arguments'''
    component = Substitute()
    component.method()
    expect_that(component.method.received('hello'))

