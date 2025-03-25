from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from interpreter.src.journal.journal_events import *

# IMPORTANT - an event is allowed if its in the whitelist, or the whitelist is null
@dataclass
class JournalSettings:
    """Settings for the journal."""
    whitelist: Dict[type, bool] = None
    max_length: int = 1000
    max_depth: int = 10

OPENING_EVENTS = {
    IfStartEvent: IfEndEvent,
    ElseStartEvent: ElseEndEvent,
    ForStartEvent: ForEndEvent,
    ForIterationStartEvent: ForIterationEndEvent,
    WhileStartEvent: WhileEndEvent,
    WhileIterationStartEvent: WhileIterationEndEvent,
    FunctionCallEvent: FunctionCallEndEvent  # Functions close with RETURN, but not required
}
    
class Journal:
    def __init__(self, settings: JournalSettings):
        self.settings: JournalSettings = settings
        self.events: List[Event] = []
        self.current_event_id: int = 0
        
        self.tree: List = []
        self.scope_json_stack: List = []
        self.scope_event_stack: List = []

    def _is_event_allowed(self, event: Event):
        return not self.settings.whitelist or (type(event) in self.settings.whitelist)

    def add_event(self, event: Event) -> None:
        if not self._is_event_allowed(event):
            return
        
        event_json = event.serialize()
            
        # if its a closing event, append data to the matching start event and quit
        # TODO check if a scope end is skipped
        if isinstance(event, ScopeEndEvent):
            next_close = None
            if len(self.scope_event_stack) != 0:
                next_close = OPENING_EVENTS[type(self.scope_event_stack[-1])]
            else:
                print(f'[JOURNAL] Warning: Tried to close scope {event.EVENT_TYPE} but no scopes exist!')
            
            if next_close is not None and isinstance(event, next_close):
                # append all the end event fields to the start event, so we have one complete event
                self._append_dict(event_json, self.scope_json_stack[-1])
                self.scope_json_stack.pop()
                self.scope_event_stack.pop()
            else:
                print(f'[JOURNAL] Warning: expected to a scope close of type {next_close} but got {event.EVENT_TYPE}.')
                
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