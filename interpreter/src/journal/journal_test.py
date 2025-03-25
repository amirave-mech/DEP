from interpreter.src.journal.journal import *
import json

def test_journal():
    # Create a journal with default settings
    journal = Journal(JournalSettings())
    
    # Simulate a function call with a loop and conditional
    func_call = FunctionCallEvent("bubble_sort", [5, 2, 8, 1, 9])
    journal.add_event(func_call)
    func_call = FunctionCallEndEvent([1,2,5,8,9])
    journal.add_event(func_call)
    
    journal.add_event(VariableAssignmentEvent(
        var_name="arr",
        before=None,
        after=[5, 2, 8, 1, 9]
    ))
    
    # Simulate an outer loop
    journal.add_event(ForStartEvent(
        "i in range(len(arr) - 1)"
    ))
    
    # First iteration of outer loop
    journal.add_event(ForIterationStartEvent(
        0
    ))
    
    journal.add_event(ForIterationEndEvent())
    
    journal.add_event(ForIterationStartEvent(
        1
    ))
    journal.add_event(ForIterationEndEvent())
    
    journal.add_event(ForIterationStartEvent(
        2
    ))
    journal.add_event(ForIterationEndEvent())
    
    # End outer loop
    journal.add_event(ForEndEvent(
        3
    ))
    
    # Get the JSON representation
    journal_json = journal.serialize()
    
    # Print the journal in a readable format
    print(json.dumps(journal_json, indent=2))
    
    # Verify that our events were recorded properly
    assert journal_json["events"][0]["type"] == "FUNCTION_CALL"
    assert journal_json["events"][0]["name"] == "bubble_sort"
    # assert len(journal_json["events"][0]["children"]) == 4  # Variable assignment, outer loop, return
    print("Test passed successfully!")

if __name__ == "__main__":
    test_journal()