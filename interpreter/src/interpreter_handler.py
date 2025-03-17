from typing import Optional
from interpreter.src.eval import Eval, Literal
from interpreter.src.parser import Parser
from interpreter.src.Scanner import Scanner
from interpreter.src.expr import display
from interpreter.src.journal.journal import Journal, JournalSettings

class Interpreter:
    _evaluator = None

    # reset_journal indicates whether to reset the journal before each feedBlock
    def __init__(self, journal_settings: Optional[JournalSettings], reset_journal: bool = False):
        self._journal = None
        self._journal_settings = journal_settings
        self._reset_journal = reset_journal
        
        self._evaluator = Eval()
        self._evaluator.subscribe(self._handle_event)

    def _handle_event(self, event) -> None:
        self._journal.add_event(event)

    def feedBlock(self, code_block: str) -> tuple[any, Journal]:
        # Initial journal or reset it
        if self._journal is None or self._reset_journal:
            self._journal = Journal(self._journal_settings)

        scanner = Scanner(code_block)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        stmt_ast_opt = parser.parse()
        # TODO pass _handle_event to the evaluator
        return self._evaluator.evaluate(stmt_ast_opt), self._journal
