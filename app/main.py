import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize/parse/evaluate <filename>", file=sys.stderr)
        exit(1)
    
    command = sys.argv[1]
    filename = sys.argv[2]
    
    try:
        with open(filename, "r") as file:
            source = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        exit(1)
    
    # Tokenize
    tokens, lex_errors = tokenize(source)
    if lex_errors:
        exit(65)
    
    # Parse
    ast, parse_errors = parse(tokens)
    if parse_errors:
        exit(65)
    
    if command == "parse":
        # Convert AST to string for display.
        for node in ast:
            print(ast_to_string(node))
        exit(0)
    elif command == "evaluate":
        result = evaluate(ast)
        print(result)
        exit(0)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

#########################
# Tokenizer
#########################
def tokenize(source):
    tokens = []
    lex_errors = False
    i = 0
    line_number = 1

    while i < len(source):
        c = source[i]
        if c == '(':
            tokens.append("LEFT_PAREN ( null")
            i += 1
        elif c == ')':
            tokens.append("RIGHT_PAREN ) null")
            i += 1
        elif c == '"':
            # Start of string literal.
            start = i + 1
            i += 1
            while i < len(source) and source[i] != '"':
                i += 1
            if i < len(source) and source[i] == '"':
                value = source[start:i]
                # Token format: STRING "value" value
                tokens.append(f'STRING "{value}" {value}')
                i += 1
            else:
                tokens.append(f"[line {line_number}] Error: Unterminated string.")
                lex_errors = True
        elif c.isdigit():
            # For simplicity, we assume a number is a sequence of digits with an optional dot.
            start = i
            while i < len(source) and source[i].isdigit():
                i += 1
            if i < len(source) and source[i] == '.':
                i += 1
                while i < len(source) and source[i].isdigit():
                    i += 1
            value = source[start:i]
            tokens.append(f"NUMBER {value} {float(value)}")
        elif c in " \t":
            i += 1
        elif c == '\n':
            line_number += 1
            i += 1
        elif source.startswith("true", i):
            tokens.append("TRUE true null")
            i += 4
        elif source.startswith("false", i):
            tokens.append("FALSE false null")
            i += 5
        else:
            # Ignore any unrecognized character for simplicity.
            i += 1

    tokens.append("EOF  null")
    return tokens, lex_errors

#########################
# Parser
#########################
def parse(tokens):
    current = 0
    ast = []
    parse_errors = False

    def expression():
        return primary()

    def primary():
        nonlocal current, parse_errors
        token = tokens[current]
        # If token is a STRING literal, return its inner value.
        if token.startswith("STRING"):
            current += 1
            # Token format: STRING "value" value
            # We split by the quote character; index 1 is the inner value.
            return token.split('"', 2)[1]
        # If token is a NUMBER literal, return a float.
        if token.startswith("NUMBER"):
            current += 1
            return float(token.split()[2])
        # If token is a TRUE literal, return True.
        if token.startswith("TRUE"):
            current += 1
            return True
        # If token is a FALSE literal, return False.
        if token.startswith("FALSE"):
            current += 1
            return False
        # Grouping: if token is LEFT_PAREN.
        if token.startswith("LEFT_PAREN"):
            current += 1  # consume '('
            expr = expression()
            if not check("RIGHT_PAREN"):
                error(peek(), "Expected ')' after expression.")
                parse_errors = True
                return None
            current += 1  # consume ')'
            return grouping(expr)
        
        error(token, "Unexpected expression")
        parse_errors = True
        return None

    def grouping(expr):
        # Create a grouping node. When printing AST, this will show as (group <expr>).
        return ("group", expr)

    def check(token_type):
        return tokens[current].startswith(token_type)

    def peek():
        return tokens[current]

    def error(token, message):
        print(f"[line {token.split()[1]}] Error: {message}", file=sys.stderr)

    # Start parsing: for this example we parse one expression.
    ast.append(expression())
    return ast, parse_errors

# Helper to convert AST to a string for parse mode.
def ast_to_string(node):
    if isinstance(node, tuple) and node[0] == "group":
        # Format as (group <inner>)
        return f"(group {ast_to_string(node[1])})"
    else:
        return str(node)

#########################
# Evaluator
#########################
def evaluate(ast):
    # Assume ast is a list with one expression.
    return evaluate_expr(ast[0])

def evaluate_expr(node):
    if isinstance(node, tuple) and node[0] == "group":
        # Unwrap grouping by evaluating its inner expression.
        return evaluate_expr(node[1])
    elif isinstance(node, float):
        # If a float is actually an integer, convert it.
        int_value = int(node)
        if int_value == node:
            return int_value
        return node
    elif isinstance(node, bool):
        # Return booleans as lowercase strings (if required).
        return str(node).lower()
    elif isinstance(node, str):
        return node
    else:
        print(f"Unknown expression type: {node}", file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()
