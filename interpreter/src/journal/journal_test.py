from interpreter.src.journal.journal import *
import json

def test_journal():
    # Create a journal with default settings
    journal = Journal()
    
    # Simulate a function call with a loop and conditional

    func_call = FunctionCallEvent(journal._get_next_event_id(), "bubble_sort", [5, 2, 8, 1, 9])
    journal.add_event(func_call)
    func_call = FunctionCallEndEvent(journal._get_next_event_id())
    journal.add_event(func_call)
    
    journal.add_event(VariableAssignmentEvent(
        id=journal._get_next_event_id(),
        var_name="arr",
        before=None,
        after=[5, 2, 8, 1, 9]
    ))
    
    # Simulate an outer loop
    journal.add_event(ForStartEvent(
        journal._get_next_event_id(),
        "i in range(len(arr) - 1)"
    ))
    
    # First iteration of outer loop
    journal.add_event(ForIterationStartEvent(
        journal._get_next_event_id(),
        0
    ))
    
    # End first iteration of outer loop
    journal.add_event(ForIterationEndEvent(
        journal._get_next_event_id()
    ))
    
    # End outer loop
    journal.add_event(ForEndEvent(
        journal._get_next_event_id(),
        1
    ))
    
    # Return from function
    journal.add_event(ReturnEvent(
        journal._get_next_event_id(),
        [2, 5, 8, 1, 9]
    ))
    
    # # Track a variable assignment
    # journal.add_event(VariableAssignmentEvent(
    #     id=journal._get_next_event_id(),
    #     var_name="arr",
    #     before=None,
    #     after=[5, 2, 8, 1, 9]
    # ))
    
    # # Simulate an outer loop
    # journal.add_event(ForStartEvent(
    #     journal._get_next_event_id(),
    #     "i in range(len(arr) - 1)"
    # ))
    
    # # First iteration of outer loop
    # journal.add_event(ForIterationStartEvent(
    #     journal._get_next_event_id(),
    #     0
    # ))
    
    # # Inner loop
    # journal.add_event(ForStartEvent(
    #     journal._get_next_event_id(),
    #     "j in range(len(arr) - i - 1)"
    # ))
    
    # # First iteration of inner loop
    # journal.add_event(ForIterationStartEvent(
    #     journal._get_next_event_id(),
    #     0
    # ))
    
    # # Conditional
    # journal.add_event(IfStartEvent(
    #     journal._get_next_event_id(),
    #     True
    # ))
    
    # # Swap operation
    # journal.add_event(VariableAssignmentEvent(
    #     journal._get_next_event_id(),
    #     "arr[0]",
    #     5,
    #     2
    # ))
    # journal.add_event(VariableAssignmentEvent(
    #     journal._get_next_event_id(),
    #     "arr[1]",
    #     2,
    #     5
    # ))
    
    # # Print for debugging
    # journal.add_event(PrintEvent(
    #     journal._get_next_event_id(),
    #     "Swapped 5 and 2"
    # ))
    
    # # Close the conditional
    # journal.add_event(IfEndEvent(
    #     journal._get_next_event_id()
    # ))
    
    # # End first iteration of inner loop
    # journal.add_event(ForIterationEndEvent(
    #     journal._get_next_event_id()
    # ))
    
    # # End inner loop 
    # journal.add_event(ForEndEvent(
    #     journal._get_next_event_id(),
    #     1
    # ))
    
    # # End first iteration of outer loop
    # journal.add_event(ForIterationEndEvent(
    #     journal._get_next_event_id()
    # ))
    
    # # End outer loop
    # journal.add_event(ForEndEvent(
    #     journal._get_next_event_id(),
    #     1
    # ))
    
    # # Return from function
    # journal.add_event(ReturnEvent(
    #     journal._get_next_event_id(),
    #     [2, 5, 8, 1, 9]
    # ))
    
    # Get the JSON representation
    journal_json = journal.serialize()
    
    # Print the journal in a readable format
    print(json.dumps(journal_json, indent=2))
    
    # Verify that our events were recorded properly
    assert len(journal_json["events"]) == 1  # 1 root event (function call)
    assert journal_json["events"][0]["type"] == "FunctionCallEvent"
    assert journal_json["events"][0]["name"] == "bubble_sort"
    assert len(journal_json["events"][0]["children"]) == 4  # Variable assignment, outer loop, return
    
    print("Test passed successfully!")

if __name__ == "__main__":
    test_journal()