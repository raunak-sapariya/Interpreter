import sys

def main():
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize/parse/evaluate/run <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    # Read the file contents.
    try:
        with open(filename, "r") as file:
            file_contents = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        exit(1)

    # Tokenize the file contents.
    tokens, lex_errors, line_number = tokenize(file_contents)
    if command == "tokenize":
        for token in tokens:
            if token.startswith("[line"):
                print(token, file=sys.stderr)
            else:
                print(token)
        exit(65 if lex_errors else 0)

    # Parse the tokens.
    ast, parser_errors = parse(tokens)
    if parser_errors:
        exit(65)

    if command == "parse":
        for node in ast:
            print(ast_to_string(node))
        exit(0)

    # Evaluate the AST.
    if command == "evaluate":
        evaluate(ast, line_number)
        exit(0)

    # Run the program (only explicit print statements produce output).
    if command == "run":
        run(ast, line_number)
        exit(0)

    print(f"Unknown command: {command}", file=sys.stderr)
    exit(1)


def tokenize(file_contents):
    """
    Converts the input string into a list of tokens.
    Returns a tuple: (tokens, lexical_errors, last_line_number)
    """
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
                if pointer + 1 < len(file_contents) and (file_contents[pointer + 1] in ("/", "*")):
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
            case " " | "\t":
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
                    tokens.append(f"[line {line_number}] Error: Unterminated string.")
                    lexical_errors = True
                    pointer += 1
            case _ if char in "0123456789":
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
            case _ if char.isalpha() or char == "_" or char in "0123456789":
                start = pointer
                while pointer + 1 < len(file_contents) and (file_contents[pointer + 1].isalnum() or file_contents[pointer + 1] == "_"):
                    pointer += 1
                value = file_contents[start:pointer + 1]
                keywords = ["and", "class", "else", "false", "for", "fun", "if", "nil", "or", "print", "return", "super", "this", "true", "var", "while"]
                if value in keywords:
                    tokens.append(f"{value.upper()} {value} null")
                else:
                    tokens.append(f"IDENTIFIER {value} null")
                pointer += 1
            case _:
                tokens.append(f"[line {line_number}] Error: Unexpected character: {char}")
                lexical_errors = True
                pointer += 1

    tokens.append("EOF  null")
    return tokens, lexical_errors, line_number


def parse(tokens):
    """
    Parses the list of tokens into an abstract syntax tree (AST).
    Returns a tuple: (statements, parser_errors)
    """
    current = 0
    parser_errors = False
    statements = []

    def expression():
        expr=equality()
        return expr
    
    def equality():
        expr = comparison()
        while match("BANG_EQUAL", "EQUAL_EQUAL"):
            operator = previous().split()[1]
            right = comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison():
        expr = term()
        while match("GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"):
            operator = previous().split()[1]
            right = term()
            expr = Binary(expr, operator, right)
        return expr

    def term():
        expr = factor()
        while match("MINUS", "PLUS"):
            operator = previous().split()[1]
            right = factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor():
        expr = unary()
        while match("STAR", "SLASH"):
            operator = previous().split()[1]
            right = unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary():
        if match("BANG", "MINUS"):
            operator = previous().split()[1]
            right = unary()
            return Unary(operator, right)
        return primary()

    def primary():
        try:
            if match("FALSE"):
                return Literal(False)
            if match("TRUE"):
                return Literal(True)
            if match("NIL"):
                return Literal(None)
            if match("NUMBER"):
                return float(previous().split()[2])
            if match("STRING"):
                return previous().split('"', 2)[1]
            if match("LEFT_PAREN"):
                expr = expression()
                if consume("RIGHT_PAREN", "Expected ')' after expression.") is None:
                    return None
                return grouping(expr)
            error(peek(), "Unexpected expression")
            return None
        except Exception as e:
            print(f"Error in primary: {e}", file=sys.stderr)
            return None

    def statement():
        # Handle print statement.
        if match("PRINT"):
            expr = expression()
            # Allow optional semicolon at EOF.
            if not isAtEnd():
                consume("SEMICOLON", "Expected ';' after expression.")
            return ("print", expr)
        else:
            expr = expression()
            if not isAtEnd():
                consume("SEMICOLON", "Expected ';' after expression.")
            return ("expression", expr)

    def match(*types) -> bool:
        nonlocal current
        for t in types:
            if check(t):
                advance()
                return True
        return False

    def consume(token_type, message):
        if check(token_type):
            return advance()
        error(peek(), message)
        return None

    def check(token_type) -> bool:
        if isAtEnd():
            return False
        return peek().startswith(token_type)

    def advance():
        nonlocal current
        if not isAtEnd():
            current += 1
        return previous()

    def isAtEnd() -> bool:
        return peek().startswith("EOF")

    def peek():
        return tokens[current]

    def previous():
        return tokens[current - 1]

    def error(token, message):
        nonlocal parser_errors
        parser_errors = True
        if token.startswith("EOF"):
            report(token, " at end", message)
        else:
            report(token, f" at '{token.split()[1]}'", message)
        return None

    def report(token, where, message):
        print(f"[line {token.split()[1]}] Error{where}: {message}", file=sys.stderr)

    while not isAtEnd():
        stmt = statement()
        if stmt is None:
            parser_errors = True
            print("Error: Unable to parse statement.", file=sys.stderr)
            exit(1)
        statements.append(stmt)
    return statements, parser_errors


