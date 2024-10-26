import sys

def main():
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize/parse <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    try:
        with open(filename, "r") as file:
            file_contents = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        exit(1)
    
    if command == "tokenize":
        tokens, lexical_errors = tokenize(file_contents)
        for token in tokens:
             if token.startswith("[line"):
                 print(token, file=sys.stderr)
             else:
                 print(token)
        if lexical_errors:
             exit(65)
        else:
             exit(0)
    elif command == "parse":
        tokens, lexical_errors = tokenize(file_contents)
        parse_result, parser_errors = parse(tokens)
        for result in parse_result:
            if result.startswith("[Error"):
                print(result, file=sys.stderr)
            else:
                print(result)       
        if parser_errors:
            exit(65)
        else:
            exit(0)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

def tokenize(file_contents):
        tokens = []  
        line_number = 1
        lexical_errors = False
        pointer = 0

        while pointer < len(file_contents):
            char = file_contents[pointer]        

            match char:
                case "(":
                    tokens.append("LEFT_PAREN ( null")
                    pointer += 1
                case ")":
                    tokens.append("RIGHT_PAREN ) null")
                    pointer += 1
                case "{":
                    tokens.append("LEFT_BRACE { null")
                    pointer += 1
                case "}":
                    tokens.append("RIGHT_BRACE } null")
                    pointer += 1
                case ",":
                    tokens.append("COMMA , null")
                    pointer += 1
                case "-":
                    tokens.append("MINUS - null")
                    pointer += 1
                case "+":
                    tokens.append("PLUS + null")
                    pointer += 1
                case ";":
                    tokens.append("SEMICOLON ; null")
                    pointer += 1
                case "*":
                    tokens.append("STAR * null")
                    pointer += 1
                case "=":
                    if pointer + 1 < len(file_contents) and file_contents[pointer + 1] == "=":
                        tokens.append("EQUAL_EQUAL == null")
                        pointer += 2
                    else:
                        tokens.append("EQUAL = null")
                        pointer += 1
                case "!":
                    if pointer + 1 < len(file_contents) and file_contents[pointer + 1] == "=":
                        tokens.append("BANG_EQUAL != null")
                        pointer += 2
                    else:
                        tokens.append("BANG ! null")
                        pointer += 1
                case "<":
                    if pointer + 1 < len(file_contents) and file_contents[pointer + 1] == "=":
                        tokens.append("LESS_EQUAL <= null")
                        pointer += 2
                    else:
                        tokens.append("LESS < null")
                        pointer += 1
                case ">": 
                    if pointer + 1 < len(file_contents) and file_contents[pointer + 1] == "=":
                        tokens.append("GREATER_EQUAL >= null")
                        pointer += 2
                    else:
                        tokens.append("GREATER > null")
                        pointer += 1
                case "/":
                    if pointer + 1 < len(file_contents) and (file_contents[pointer + 1] == "/" or file_contents[pointer + 1] == "*"):
                        if file_contents[pointer + 1] == "/":
                            while pointer < len(file_contents) and file_contents[pointer] != "\n":
                                pointer += 1
                        elif file_contents[pointer + 1] == "*":
                            while pointer < len(file_contents) and not (file_contents[pointer] == "*" and file_contents[pointer + 1] == "/"):
                                pointer += 1 
                            pointer += 2
                    else:
                        tokens.append("SLASH / null")
                        pointer += 1
                case " "|"\t":
                    pointer += 1
                case "\n":
                    pointer += 1
                    line_number += 1
                case '"':
                    start = pointer
                    while pointer + 1 < len(file_contents) and file_contents[pointer + 1] != '"':
                        pointer += 1
                    if pointer + 1 < len(file_contents) and file_contents[pointer + 1] == '"':
                        value = file_contents[start + 1:pointer + 1]
                        tokens.append(f'STRING "{value}" {value}')
                        pointer += 2
                    else:
                        error_message=(f'[line {line_number}] Error: Unterminated string.')
                        tokens.append(error_message)
                        lexical_errors = True
                        pointer += 1
                case "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"|".": 
                    start = pointer
                    if pointer+1< len(file_contents) and ((file_contents[pointer] in "0123456789")):
                        while pointer< len(file_contents) and (file_contents[pointer] in "0123456789"):
                            pointer += 1

                        if pointer< len(file_contents) and file_contents[pointer] == ".":
                            pointer += 1
                            while pointer < len(file_contents) and file_contents[pointer] in "0123456789":
                                pointer += 1
                        value = file_contents[start:pointer]
                        tokens.append(f"NUMBER {value} {float(value)}")

                    elif pointer+1< len(file_contents) and (file_contents[pointer] == "."  and file_contents[pointer + 1] in "0123456789"): 
                        if pointer + 1 < len(file_contents) and file_contents[pointer + 1] in "0123456789":
                            pointer += 1
                            while pointer < len(file_contents) and file_contents[pointer] in "0123456789":
                                pointer += 1
                        value = file_contents[start:pointer]
                        tokens.append(f"NUMBER {value} {float(value)}")
                    else:
                        tokens.append("DOT . null")
                        pointer += 1
                case "a"|"b"|"c"|"d"|"e"|"f"|"g"|"h"|"i"|"j"|"k"|"l"|"m"|"n"|"o"|"p"|"q"|"r"|"s"|"t"|"u"|"v"|"w"|"x"|"y"|"z"|"A"|"B"|"C"|"D"|"E"|"F"|"G"|"H"|"I"|"J"|"K"|"L"|"M"|"N"|"O"|"P"|"Q"|"R"|"S"|"T"|"U"|"V"|"W"|"X"|"Y"|"Z"|"_"|"0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9":
                    start = pointer
                    while pointer + 1 < len(file_contents) and file_contents[pointer + 1] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789":
                        pointer += 1
                    value = file_contents[start:pointer + 1]
                    Identifiers = ["and", "class", "else", "false", "for", "fun", "if", "nil", "or", "print", "return", "super", "this", "true", "var", "while"]
                    if value in Identifiers:
                        tokens.append(f"{value.upper()} {value} null")
                    else:
                        tokens.append(f"IDENTIFIER {value} null")
                    pointer += 1              
                case "$"|"#"|"@"|"%"|_:
                    error_message=(f"[line {line_number}] Error: Unexpected character: {char}")
                    tokens.append(error_message)
                    lexical_errors = True
                    pointer += 1 

        tokens.append("EOF  null")
        
        return tokens, lexical_errors

