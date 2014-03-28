class Complaint(Exception):
    pass
class ArgumentMissmatchComplaint(Complaint):
    pass
class CalledTooOftenComplaint(Complaint):
    pass
class CalledTooRarelyComplaint(Complaint):
    pass
class KeywordArgumentMissmatchComplaint(Complaint):
    pass
class MissingCallComplaint(Complaint):
    pass
class MissingArgumentComplaint(Complaint):
    pass
class MissingKeywordArgumentComplaint(Complaint):
    pass
class UndesiredCallComplaint(Complaint):
    pass
class UnexpectedKeywordComplaint(Complaint):
    pass    
class WrongArgumentTypeComplaint(Complaint):
    pass
class WrongKeywordArgumentTypeComplaint(Complaint):
    pass