def evaluate_expr(expr, line_number):
    """
    Recursively evaluates an expression AST node.
    Returns the computed value.
    """
    def isTruthy(value):
        return value is not None and value is not False

    def convertNumber(value):
        if isinstance(value, float):
            int_value = int(value)
            if int_value == value:
                return int_value
        return value

    def checkNumberOperand(operator, operand):
        if isinstance(operand, bool) or not isinstance(operand, (int, float)):
            print(f"[Line {line_number}] Error: Operand must be a number, not '{operand}'", file=sys.stderr)
            exit(70)

    def checkNumberOperands(operator, left, right):
        if (isinstance(left, bool) or isinstance(right, bool) or
            not isinstance(left, (int, float)) or not isinstance(right, (int, float))):
            print(f"[Line {line_number}] Error: Operands must be numbers, not '{left}' and '{right}'", file=sys.stderr)
            exit(70)

    def checkAdditionOperands(operator, left, right):
        if (isinstance(left, str) and not isinstance(right, str)) or (not isinstance(left, str) and isinstance(right, str)):
            print(f"[Line {line_number}] Error: Operands for '+' must be both numbers or both strings, not '{left}' and '{right}'", file=sys.stderr)
            exit(70)

    if isinstance(expr, tuple):
        tag = expr[0]

        if tag == "group":
            return evaluate_expr(expr[1], line_number)

        elif tag == "literal":
            return expr[1]

        elif tag == "unary":
            right = evaluate_expr(expr[2], line_number)
            if expr[1] == "-":
                checkNumberOperand(expr[1], right)
                return convertNumber(-float(right))
            elif expr[1] == "!":
                return not isTruthy(right)
            else:
                print(f"Unknown unary operator: {expr[1]}", file=sys.stderr)
                exit(1)

        elif tag == "binary":
            left = evaluate_expr(expr[2], line_number)
            right = evaluate_expr(expr[3], line_number)
            if expr[1] == "*":
                checkNumberOperands(expr[1], left, right)
                return convertNumber(left * right)
            elif expr[1] == "/":
                checkNumberOperands(expr[1], left, right)
                return convertNumber(left / right)
            elif expr[1] == "+":
                checkAdditionOperands(expr[1], left, right)
                return left + right
            elif expr[1] == "-":
                checkNumberOperands(expr[1], left, right)
                result = left - right
            elif expr[1] == "<":
                checkNumberOperands(expr[1], left, right)
                return left < right
            elif expr[1] == "<=":
                checkNumberOperands(expr[1], left, right)
                return left <= right
            elif expr[1] == ">":
                checkNumberOperands(expr[1], left, right)
                return left > right
            elif expr[1] == ">=":
                checkNumberOperands(expr[1], left, right)
                return left >= right
            elif expr[1] == "==":
                return left == right
            elif expr[1] == "!=":
                return left != right
            else:
                print(f"Unknown binary operator: {expr[1]}", file=sys.stderr)
                exit(1)
        else:
            print(f"Unknown expression tag: {tag}", file=sys.stderr)
            exit(1)

    elif isinstance(expr, float):
        return convertNumber(expr)
    
    elif isinstance(expr, bool):
        return expr

    elif isinstance(expr, str):
        return expr
            
    else:
        print(f"Unknown expression type: {expr}", file=sys.stderr)
        exit(1)


def evaluate(statements, line_number):
    """
    Evaluates each statement and prints the result of every expression.
    This command is used in testing to show the evaluation result of each statement.
    """
    for stmt in statements:
        if stmt[0] == "expression":
            result = evaluate_expr(stmt[1], line_number)
            if isinstance(result, bool):
                print("true" if result else "false")
            elif result is None:
                print("nil")
            else:
                print(result)
        elif stmt[0] == "print":
            result = evaluate_expr(stmt[1], line_number)
            print(stringify(result))
        else:
            print(f"Unknown statement type: {stmt[0]}", file=sys.stderr)
            exit(1)
    exit(0)


def run(statements, line_number):
    """
    Runs the list of statements.
    Only explicit print statements produce output;
    bare expression statements are evaluated for side effects.
    """
    for stmt in statements:
        if stmt[0] == "print":
            result = evaluate_expr(stmt[1], line_number)
            print(stringify(result))
        elif stmt[0] == "expression":
            evaluate_expr(stmt[1], line_number)
        else:
            print(f"Unknown statement type: {stmt[0]}", file=sys.stderr)
            exit(1)


# AST Node constructors.
def Binary(left, operator, right):
    return ("binary", operator, left, right)

def Unary(operator, right):
    return ("unary", operator, right)

def Literal(value):
    return ("literal", value)

def grouping(expr):
    return ("group", expr)


# Helper function to convert values to strings
def stringify(value):
    """Converts a value to a string for printing."""
    if isinstance(value, bool):
        return "true" if value else "false"
    elif value is None:
        return "nil"
    elif isinstance(value, float):
        return str(int(value)) if int(value) == value else str(value)
    elif isinstance(value, str):
        return value
    else:
        return str(value)


# Helper function
def ast_to_string(node):
    """Returns a string representation of the AST node."""
    if isinstance(node, tuple):
        tag = node[0]
        if tag == "group":
            return f"(group {ast_to_string(node[1])})"
        elif tag == "binary":
            return f"({node[1]} {ast_to_string(node[2])} {ast_to_string(node[3])})"
        elif tag == "unary":
            return f"({node[1]} {ast_to_string(node[2])})"
        elif tag == "literal":
            value = node[1]
            if isinstance(value, bool):
                return "true" if value else "false"
            elif value is None:
                return "nil"
        else:
            return str(node)
    else:
        return str(node)
        

    

if __name__ == "__main__":
    main()

