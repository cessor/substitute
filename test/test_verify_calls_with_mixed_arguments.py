from nose.tools import *
from substitute import *
from substitute.complaint import *
expect_that = assert_true

def test_expect_received_mixed_data():
	component = Substitute()
	component.method('Johannes', age=12)
	expect_that(component.method.was_called_with('Johannes', age=12))

@raises(ArgumentMissmatchComplaint)
def test_expect_received_wrong_arg_mixed_fails():
	component = Substitute()
	component.method('John', age=12)
	expect_that(component.method.was_called_with('Johannes', age=12))

@raises(KeywordArgumentMissmatchComplaint)
def test_expect_received_wrong_kwargs_mixed_fails():
	component = Substitute()
	component.method('Johannes', age=32)
	expect_that(component.method.was_called_with('Johannes', age=12))