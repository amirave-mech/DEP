from Scanner import Scanner

source = """!*+-/=<> {var blawg = 123.555.lower()} <= == |> this is a comment ==
test test the test AND = for"""

scanner = Scanner(source)

for token in scanner.scan_tokens():
    print(str(token))

print('')

lines = source.split('\n')
token = scanner.scan_tokens()[10]
print(lines[token.line])

carets = ''
for i, ch in enumerate(lines[token.line]):
    if token.char_range[0] <= i < token.char_range[1]:
        carets += '^'
    else:
        carets += ' '

print(carets)