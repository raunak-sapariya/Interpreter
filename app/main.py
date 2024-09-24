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
        # print(tokens)
        # print()
        # print(parse_result)
        for result in parse_result:
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
    token_len=len(tokens)
    fst=0
    previous=fst-1
    last=len(tokens)-1
    parser_errors=False
    parse_result=[]

    def extract_value(token):
    # Handle extracting actual value from tokens like STRING, NUMBER, TRUE, FALSE, NIL
        if token.startswith("STRING"):
            return token.split('"')[1]  # Extract the actual string value
        elif token.startswith("NUMBER"):
            return token.split()[1]  # Extract the number value
        elif token.startswith("TRUE"):
            return "true"
        elif token.startswith("FALSE"):
            return "false"
        elif token.startswith("NIL"):
            return "nil"
        else:
            return token  # For other tokens, return as is


    while  fst < token_len:
        token=tokens[fst]
        if token.startswith("TRUE"):parse_result.append("true")
        elif token.startswith("FALSE"):parse_result.append("false")
        elif token.startswith("NIL"):parse_result.append("nil")
        elif token.startswith("NUMBER"):parse_result.append(float(token.split()[1]))
        elif token.startswith("STRING"):parse_result.append(token.split('"')[1])
        elif token.startswith("LEFT_PAREN"):
            fst += 1  # Move past the LEFT_PAREN token
            l = []  # List to store tokens inside the parentheses
            nested_count = 1  # Track nested parentheses

            while fst < token_len and nested_count > 0:
                current_token = tokens[fst]

                if current_token.startswith("LEFT_PAREN"):
                    # Recursively parse the inner group
                    fst += 1
                    group_tokens = []
                    while fst < token_len and not tokens[fst].startswith("RIGHT_PAREN"):
                        group_tokens.append(tokens[fst])
                        fst += 1

                    if fst < token_len and tokens[fst].startswith("RIGHT_PAREN"):
                        value = f"(group {' '.join([extract_value(t) for t in group_tokens])})"
                        l.append(value)  # Add the grouped value as a token
                        nested_count -= 1
                    else:
                        parser_errors = True
                        print("Error: Unterminated parentheses")
                        break

                elif current_token.startswith("RIGHT_PAREN"):
                    nested_count -= 1  # Reduce the nesting level
                    if nested_count > 0:
                        l.append(current_token)  # Add the RIGHT_PAREN if it's not the closing one for the current group
                else:
                    l.append(extract_value(current_token))  # Use extract_value to get the actual token value

                fst += 1  # Move to the next token

            if nested_count == 0:
                # Successfully closed all nested parentheses
                value = f"(group {' '.join(l)})"
                parse_result.append(value)  # Append the grouped result
            else:
                # If we exit the loop with unbalanced parentheses
                parser_errors = True
                print("Error: Unterminated nested parentheses")

            fst += 1  # Move past the last RIGHT_PAREN


        
            

                


        fst+=1
    return parse_result,parser_errors



if __name__ == "__main__":
    main()

