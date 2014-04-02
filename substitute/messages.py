from complaint import *
messages = {
    CalledTooRarelyComplaint: """\n\n\tThe method '{name}' was not called often enough!\n
    I expected {expected} calls but the method was called only {actual} time{s}

Expected: {pad_expected} x {name}(...)
Was:      {pad_actual} x {name}(...)
    """,
    CalledTooOftenComplaint: """\n\n\tThe method '{name}' was called too many times!\n
    I expected {expected} calls but the method was called {actual} time{s}

Expected: {pad_expected} x {name}(...)
Was:      {pad_actual} x {name}(...)
    """,
    ArgumentMissmatchComplaint: """\n\n\tThe method '{name}' was called with the wrong arguments!

Expected: {name}{expected} 
Received: {name}{actual}
""",
    KeywordArgumentMissmatchComplaint: """\n\n\tThe method '{name}' was called with the wrong keyword-arguments!

Expected: {name}({expected}) 
Received: {name}({actual})
""",
    MissingCallComplaint: """\n\n\tThe method '{name}' was not called at all!

Expected: 1 x {name}(...)
Was:      0 x {name}(...)
""",
    MissingArgumentComplaint: """\n\n\tThe method '{name}' was called without arguments!

Expected: {name}({expected})
Received: {name}{actual}
    """,
    MissingKeywordArgumentComplaint: """\n\n\tThe method '{name}' was called without an expected keyword!

Expected: {name}({expected})
Received: {name}({actual})
    """,

    UndesiredCallComplaint: """\n\n\tThe method '{name}' was called, which was unintended!

Expected: 0 x {name}(...)
Was:      1 x {name}(...)
""",
    UnexpectedKeywordComplaint: """\n\n\tThe method '{name}' was called with keyword-arguments, but normal arguments were expected!

Expected: {name}{expected} 
Received: {name}{actual}
""",
    WrongKeywordArgumentTypeComplaint: '''\n\n\tThe method '{name}' was called by the wrong signature!\n
The actual call was was: {name}({values})

Expected: {name}({types})
Received: {name}({call_parameter_types})
''',
    WrongArgumentTypeComplaint : '''\n\n\tThe method '{name}' was called by the wrong signature!\n
The actual call was was: {name}({values})

Expected: {name}({types})
Received: {name}({call_parameter_types})
'''
}