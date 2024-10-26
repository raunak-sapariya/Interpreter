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

    #print(f"Command: {command}", f"Filename: {filename}", file=sys.stderr)
    
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
            if result.startswith("[line"):
                print(result, file=sys.stderr)
            else:
                print(result)
        if lexical_errors or parser_errors:
            exit(65)

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
    parse_result = []
    parser_errors = False
    
    class parser:
        def __init__(self,tokens):
            self.tokens=tokens
            self.current=0

        def expression(self):
            return self.equality()

        def equality(self):
            expr=self.comparison()
            while self.match("BANG_EQUAL","EQUAL_EQUAL"):
                operator=self.previous
                right=self.comparison()
                expr=[operator,expr,right]
            return expr

        def comparison(self):
            expr=self.term()
            while self.match("GREATER","GREATER_EQUAL","LESS","LESS_EQUAL"):
                operator=self.previous
                right=self.term()
                expr=[operator,expr,right]
            return expr 

        def term(self):
            expr=self.factor()
            while self.match("MINUS","PLUS"):
                operator=self.previous
                right=self.factor()
                expr=[operator,expr,right]
            return expr

        def factor(self):
            expr=self.unary()
            while self.match("SLASH","STAR"):
                operator=self.previous
                right=self.unary()
                expr=[operator,expr,right]
            return expr
        
        def unary(self):
            if self.match("BANG","MINUS"):
                operator=self.previous
                right=self.unary()
                return [operator,right]
            return self.primary()

        def primary(self):
            if self.match("FALSE"):
                return "false"
            if self.match("TRUE"):
                return "true"
            if self.match("NIL"):
                return "nil"
            if self.match("NUMBER","STRING"):
                return self.previous
            if self.match("LEFT_PAREN"):
                expr=self.expression()
                self.consume("RIGHT_PAREN","Expect ')' after expression.")
                return expr
            error=self.peek()
            self.error(error,"Expect expression.")

        def match(self,*types):
            for type in types:
                if self.check(type):
                    self.advance()
                    return True
            return False
        
        def check(self,type):
            if self.is_at_end():
                return False
            return self.peek()["type"]==type

        def advance(self):
            if not self.is_at_end():
                self.current+=1
            return self.previous_token()

        def is_at_end(self):
            return self.peek()["type"]=="EOF"

        def peek(self):
            return self.tokens[self.current]

        def previous_token(self):
            return self.tokens[self.current-1]

        def consume(self,type,message):
            if self.check(type):
                return self.advance()
            self.error(self.peek(),message)

        def error(self,token,message):
            parser_errors=True
            error_message=(f"[line {token['line']}] Error at '{token['type']}': {message}")
            parse_result.append(error_message)

    parser=parser(tokens)
    parse_result.append(parser.expression())
    return parse_result,parser_errors


if __name__ == "__main__":
    main()

