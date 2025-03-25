from dataclasses import dataclass

class InterpreterException(Exception):
    # line: int
    
    def __init__(self, message):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        
    # TODO token?
    