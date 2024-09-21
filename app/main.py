import sys

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # print(len(sys.argv))
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


    print(f"Command: {command}",f"Filename: {filename}", file=sys.stderr)
    
    if command == "tokenize":
        for tokenn in token(file_contents):
            print(tokenn)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)


# Implementing scanner here
def token(file_contents):
        try:
            

            line_number = 1
            lexical_errors=False
            pointer = 0

            while pointer < len(file_contents):
                char=file_contents[pointer]        

                match char:
                    case "(":
                            yield("LEFT_PAREN ( null")
                            pointer += 1

                    case ")":
                            yield("RIGHT_PAREN ) null")
                            pointer += 1

                    case "{":
                            yield("LEFT_BRACE { null")
                            pointer += 1

                    case "}":
                            yield("RIGHT_BRACE } null")
                            pointer += 1

                    case",":
                            yield("COMMA , null")
                            pointer += 1

                    case"-":
                            yield("MINUS - null")
                            pointer += 1

                    case"+":
                            yield("PLUS + null")
                            pointer += 1

                    case";":
                            yield("SEMICOLON ; null")
                            pointer += 1

                    case"*":
                            yield("STAR * null")
                            pointer += 1

                    case"=":
                        if  pointer+1 < len(file_contents) and file_contents[pointer+1]=="=":
                            yield("EQUAL_EQUAL == null")
                            pointer += 2

                        else:
                            yield("EQUAL = null")
                            pointer += 1

                    case "!":
                        if pointer+1 <len(file_contents) and file_contents[pointer+1]=="=":
                            yield("BANG_EQUAL != null")
                            pointer +=2
                        else :
                            yield("BANG ! null")
                            pointer +=1

                    case "<":
                        if pointer+1 < len(file_contents) and file_contents[pointer+1]=="=":
                            yield("LESS_EQUAL <= null")
                            pointer +=2
                        #HTML COMMENT <!-- -->
                        elif(pointer+1 <len(file_contents) and (file_contents[pointer+1]=="!" and file_contents[pointer+2:pointer+3]=="-")): 
                            if pointer+3 <len(file_contents) and (file_contents[pointer+1]=="!" and file_contents[pointer+2:pointer+3]=="-"):
                                pointer+=3
                                while pointer < len(file_contents) and not (file_contents[pointer:pointer+1]=="-" and file_contents[pointer+2]==">"):
                                    pointer+=1
                                pointer+=3
                            else:
                                r=(f"[line {line_number}] Error: HTML Comment.[<!-- -->]")
                                lexical_errors = True
                                pointer += 1
                        else :
                            yield("LESS < null")
                            pointer +=1

                    case ">": 
                        if pointer+1 < len(file_contents) and file_contents[pointer+1]=="=":
                            yield("GREATER_EQUAL >= null")
                            pointer +=2
                        else :
                            yield("GREATER > null")
                            pointer +=1

                    #COMMENT AND DIVISION // /**/
                    case "/":
                        if pointer+1 < len(file_contents) and (file_contents[pointer+1]=="/" or file_contents[pointer+1]=="*"):
                            #SINGLE-LINE COMMENT //
                            if file_contents[pointer+1]=="/":
                                while pointer < len(file_contents) and file_contents[pointer]!="\n":
                                    pointer +=1
                            #MULTI-LINE COMMENT /* */
                            elif file_contents[pointer+1]=="*":
                                while  pointer < len(file_contents) and not (file_contents[pointer]=="*" and file_contents[pointer+1]=="/"):
                                    pointer +=1 
                                pointer +=2
                        else:
                            yield("SLASH / null")
                            pointer += 1

                    #<SPACE> <TAB> <NEWLINE>
                    case " "|"\t":
                        pointer +=1
                        pass
                    case "\n":
                        pointer+=1
                        line_number+=1
                        pass

                    #STRINGS
                    #DOUBLE-QUOTE
                    case '"':
                        start = pointer
                        while pointer+1 < len(file_contents) and file_contents[pointer+1] != '"':
                            pointer+= 1
                        if pointer+1 < len(file_contents) and file_contents[pointer+1] == '"':
                            value = file_contents[start+1:pointer+1]
                            yield(f'STRING "{value}" {value}')
                            pointer += 2
                        else:
                            yield(f'[line {line_number}] Error: Unterminated string. " "')
                            lexical_errors = True
                            pointer += 1

                    #SINGLE-QUOTE
                    case "'":
                        start = pointer
                        #MILTI-LINE STRING ''' '''
                        if pointer+2 < len(file_contents) and (file_contents[pointer+1]=="'" and file_contents[pointer+2]=="'" and file_contents[pointer-1]=="="):
                            # if pointer+1 <len(file_contents) and (file_contents[pointer]=="'" and file_contents[pointer+1]=="'" and file_contents[pointer+2]=="'"):
                            pointer+=3
                            while pointer+1 < len(file_contents) and not(file_contents[pointer]=="'" and file_contents[pointer+1]=="'" and file_contents[pointer+2]=="'"):
                                pointer+=1
                            if pointer+1 <len(file_contents) and (file_contents[pointer]=="'" and file_contents[pointer+1]=="'" and file_contents[pointer+2]=="'"):
                                value = file_contents[start+3:pointer]
                                pointer+=3
                                yield(f"STRING '{value}' {value}")
                            else:
                                yield(f"[line {line_number}] Error: Unterminated MULTI-LINE STRING ''' '''.")
                                lexical_errors = True
                                pointer += 1

                        #SINGLT-LINE STRING ' '
                        elif(pointer + 1 < len(file_contents) and file_contents[pointer-1]=="="):
                            while pointer+1 < len(file_contents) and file_contents[pointer+1] != "'":
                                    pointer+= 1
                            if pointer+1 < len(file_contents) and file_contents[pointer+1] == "'":
                                    value = file_contents[start+1:pointer+1]
                                    yield(f"STRING '{value}' {value}")
                                    pointer += 2
                            else:
                                    yield(f"[line {line_number}] Error: Unterminated string.")
                                    lexical_errors = True
                                    pointer += 1

                        #FOR .PY FILE MULTI-LINE COMMENT ''' '''' 
                        elif(file_contents[pointer-1]!="="):
                            if pointer+2 <len(file_contents) and (file_contents[pointer+1]=="'" and file_contents[pointer+2]=="'" and file_contents[pointer-1]!="="):
                                    pointer+=3
                                    while pointer < len(file_contents) and not(file_contents[pointer]=="'" and file_contents[pointer+1]=="'" and file_contents[pointer+2]=="'"):
                                        pointer+=1
                                    pointer+=3
                            else:
                                yield(f"[line {line_number}] Error: Multi-Line Comment.[''' ''']")
                                lexical_errors = True
                                pointer += 1
                        else:
                            yield(f"[line {line_number}] Error: Invalid use of single quote.")
                            lexical_errors = True
                            pointer += 1

                    #NUMBERS 
                    case "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"|".":
                        start = pointer
                        if pointer+1 < len(file_contents) and  (file_contents[pointer+1] in"0123456789" or file_contents[pointer+1] == "."):
                            while pointer+1 < len(file_contents) and (file_contents[pointer+1] in"0123456789" or file_contents[pointer+1] == "."):
                                pointer += 1
                            if pointer+1 < len(file_contents) and file_contents[pointer+1] == ".":
                                pointer += 1
                                while pointer+1 < len(file_contents) and file_contents[pointer+1] in "0123456789":
                                    pointer += 1
                            value = file_contents[start:pointer+1]
                            yield(f"NUMBER {value} {float(value)}")
                            pointer += 1
                        else:
                            yield("DOT . null")
                            pointer += 1

                    #IDENTIFIERS AND RESERVED WORD
                    case  "a"|"b"|"c"|"d"|"e"|"f"|"g"|"h"|"i"|"j"|"k"|"l"|"m"|"n"|"o"|"p"|"q"|"r"|"s"|"t"|"u"|"v"|"w"|"x"|"y"|"z"|"A"|"B"|"C"|"D"|"E"|"F"|"G"|"H"|"I"|"J"|"K"|"L"|"M"|"N"|"O"|"P"|"Q"|"R"|"S"|"T"|"U"|"V"|"W"|"X"|"Y"|"Z"|"_"|"0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9":
                        start=pointer
                        while pointer+1 <len(file_contents) and file_contents[pointer+1] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789":
                            pointer+=1
                        value = file_contents[start:pointer+1]
                        Identifiers=["and","class","else","false","for","fun","if","nil","or","print","return","super","this","true","var","while"]
                        if value in Identifiers:
                            yield(f"{value.upper()} {value} null")
                        else:
                            yield(f"IDENTIFIER {value} null")
                        pointer += 1

                    #ERRORS
                    case "$"|"#"|"@"|"%"|_:
                        yield(f"[line {line_number}] Error: Unexpected character: {char}")
                        lexical_errors = True
                        pointer += 1 

            #end of file        
            yield("EOF  null")
            
            if lexical_errors:
                exit(65)
                
            else:
                exit(0)
                
        except Exception as e:
            yield(f"An unexpected error occurred: {str(e)}")
            exit(1)

if __name__ == "__main__":
    main()
