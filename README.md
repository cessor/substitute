[![Build Status](https://travis-ci.org/cessor/substitute.svg?branch=master)](https://travis-ci.org/cessor/substitute)

Substitute
==========

A friendly substitute for python mocking frameworks [*](http://nsubstitute.github.io/).

It helps you replace the dependent-on components of a class when you are writing unit tests. It provides what others call Mocks or Stubs. It is loosely based on [NSubstitute](http://nsubstitute.github.io/), my favorite substitution framework for .NET.

## Creating a substitute...
To use a substitute in your tests simply create it like this:

    person = Substitute()

# Providing data...
In order to pass indirect input into the system under test you can either specify some properties or define the data that will be returned when a method is called.

## ...from properties
### Provide data as properties

    person = Substitute()
    person.name = 'Johannes'

### Or behave like a dictionary
    person['name'] = 'Johannes'

## ...from methods
### Always return the same value and ignore all parameters
    # Configuration
    calculator = Substitute()
    calculator.add.returns(3)

    # Actual call
    calculator.add()    # returns 3
    calculator.add('a') # returns 3
    calculator.add(1,2) # returns 3

### Only return data for specific parameters
    calculator.add(1,2).returns(3)

    calculator.add(1,2) # returns 3
    calculator.add(4,5) # returns None

### Only return data for parameters of the correct signature
    calculator.add(int, int).returns(9)
    
    calculator.add(4, 5)    # returns 9
    calculator.add('a','b') # returns None
    
### Raising Exceptions
    # Configuration
    calculator.divide.raises(DivisionByZeroError)

    # Actual call
    calculator.divide(10, 0) # raises error

# Verifying that something has happened...
Your system under test probably interacts with its surroundings by calling methods on other objects, some of which don't return anything. An example, as shown below would be calling the 'insert' or 'update' method on a database, or a log method. The calls a system makes can be checked on the substitute, too, and you can also verify that the call was made with the correct values.

    # Configuration
    address = City('London')              # some data
    peter = Person(name='Peter', address) # 
    address = City('Berlin')              #
    jane = Person(name='Jane', address)   # 
    
    database = Substitute()         # Substituting the dependent-on component
    
    people = People(database)       # System under Test
    expect_that = assert_true       # Readability is all!
    
## Checking that a call was made
    people.move(peter, City('New York')) # Method under Test

    expect_that(database.insert.was_called)

## Checking that a call was not made
    people.move(peter, City('New York')) # He already lives there

    expect_that(database.update.was_not_called)

## Checking that the call received proper values
    people.move(peter, City('New York')) # Method under Test

    # Fails, was called with New York!
    expect_that(database.insert.was_called_with(City('London'))) 

    # Other examples
    database.insert.was_called_with(City('New York')) # Succeeds!
    database.insert.was_called_with_any(City)         # Check Type
    database.insert.received(City('New York'))        # Also works
    database.insert.received_any(City)                # You guessed it...

## Checking on how many times something was called...
    
    people.marry(peter, jane)

    expect_that(database.update.was_called_exactly(TWICE))

    # Other examples 
    database.insert.was_called_exactly(ONCE)
    database.insert.was_called_exactly(TWICE)
    task.queue.was_called_exactly(times=10)


# About mocks and stubs...
During its lifetime an object will pass values to other components and receive values from them. In your test you want to control these indirect inputs and outputs. Indirect inputs are essentially data that are provided by a component. Indirect outputs (from the system under test) are essentially data that the dependent-on components receive from the system under test. Don't get confused, just always see it from the perspective of the thing being tested. Inputs come in, outputs go out. 
A component that provides canned data as indirect input is often referred to as a 'stub'. Configuring a substitute to provide canned data is especially useful when dealing with 'expensive' resources such as a database or the web. If, for example, you have a web client that parses the data from a website, you might want to provide some fake data to work with, rather than doing real requests to the web. Consider the following example:

    class TrelloClient(object):
        def __init__(self, requests):
            self._web = requests
        def all_boards(self):
            response = self._web.get(trello_url).content
            for board in parse(response):
                yield Board.from_document(board)
    ...

Here, the (really great) requests module is used to make web requests. Unfortunately, the roundtrip might take a while (overall resulting in very long running tests) and also you don't want your tests to break when there is no internet, for example when you are running them at an airport a hotel right before you are supposed to give a talk at a conference and the wifi goes down all the time. You can easily reduce the impact of the dependency on the web in your test using a substitute:

    def test_finding_all_boards():
        '''Finds all boards'''
        
        # Arrange
        response = Substitute()
        response.content = "{"json": "<...data...>"}"
        web = Substitute()
        web.get.returns(response)

        # System under Test
        client = TrelloClient(web)

        # Act
        boards = client.all_boards()

        # Assert length, content, whatever
        assert_sequence(boards, ...) 

## Don't cross the streams...
You should avoid passing data to a system under test and then also verifying that call was made, like this:

    def test_something():       
        calculator = Substitute()
        calculator.cos(0.5).returns(0.8776)
        robot = Robot(calculator)
        robot.rotate_arm()
        expect_that(calculator.cos.received(0.5))

This test has many problems, one of which being that it doesn't test anything. It tests that the configured call is being made, which it is, when it was configured. Tests like this tend to be very brittle, they mirror the exact implementation. As soon as minor changes occur, they break. Tests should help you detect bad inputs and outputs and tell you when something changes unexpectedly, but they should allow a certain amount of change until they actually break. If they break too often, refactoring code will become very annoying because you can't make any changes at all. Testing is not about mirroring your code in another file, but to provide a safety net. Also they are good to isolate cases of potentially bad values. In a test as shown the system depends on the call being made. If it is made properly, the appropriate return value is given to the sut and the whole thing will run smoothely. There is no need to actually assert that the call is being made. If the configured return value is not obtained, the system will break anyway. If it doesn't - then why are you configuring the substitute to provide values? Try being as specific as necessary and as generic as possible. 

# Mocks aren't stubs...
Don't believe me? Then read Martin Fowlers great article about the difference: [Mocks Aren't Stubs](http://martinfowler.com/articles/mocksArentStubs.html).
Sometimes a system under test calls methods on other components, without actually caring for a return value. This is often the case for functions that provide sideeffects, such as logging, writing to a file or saving an object to or updating one in a database. 
Checking on these interactions is often referred to as 'verifying expectations on a mock', but I never found the term 'mock' very helpful, therefore I try to avoid it where I can. It is all about verifying the indirect inputs and outputs of a system. Depending on who you ask, people will start confusing you anyway. Some say mock but mean a stub, some say mock but mean a test spy. These are all different things and I encourage you to look up the difference in this book: [http://xunitpatterns.com/](http://xunitpatterns.com/) but I try to avoid these terms whenever I can and recommend you do the same. Something goes in, something comes out. Don't call it mock or stub. It doesn't really matter and tests become way more readable when you leave out these weasel words. The basic python mocking tool is actually quite nice, but I don't like the notion of Mock or Magic Mock in it. Yet these are better than what other people have to deal with:

    var stubUserRepository = MockRepository.GenerateStub<IUserRepository>();
    var stubbedSmsSender = MockRepository.GenerateStub<ISmsSender>();
    var theUser = new User{HashedPassword = "this is not hashed password"};    
    stubUserRepository.Stub(x => x.GetUserByName("ayende")).Return(theUser);

Yeah. I know*.

<small>*) I really respect ayende and have been using the incredible RhinoMocks for ages, but I feel that it has a very steep learning curve. Just like the guys behind NSubstitute I just wanted a different syntax.</small>

License
=======
The MIT License (MIT)

Copyright (c) 2014 Johannes Hofmeister, cessor, twitter.com/@pro_cessor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.