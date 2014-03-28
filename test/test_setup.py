from nose.tools import *
from substitute import *
expect_that = assert_true
@raises(ValueError)
def test_bad_configuration_of_calling_with_argument_fails():
    '''Substitute - Setup: Notifies about bad configuration if a value is used rather than a type'''
    component = Substitute()
    expect_that(component.method.received_any('value'))

@raises(ValueError)
def test_bad_configuration_of_calling_with_keyword_argument_fails():
    '''Substitute - Setup: Notifies about bad configuration if a value is used rather than a type'''
    component = Substitute()
    expect_that(component.method.received_any(name='value'))