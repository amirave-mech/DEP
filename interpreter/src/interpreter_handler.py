from typing import Optional
from interpreter.src.eval import Eval, Literal
from interpreter.src.interpreter_exception import InterpreterException
from interpreter.src.journal.journal_events import ErrorEvent
from interpreter.src.parser import Parser
from interpreter.src.Scanner import Scanner
from interpreter.src.expr import display
from interpreter.src.journal.journal import Journal, JournalSettings

class Interpreter:
    # reset_journal indicates whether to reset the journal before each feedBlock
    def __init__(self, journal_settings: JournalSettings, reset_journal: bool = False):
        self._journal: Journal = None
        self._journal_settings: JournalSettings = journal_settings
        self._reset_journal = reset_journal
        
        self._evaluator = Eval()
        self._evaluator.subscribe(self._handle_event)

    def _handle_event(self, event) -> None:
        self._journal.add_event(event)

    def feedBlock(self, code_block: str) -> Journal:
        # Initial journal or reset it
        if self._journal is None or self._reset_journal:
            self._journal = Journal(self._journal_settings)

        scanner = Scanner(code_block)
        try:
            tokens = scanner.scan_tokens()
        except InterpreterException as e:
            self._journal.add_event(ErrorEvent(str(e)))
            return self._journal

        parser = Parser(tokens)
        try:
            stmt_ast_opt = parser.parse()
        except InterpreterException as e:
            self._journal.add_event(ErrorEvent(str(e)))
            return self._journal
                
        try:
            self._evaluator.evaluate(stmt_ast_opt)
        except InterpreterException as e:
            self._journal.add_event(ErrorEvent(str(e)))
    
        return self._journal