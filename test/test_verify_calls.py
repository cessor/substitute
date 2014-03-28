from nose.tools import *
from substitute import *
from substitute.complaint import *
expect_that = assert_true

def test_expect_was_called():
    '''Substitute - Verify: Method was called'''
    component = Substitute()
    component.method()
    expect_that(component.method.was_called)

def test_expect_was_not_called():
    '''Substitute - Verify: Method was not called'''
    component = Substitute()
    expect_that(component.method.was_not_called)

@raises(MissingCallComplaint)
def test_expect_was_called_fails():
    '''Substitute - Verify: Method was missing'''
    component = Substitute()
    expect_that(component.method.was_called)

@raises(UndesiredCallComplaint)
def test_expect_was_not_called_fails():
    '''Substitute - Verify: Method was called unexpectedly'''
    component = Substitute()
    component.method()
    expect_that(component.method.was_not_called)

def test_expect_was_called_once():
    '''Substitute - Verify (times): Method was called expected times (ONCE)'''
    component = Substitute()
    component.method()
    expect_that(component.method.was_called_exactly(ONCE))

def test_expect_was_actually_called_twice():
    '''Substitute - Verify (times): Was called expected times (TWICE)'''
    component = Substitute()
    component.method()
    component.method()
    # Assert: Does not raise exception.
    expect_that(component.method.was_called_exactly(TWICE))

@raises(MissingCallComplaint)
def test_expect_was_called_once_fails():
    '''Substitute - Verify (times): Method was never called'''
    component = Substitute()
    expect_that(component.method.was_called_exactly(ONCE))

@raises(CalledTooRarelyComplaint)
def test_expect_was_called_twice_fails():
    '''Substitute - Verify (times): Method was called too rarely'''
    component = Substitute()
    component.method()
    expect_that(component.method.was_called_exactly(TWICE))

@raises(CalledTooOftenComplaint)
def test_expect_was_called_too_often_fails():
    '''Substitute - Verify (times): Method was called too often (ONCE)'''
    component = Substitute()
    component.method()
    # Called twice
    component.method()
    expect_that(component.method.was_called_exactly(ONCE))

@raises(CalledTooOftenComplaint)
def test_expect_was_called_too_often_fails_2():
    '''Substitute - Verify (times): Method was called too often (TWICE)'''
    component = Substitute()
    component.method()
    component.method()
    component.method()
    expect_that(component.method.was_called_exactly(TWICE))