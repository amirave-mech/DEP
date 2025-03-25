from dataclasses import dataclass
from typing import *


@dataclass
class Event:
    """Base class for all events."""    
    # Class attribute for event identifier
    EVENT_TYPE = None

    def serialize(self):
        """Base serialization method."""
        event_type = self.EVENT_TYPE if self.EVENT_TYPE else self.__class__.__name__
        return {
            "type": event_type,
            # "id": self.id
        }


@dataclass
class ScopeStartEvent(Event):
    """Base class for scope start events."""
    def serialize(self):
        """Serialize scope event with base event serialization."""
        base_serialization = super().serialize()
        return base_serialization
    
@dataclass
class ScopeEndEvent(Event):
    """Base class for scope end events."""
    def serialize(self):
        """Serialize scope event with base event serialization."""
        base_serialization = super().serialize()
        return base_serialization


@dataclass
class IfStartEvent(ScopeStartEvent):
    EVENT_TYPE = "IF"
    hit: bool

    def serialize(self):
        """Serialize IfStartEvent with hit attribute."""
        base_serialization = super().serialize()
        base_serialization["hit"] = self.hit
        return base_serialization


@dataclass
class IfEndEvent(ScopeEndEvent):
    def serialize(self):
        """Serialize IfEndEvent."""
        return super().serialize()


@dataclass
class ElseStartEvent(ScopeStartEvent):
    EVENT_TYPE = "ELSE"
    
    def serialize(self):
        """Serialize ElseStartEvent with children."""
        base_serialization = super().serialize()
        return base_serialization


@dataclass
class ElseEndEvent(ScopeEndEvent):
    def serialize(self):
        """Serialize ElseEndEvent."""
        return super().serialize()


@dataclass
class ForStartEvent(ScopeStartEvent):
    EVENT_TYPE = "FOR"
    condition: str

    def serialize(self):
        """Serialize ForStartEvent with condition."""
        base_serialization = super().serialize()
        base_serialization["condition"] = self.condition
        return base_serialization


@dataclass
class ForIterationStartEvent(ScopeStartEvent):
    EVENT_TYPE = "FOR_ITERATION"
    iterator: Any

    def serialize(self):
        """Serialize ForIterationStartEvent with iterator."""
        base_serialization = super().serialize()
        base_serialization["iterator"] = str(self.iterator)
        return base_serialization


@dataclass
class ForIterationEndEvent(ScopeEndEvent):
    def serialize(self):
        """Serialize ForIterationEndEvent."""
        return super().serialize()


@dataclass
class ForEndEvent(ScopeEndEvent):
    iterations: int

    def serialize(self):
        """Serialize ForEndEvent with iterations."""
        base_serialization = super().serialize()
        base_serialization["iterations"] = self.iterations
        return base_serialization
    
@dataclass
class WhileStartEvent(ScopeStartEvent):
    EVENT_TYPE = "WHILE"
    condition: str

    def serialize(self):
        """Serialize WhileStartEvent with condition."""
        base_serialization = super().serialize()
        base_serialization["condition"] = self.condition
        return base_serialization


@dataclass
class WhileIterationStartEvent(ScopeStartEvent):
    EVENT_TYPE = "WHILE_ITERATION"

    def serialize(self):
        """Serialize WhileIterationStartEvent with iterator."""
        base_serialization = super().serialize()
        return base_serialization


@dataclass
class WhileIterationEndEvent(ScopeEndEvent):
    def serialize(self):
        """Serialize WhileIterationEndEvent."""
        return super().serialize()


@dataclass
class WhileEndEvent(ScopeEndEvent):
    iterations: int

    def serialize(self):
        """Serialize WhileEndEvent with iterations."""
        base_serialization = super().serialize()
        base_serialization["iterations"] = self.iterations
        return base_serialization


@dataclass
class VariableAssignmentEvent(Event):
    EVENT_TYPE = "VARIABLE_ASSIGNMENT"
    var_name: str
    before: Any
    after: Any

    def serialize(self):
        """Serialize VariableAssignmentEvent with variable details."""
        base_serialization = super().serialize()
        base_serialization.update({
            "var_name": self.var_name,
            "before": str(self.before),
            "after": str(self.after)
        })
        return base_serialization


@dataclass
class PrintEvent(Event):
    EVENT_TYPE = "PRINT"
    value: str

    def serialize(self):
        """Serialize PrintEvent with value."""
        base_serialization = super().serialize()
        base_serialization["value"] = self.value
        return base_serialization


@dataclass
class FunctionCallEvent(ScopeStartEvent):
    EVENT_TYPE = "FUNCTION_CALL"
    name: str
    params: List[Any]
    
    def serialize(self):
        """Serialize FunctionCallEvent with name and parameters."""
        base_serialization = super().serialize()
        base_serialization.update({
            "name": self.name,
            "params": [str(param) for param in self.params]
        })
        return base_serialization


@dataclass
class FunctionCallEndEvent(ScopeEndEvent):
    return_value: any
    
    def serialize(self):
        """Serialize FunctionCallEndEvent."""
        return super().serialize()


@dataclass
class ErrorEvent(Event):
    EVENT_TYPE = "ERROR"
    info: str

    def serialize(self):
        """Serialize ErrorEvent with error info."""
        base_serialization = super().serialize()
        base_serialization["info"] = self.info
        return base_serialization


@dataclass
class SwapEvent(Event):
    EVENT_TYPE = "SWAP"
    var_names: Tuple[str, str]
    values: Tuple[Any, Any]

    def serialize(self):
        """Serialize SwapEvent with variable names and values."""
        base_serialization = super().serialize()
        base_serialization.update({
            "var_names": list(self.var_names),
            "values": [str(value) for value in self.values]
        })
        return base_serialization


@dataclass
class ArrayModificationEvent(Event):
    EVENT_TYPE = "ARRAY_MODIFICATION"
    index: Union[int, str]
    arr_before: List[Any]
    arr_after: List[Any]

    def serialize(self):
        """Serialize ArrayModificationEvent with array details."""
        base_serialization = super().serialize()
        base_serialization.update({
            "index": self.index,
            "arr_before": [str(item) for item in self.arr_before],
            "arr_after": [str(item) for item in self.arr_after]
        })
        return base_serialization