def parse(tokens):
    current = 0
    parser_errors = False
    parse_result = []

    def match(expected):
        nonlocal current
        if current < len(tokens) and tokens[current].startswith(expected):
            current += 1
            return True
        return False

    def check(expected):
        if current >= len(tokens):
            return False
        return tokens[current].startswith(expected)

    def parse_expression():
        return parse_equality()

    def parse_equality():
        expr = parse_comparison()
        if expr is None:
            return None
        while match("BANG_EQUAL") or match("EQUAL_EQUAL"):
            operator = tokens[current - 1].split()[1]
            right = parse_comparison()
            if right is None:
                return None
            expr = f"({operator} {expr} {right})"
        return expr

    def parse_comparison():
        expr = parse_term()
        if expr is None:
            return None
        while match("GREATER") or match("GREATER_EQUAL") or match("LESS") or match("LESS_EQUAL"):
            operator = tokens[current - 1].split()[1]
            right = parse_term()
            if right is None:
                return None
            expr = f"({operator} {expr} {right})"
        return expr

    def parse_term():
        expr = parse_factor()
        if expr is None:
            return None
        while match("MINUS") or match("PLUS"):
            operator = tokens[current - 1].split()[1]
            right = parse_factor()
            if right is None:
                nonlocal parser_errors
                parser_errors = True
                parse_result.append("[Error: Expected expression]")
                return None
            expr = f"({operator} {expr} {right})"
        return expr

    def parse_factor():
        expr = parse_unary()
        if expr is None:
            return None
        while match("STAR") or match("SLASH"):
            operator = tokens[current - 1].split()[1]
            right = parse_unary()
            if right is None:
                nonlocal parser_errors
                parser_errors = True
                parse_result.append("[Error: Expected expression]")
                return None
            expr = f"({operator} {expr} {right})"
        return expr

    def parse_unary():
        if match("BANG") or match("MINUS"):
            operator = tokens[current - 1].split()[1]
            right = parse_unary()
            if right is None:
                nonlocal parser_errors
                parser_errors = True
                parse_result.append("[Error: Expected expression]")
                return None
            return f"({operator} {right})"
        return parse_primary()

    def parse_primary():
        nonlocal parser_errors
        if match("FALSE"):
            return "false"
        if match("TRUE"):
            return "true"
        if match("NIL"):
            return "nil"
        if match("NUMBER"):
            return tokens[current - 1].split()[2]
        if match("STRING"):
            q=tokens[current - 1].split('"',1)
            return f'{q[1].split('"', 1)[0]}'
        if match("IDENTIFIER"):
            return tokens[current - 1].split()[1]
        if match("LEFT_PAREN"):
            expr = parse_expression()
            if expr is None:
                return None
            if not match("RIGHT_PAREN"):
                parser_errors = True
                parse_result.append("[Error: Expected ')']")
                return None
            return f"(group {expr})"
        
        parser_errors = True
        parse_result.append("[Error: Expected expression]")
        return None

    expr = parse_expression()
    if expr is not None:
        parse_result.append(expr)
    elif not parse_result:  # Only add if no error message has been added yet
        parser_errors = True
        parse_result.append("[Error: Expected expression]")

    return parse_result, parser_errors

if __name__ == "__main__":
    main()