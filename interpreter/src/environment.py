class Environment:
    def __init__(self, parent=None):
        """Creates a new environment. If parent is provided, this is a nested scope."""
        self.variables = {}  # Stores variable bindings
        self.parent = parent  # Points to the outer environment (if any)

    def get(self, name):
        """Retrieves a variable, checking parent environments if necessary."""
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)  # Look up in outer scopes
        else:
           return None

    def assign(self, name, value):
        """Assigns a value to an existing variable, searching up the scope chain if needed."""
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            self.parent.assign(name, value)  # Modify in the enclosing scope
        else:
            self.variables[name] = value

    def __repr__(self):
        return f"Environment({self.variables}, parent={self.parent is not None})"
