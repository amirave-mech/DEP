from Scanner import Scanner

scanner = Scanner("!*+-/=<> <= == |> this is a comment ==")
for token in scanner.scan_tokens():
    print(str(token))
