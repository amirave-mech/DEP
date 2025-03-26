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
        """Assigns to an existing variable if found, otherwise creates it in local scope."""
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            # Try assigning in parent. If it returns False, fall through to create locally.
            assigned = self.parent.try_assign(name, value)
            if not assigned:
                self.variables[name] = value
        else:
            self.variables[name] = value

    def try_assign(self, name, value) -> bool:
        if name in self.variables:
            self.variables[name] = value
            return True
        elif self.parent:
            return self.parent.try_assign(name, value)
        else:
            return False

    def get_root_env(self):
        root = self
        while root.parent is not None:
            root=root.parent
        return root

    def assign_to_root(self, name, value):
        self.get_root_env().assign(name, value)

    def define_func(self, name, value):
        self.assign_to_root(name, value)

    def __repr__(self):
        return f"Environment({self.variables}, parent={self.parent is not None})"
