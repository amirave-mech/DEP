class ReturnException(Exception):
    def __init__(self, ret_val):
        self._ret_val = ret_val

    @property
    def ret_val(self):
        return self._ret_val