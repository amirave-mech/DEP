import json
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field


@dataclass
class Event:
    """Base class for all events."""
    id: int

    def serialize(self):
        """Base serialization method."""
        return {
            "type": self.__class__.__name__,
            "id": self.id
        }


@dataclass
class ScopeStartEvent(Event):
    def serialize(self):
        """Serialize scope event with base event serialization."""
        base_serialization = super().serialize()
        return base_serialization
    
@dataclass
class ScopeEndEvent(Event):
    def serialize(self):
        """Serialize scope event with base event serialization."""
        base_serialization = super().serialize()
        return base_serialization


@dataclass
class IfStartEvent(ScopeStartEvent):
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
    condition: str

    def serialize(self):
        """Serialize ForStartEvent with condition."""
        base_serialization = super().serialize()
        base_serialization["condition"] = self.condition
        return base_serialization


@dataclass
class ForIterationStartEvent(ScopeStartEvent):
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
class VariableAssignmentEvent(Event):
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
    value: str

    def serialize(self):
        """Serialize PrintEvent with value."""
        base_serialization = super().serialize()
        base_serialization["value"] = self.value
        return base_serialization


@dataclass
class ReturnEvent(Event):
    value: Any

    def serialize(self):
        """Serialize ReturnEvent with return value."""
        base_serialization = super().serialize()
        base_serialization["value"] = str(self.value)
        return base_serialization


@dataclass
class FunctionCallEvent(ScopeStartEvent):
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
    def serialize(self):
        """Serialize FunctionCallEndEvent."""
        return super().serialize()


@dataclass
class ErrorEvent(Event):
    info: str

    def serialize(self):
        """Serialize ErrorEvent with error info."""
        base_serialization = super().serialize()
        base_serialization["info"] = self.info
        return base_serialization


@dataclass
class SwapEvent(Event):
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


@dataclass
class JournalSettings:
    """Settings for the journal."""
    event_logging: Dict[type, bool] = field(default_factory=dict)
    max_length: int = 1000
    max_depth: int = 10


class Journal:
    OPENING_EVENTS = {
        IfStartEvent: IfEndEvent,
        ElseStartEvent: ElseEndEvent,
        ForStartEvent: ForEndEvent,
        ForIterationStartEvent: ForIterationEndEvent,
        FunctionCallEvent: FunctionCallEndEvent  # Functions close with RETURN, but not required
    }
    
    # Closing scope events and their corresponding opening events
    CLOSING_EVENTS = {
        IfEndEvent: IfStartEvent,
        ElseEndEvent: ElseStartEvent,
        ForEndEvent: ForStartEvent,
        ForIterationEndEvent: ForIterationStartEvent,
        ReturnEvent: FunctionCallEvent,  # Special case for function returns
        FunctionCallEndEvent : FunctionCallEvent
    }
    
    def __init__(self, settings: Optional[JournalSettings] = None):
        self.settings = settings or JournalSettings()
        self.events: List[Event] = []
        self.current_event_id: int = 0

    def _get_next_event_id(self) -> int:
        event_id = self.current_event_id
        self.current_event_id += 1
        return event_id
    
    tree = []
    scope_json_stack = []
    scope_event_stack = []

    def add_event(self, event: Event) -> None:
        event_json = event.serialize()
            
        # if its a closing event, append data to the matching start event and quit
        # TODO check if a scope end is skipped
        if isinstance(event, ScopeEndEvent):
            next_close = None
            if len(self.scope_event_stack) != 0:
                next_close = self.OPENING_EVENTS[type(self.scope_event_stack[-1])]
            
            if next_close is not None and isinstance(event, next_close):
                # append all the end event fields to the start event, so we have one complete event
                self._append_dict(event_json, self.scope_json_stack[-1])
                self.scope_json_stack.pop()
                self.scope_event_stack.pop()
                
            return
        
        if len(self.scope_event_stack) != 0:
            self.scope_json_stack[-1]["children"].append(event_json)
        else:
            self.tree.append(event_json)
        
        # if the event is a scope start, add it to the stack
        if isinstance(event, ScopeStartEvent):
            event_json["children"] = []
            self.scope_event_stack.append(event)
            self.scope_json_stack.append(event_json)
            
        # print("EVENT:", event_json)
        # print()
        # print("TREE:", json.dumps(self.tree, indent=4))
        # print()
        # print("STACK:", self.scope_event_stack)
        # print()
        # print("JSON STACK:", (self.scope_json_stack))
        # print("\n\n============\n\n")
            
    def _append_dict(self, dict_from, dict_to):
        for key, value in dict_from.items():
            if key not in dict_to:
                dict_to[key] = value
    
    def serialize(self) -> Dict[str, Any]:
        """Builds and returns the JSON representation of the journal."""
        # event_tree = self.tree #_build_event_tree()
        return {
            "events": self.tree
        }