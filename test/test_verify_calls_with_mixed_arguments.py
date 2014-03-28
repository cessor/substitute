from nose.tools import *
from substitute import *
from substitute.complaint import *
expect_that = assert_true

def test_expect_received_mixed_data():
    '''Substitute - Verify (mixed): Method was called with args and kwargs'''
	component = Substitute()
	component.method('Johannes', age=12)
	expect_that(component.method.was_called_with('Johannes', age=12))

@raises(ArgumentMissmatchComplaint)
def test_expect_received_wrong_arg_mixed_fails():
    '''Substitute - Verify (mixed): Method was called with wrong arg'''
	component = Substitute()
	component.method('John', age=12)
	expect_that(component.method.was_called_with('Johannes', age=12))

@raises(KeywordArgumentMissmatchComplaint)
def test_expect_received_wrong_kwargs_mixed_fails():
    '''Substitute - Verify (mixed): Method was called with wrong kwarg'''
	component = Substitute()
	component.method('Johannes', age=32)
	expect_that(component.method.was_called_with('Johannes', age=12))

def test_expect_received_mixed_data_by_type():
    '''Substitute - Verify (mixed): Method was called with args and kwargs (type)'''
	component = Substitute()
	component.method('Johannes', age=32)
	expect_that(component.method.was_called_with_any(str, age=int))

@raises(WrongArgumentTypeComplaint)
def test_expect_received_wrong_arg_mixed_by_type_fails():
    '''Substitute - Verify (mixed): Method was called with wrong arg (type)'''
	component = Substitute()
	component.method(5, age=32)
	expect_that(component.method.was_called_with_any(str, age=int))

@raises(WrongKeywordArgumentTypeComplaint)
def test_expect_received_wrong_kwarg_mixed_by_type_fails():
	'''Substitute - Verify (mixed): Method was called with wrong kwarg (type)'''
	component = Substitute()
	component.method('hello', age=32)
	expect_that(component.method.was_called_with_any(str, age=str))