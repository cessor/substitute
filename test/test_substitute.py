from nose.tools import *
from substitute import *
expect_that = assert_true

@raises(MissingCallComplaint)
def test_expect_was_called_fails():
    '''Substitute: Raises an exception when an expected method was not called'''
    component = Substitute()
    expect_that(component.method.was_called)

# Assert: Does not raise exception.
def test_expect_was_actually_called():
    '''Substitute: Does not raise an exception when the method was called'''
    component = Substitute()
    component.method()
    expect_that(component.method.was_called)

@raises(UndesiredCallComplaint)
def test_expect_was_not_called_fails():
    '''Substitute: Does raise an exception when a call occured unexpectedly'''
    component = Substitute()
    component.method()
    expect_that(component.method.was_not_called)

# Assert: Does not raise exception.
def test_expect_was_actually_not_called():
    '''Substitute: Does not raise an exception when a call occured unexpectedly'''
    component = Substitute()
    expect_that(component.method.was_not_called)

@raises(CalledTooRarelyComplaint)
def test_expect_was_called_once_fails():
    '''Substitute: Raises an exception when an expected method was not called'''
    component = Substitute()
    expect_that(component.method.was_called_exactly(ONCE))

# Assert: Does not raise exception.
def test_expect_was_actually_called_once():
    '''Substitute: Does not raise an exception if the method was called'''
    component = Substitute()
    component.method()
    expect_that(component.method.was_called_exactly(ONCE))

@raises(CalledTooOftenComplaint)
def test_expect_was_called_once_fails_if_called_too_often():
    '''Substitute: Raises an exception if a call was expected once but was called more often'''
    component = Substitute()
    component.method()
    # Called twice
    component.method()
    expect_that(component.method.was_called_exactly(ONCE))

@raises(CalledTooRarelyComplaint)
def test_expect_was_called_twice_fails_if_never_called():
    '''Substitute: Raises an exception if a call was made too rarely (never called but expected twice)'''
    component = Substitute()
    expect_that(component.method.was_called_exactly(TWICE))

@raises(CalledTooRarelyComplaint)
def test_expect_was_called_twice_fails_if_called_only_once():
    '''Substitute: Raises an exception if a call was made too rarely (called once but expected twice)'''
    component = Substitute()
    component.method()
    expect_that(component.method.was_called_exactly(TWICE))

# Assert: Does not raise exception.
def test_expect_was_actually_called_twice():
    '''Substitute: Does not raise an exception if two calls were made and two were expected'''
    component = Substitute()
    component.method()
    component.method()
    expect_that(component.method.was_called_exactly(TWICE))

@raises(CalledTooOftenComplaint)
def test_expect_was_called_twice_fails_if_called_too_often():
    '''Substitute: Raises an exception if the method was called too many times'''
    component = Substitute()
    component.method()
    component.method()
    component.method()
    expect_that(component.method.was_called_exactly(TWICE))

def test_calling_with_arguments():
    '''Substitute: Does not raise exception if an expected parameter was received'''
    component = Substitute()
    component.method('hello')
    expect_that(component.method.received('hello'))

@raises(ArgumentMissmatchComplaint)
def test_calling_with_arguments():
    '''Substitute: Does raise exception if an unexpected parameter was received'''
    component = Substitute()
    component.method('hello, honey')
    expect_that(component.method.received('hello'))

@raises(MissingCallComplaint)
def test_calling_with_arguments_fails():
    '''Substitute: Does raise an exception if there was no call received'''
    component = Substitute()
    expect_that(component.method.received('hello'))

def test_calling_with_vague_arguments():
    '''Substitute: Does not raise an exception if a string was expected and received'''
    component = Substitute()
    component.method('hello, honey')
    expect_that(component.method.received_any(str))

@raises(MissingCallComplaint)
def test_calling_not_calling_but_expecting_values_raises_missing_call_complaint():
    '''Substitute: Does raise an exception if values were expected but no call was made at all'''
    component = Substitute()
    expect_that(component.method.received_any(str))

@raises(ValueError)
def test_bad_configuration_of_calling_with_argument_fails():
    '''Substitute: Notifies about bad configuration if a value is used rather than a type'''
    component = Substitute()
    expect_that(component.method.received_any('value'))

@raises(WrongArgumentTypeComplaint)
def test_calling_with_with_vague_arguments_fails():
    '''Substitute: Does raise an exception if an int was was received but a string was expected'''
    component = Substitute()
    component.method(5)
    expect_that(component.method.received_any(str))

@raises(WrongArgumentTypeComplaint)
def test_calling_with_with_vague_arguments_fails_with_more_params():
    '''Substitute: Does raise an exception if an int was was received but a string was expected (more params)'''
    component = Substitute()
    component.method(5, 'hello', {})
    expect_that(component.method.received_any(str, dict))

def test_calls_return_stubbed_data():
    '''Substitute: Returns data when configured to do so'''
    component = Substitute()
    component.method.returns(5)
    assert_equal(component.method(), 5)

def test_calls_always_return_stubbed_data():
    '''Substitute: Returns data when configured to do so'''
    component = Substitute()
    component.method.returns(5)
    result = component.method()
    assert_equal(result, 5)

def test_calls_always_return_stubbed_data_even_with_parameterized_calls():
    '''Substitute: Returns data after configured, even when called with parameters'''
    component = Substitute()
    component.method.returns(8)
    result = component.method(2,3)
    assert_equal(result, 8)

def test_calls_return_stubbed_data_for_specific_values():
    '''Substitute: Returns data only for specific parameters'''
    component = Substitute()
    component.method(3, 4).returns(7)
    result = component.method(3, 4)
    assert_equal(result, 7)

def test_calls_return_nothing_when_called_with_wrong_values():
    '''Substitute: Returns None if the method was called with the wrong values'''
    component = Substitute()
    component.method(3, 4).returns(7)
    result = component.method(1, 2)
    assert_equal(result, None)

def test_calls_return_stubbed_data_if_configured_for_generic_values():
    '''Substitute: Returns data if configured for any values of a certain type'''
    component = Substitute()
    component.method(int, int).returns(3)
    result = component.method(8, 8)
    assert_equal(result, 3)

def test_calls_return_nothing_when_called_with_wrong_signature():
    '''Substitute: Returns None if the method was called with the wrong signature'''
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

def test_calls_return_stubbed_data_for_mixed_signature():
    '''Substitute: Returns data if configured and called with mixed signature'''
    component = Substitute()
    component.method(str, int).returns('aligator5')
    result = component.method('aligator', 5)
    assert_equal(result, 'aligator5')

def test_a_substitute_does_not_raise_exception_upon_configuration():
    '''Substitute: Does not raise an exception when configured but not called'''
    component = Substitute()
    component.method.raises(Exception)
    # Does not raise    

@raises(Exception)
def test_a_substitute_can_raise_exceptions():
    '''Substitute: Does raise an exception when configured and called'''
    component = Substitute()  
    component.method.raises(Exception)
    component.method()
    
def test_can_set_data():
    '''Substitute: Can privide property data'''
    component = Substitute()  
    component.value = 'hello'
    assert_equal(component.value, 'hello')

def test_can_find_data_like_a_dictionary():
    '''Substitute: Can provide property data like a dictionary'''
    component = Substitute()  
    component['value'] = 'hello'
    assert_equal(component['value'], 'hello')

def test_string_compare_syntax():
    s = ComparableString('Hello')
    s.should.equal('Hello')

@raises(AssertionError)
def test_string_compare_syntax_fails():
    s = ComparableString('Hello')
    s.should.equal('Helloa')