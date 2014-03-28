from nose.tools import *
from substitute import *
from substitute.complaint import *
expect_that = assert_true

# arg = Argument
# kwarg = Keyword Argument

# kwargs by names & values
def test_expect_received_kwarg():
    '''Substitute - Verify (kwargs): Method was called with kwarg'''
    component = Substitute()
    component.method(name='hello')
    expect_that(component.method.received(name='hello'))

@raises(MissingCallComplaint)
def test_was_never_called_fails():
    '''Substitute - Verify (kwargs): Method was never called (kwargs)'''
    component = Substitute()
    expect_that(component.method.received(name='hello'))

@raises(KeywordArgumentMissmatchComplaint)
def test_expect_received_wrong_kwarg_fails():
    '''Substitute - Verify (kwargs): Method was called with wrong kwarg'''
    component = Substitute()
    component.method(name='Jos')
    expect_that(component.method.received(name='Joseph'))

@raises(MissingKeywordArgumentComplaint)
def test_expect_received_no_kwarg_fails():
    '''Substitute - Verify (kwargs): Method was called without any args or kwars'''
    component = Substitute()
    component.method()
    expect_that(component.method.received(name='hello'))

@raises(MissingKeywordArgumentComplaint)
def test_expect_received_no_kwarg_fails_2():
    '''Substitute - Verify (kwargs): Method was called without any kwargs'''
    component = Substitute()
    component.method('Joseph')
    expect_that(component.method.received(name='Joseph'))

@raises(MissingKeywordArgumentComplaint)
def test_expect_received_wrong_kwarg_fails_2():
    '''Substitute - Verify (kwargs): Method was called with the wrong kwargs'''
    component = Substitute()
    component.method(key='Joseph')
    expect_that(component.method.received(name='Joseph'))

# kwargs by type
def test_expect_received_kwarg_type():
    '''Substitute - Verify (kwargs): Method was called with kwarg type'''
    component = Substitute()
    component.method(name='hello')
    expect_that(component.method.received_any(name=str))

@raises(MissingCallComplaint)
def test_was_never_called_fails_2():
    '''Substitute - Verify (kwargs): Method was never called (kwarg type)'''
    component = Substitute()
    expect_that(component.method.received_any(name=str))

@raises(MissingKeywordArgumentComplaint)
def test_expect_received_no_kwarg_type_fails_2():
    '''Substitute - Verify (kwargs): Method was called without any kwargs (type)'''
    component = Substitute()
    component.method('Joseph')
    expect_that(component.method.received_any(name=str))

@raises(MissingKeywordArgumentComplaint)
def test_expect_received_wrong_kwarg_type_fails_2():
    '''Substitute - Verify (kwargs): Method was called with the wrong kwargs (type)'''
    component = Substitute()
    component.method(key='hello')
    expect_that(component.method.received_any(name=str))

@raises(WrongKeywordArgumentTypeComplaint)
def test_expect_received_wrong_kwarg_type_fails():
    '''Substitute - Verify (kwargs): Method was called with wrong kwarg type'''
    component = Substitute()
    component.method(name=4)
    expect_that(component.method.received_any(name=str))