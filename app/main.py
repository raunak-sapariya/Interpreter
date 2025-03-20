import sys

def main():
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize/parse/evaluate <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]
    
    # Read the file contents
    try:
        with open(filename, "r") as file:
            file_contents = file.read()
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        exit(1)


    # Tokenize the file contents
    tokens, lex_errors = tokenize(file_contents)

    if command == "tokenize":
        for token in tokens:
             if token.startswith("[line"):
                 print(token, file=sys.stderr)
             else:
                 print(token)
        if lex_errors:
             exit(65)
        else:
             exit(0)

    # Parse the tokens
    ast, parser_errors = parse(tokens)
    if parser_errors:
        exit(65)

    if command == "parse":
        # Print the AST using the ast_to_string function
        for node in ast:
            print(ast_to_string(node))
        exit(0)

    # Evaluate the AST
    elif command == "evaluate":
        result = evaluate(ast)
        if result is not None:
            print(result)
        exit(0)

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
                case ".":
                    tokens.append("DOT . null")
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
                case "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9": 
                    start = pointer
                    while pointer + 1 < len(file_contents) and file_contents[pointer+1] in "0123456789":
                        pointer += 1
                    if pointer + 1 < len(file_contents) and file_contents[pointer+1] == ".":
                        if pointer + 2 < len(file_contents) and file_contents[pointer+2] in "0123456789":
                            pointer += 2
                            while pointer + 1 < len(file_contents) and file_contents[pointer+1] in "0123456789":
                                pointer += 1
                        while pointer + 1 < len(file_contents) and file_contents[pointer+1] in "0123456789":
                            pointer += 1
                    value = file_contents[start:pointer+1]
                    tokens.append(f"NUMBER {value} {float(value)}")
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
    current=0
    parse_result=[]
    parser_errors=False

    # Grammar Rules
    def expression():
        expr=equality()
        return expr
    
    def equality():
        expr=comparison()
        while match("BANG_EQUAL","EQUAL_EQUAL"):
            operator=previous().split()[1]
            right=comparison()
            expr=Binary(expr,operator,right)
        return expr
    
    def match(*types) -> bool:
        for type in types:
            if check(type):
                advance()
                return True
        return False
    
    # Consumes the token if it matches the type else raises an error
    def consume(type,message):
        if check(type):
            return advance()
        error(peek(),message)
        return None
    
    def check(type) -> bool:
        if isAtEnd():
            return False
        return peek().startswith(type)
    
    def advance():
        nonlocal current
        if not isAtEnd():
            current+=1
        return previous()
    
    def isAtEnd() -> bool:
        return peek().startswith("EOF")
                
    def peek():
        return tokens[current]

    def previous():
        return tokens[current-1]
    
    # Error Handling
    def report(token,where,message):
        print(f"[line {token.split()[1]}] Error{where}: {message}", file=sys.stderr)
    
    # Error Handling 
    def error(token, message):
        nonlocal parser_errors
        parser_errors=True
        if token.startswith("EOF"):
            report(token, " at end", message)
        else:
            report(token, f" at '{token.split()[1]}'", message)
        return None
    
    def comparison():
        expr=term()
        while match ("GREATER","GREATER_EQUAL","LESS","LESS_EQUAL"):
            operator=previous().split()[1]
            right=term()
            expr=Binary(expr,operator,right)
        return expr
    
    def term ():
        expr=factor()
        while match("MINUS","PLUS"):
            operator=previous().split()[1]
            right=factor()
            expr=Binary(expr,operator,right)
        return expr
    
    def factor():
        expr=unary()
        while match("STAR","SLASH"):
            operator=previous().split()[1]
            right=unary()
            expr=Binary(expr,operator,right)
        return expr
    
    def unary():
        if match("BANG","MINUS"):
            operator=previous().split()[1]
            right=unary()
            return Unary(operator,right)
        return primary()
    
    def primary():
        try:
            if match("FALSE"):
                return Literal("false")
            if match("TRUE"):
                return Literal("true")
            if match("NIL"):
                return Literal("nil")
            if match("NUMBER"):
                return float(previous().split()[2])
            if match("STRING"):
                return previous().split('"',2)[1]
            if match("LEFT_PAREN"):
                expr=expression()
                closing= consume("RIGHT_PAREN","Expected ')' after expression.")
                if closing is None:
                    return None
                return grouping(expr)
            
            error(peek(), "Unexpected expression")
            return None
            
        except Exception as e:
            print(f"Error in primary: {e}", file=sys.stderr)
            return None
    
    # AST Node 
    def Binary(left,operator,right):
        return ("binary", operator, left, right)

    def Unary(operator,right):
        return ("unary", operator, right)

    def Literal(value):
        return ("literal", value)

    def grouping(expr):
        return ("group", expr)
    
    parse_result.append(expression())
    if parser_errors :
        return parse_result, True
    return parse_result, False
    


def evaluate(parse_result):

    def isTruthy(value) -> str:
        if value == "false" or value == "nil":
            return "true"
        return "false"


    
    def evaluate_expr(expr):

        if isinstance(expr, tuple):
            tag = expr[0]

            if tag == "group":
                return evaluate_expr(expr[1])
            
            elif tag == "literal":
                return expr[1]
            
            elif tag == "unary":
                right = evaluate_expr(expr[2])
                if expr[1] == "-":
                    return -right
                elif expr[1] == "!":
                    return isTruthy(right)
                else:
                    print(f"Unknown unary operator: {expr[1]}", file=sys.stderr)
                    exit(1)

            else:
                print(f"Unknown expression tag: {tag}", file=sys.stderr)
                exit(1)
        
        elif isinstance(expr, float):
            int_value = int(expr)
            if int_value == expr:
                return int_value
            else:
                return expr
            
        elif isinstance(expr, bool):
            return expr
        
        elif isinstance(expr, str):
            return (expr)
            
        else:
            print(f"Unknown expression type: {expr}", file=sys.stderr)
            exit(1)

    for expr in parse_result:
        if expr is not None:
            result = evaluate_expr(expr)
            print(result)
        else:
            print("Error: Unable to evaluate expression.", file=sys.stderr)
            exit(1)

    exit(0)


    

# Helper function
def ast_to_string(node):
    if isinstance(node, tuple) :
        tag = node[0]
        if tag == "group":
            return f"(group {ast_to_string(node[1])})"
        elif tag == "binary":
            return f"({node[1]} {ast_to_string(node[2])} {ast_to_string(node[3])})"
        elif tag == "unary":
            return f"({node[1]} {ast_to_string(node[2])})"
        elif tag == "literal":
            return str(node[1])
        else:
            return str(node)
    else:
        return str(node)
        

    

if __name__ == "__main__":
    main()

