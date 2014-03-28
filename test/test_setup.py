from nose.tools import *
from substitute import *
expect_that = assert_true

@raises(ValueError)
def test_bad_config_of_calling_with_type_argument_fails():
    '''Substitute - Setup: called_with     should ask for a value, not a type. called_with(str)'''
    component = Substitute()
    expect_that(component.method.received(str))

@raises(ValueError)
def test_bad_config_of_calling_with_type_keyword_argument_fails():
    '''Substitute - Setup: called_with     should ask for a value, not a type. called_with(key=str)'''
    component = Substitute()
    expect_that(component.method.received(name=str))

@raises(ValueError)
def test_bad_configuration_of_calling_with_argument_fails():
    '''Substitute - Setup: called_with_any should ask for a type, not a value. called_with_any('value')'''
    component = Substitute()
    expect_that(component.method.received_any('value'))

@raises(ValueError)
def test_bad_configuration_of_calling_with_keyword_argument_fails():
    '''Substitute - Setup: called_with_any should ask for a type, not a value. called_with_any(key='value')'''
    component = Substitute()
    expect_that(component.method.received_any(name='value'))