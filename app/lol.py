a=6.
print(a) # case "'":
                #     start = pointer
                #     if pointer + 2 < len(file_contents) and (file_contents[pointer + 1] == "'" and file_contents[pointer + 2] == "'" and file_contents[pointer - 1] == "="):
                #         pointer += 3
                #         while pointer + 1 < len(file_contents) and not(file_contents[pointer] == "'" and file_contents[pointer + 1] == "'" and file_contents[pointer + 2] == "'"):
                #             pointer += 1
                #         if pointer + 1 < len(file_contents) and (file_contents[pointer] == "'" and file_contents[pointer + 1] == "'" and file_contents[pointer + 2] == "'"):
                #             value = file_contents[start + 3:pointer]
                #             pointer += 3
                #             tokens.append(f"STRING '{value}' {value}")
                #         else:
                #             tokens.append(f"[line {line_number}] Error: Unterminated MULTI-LINE STRING ''' '''.")
                #             lexical_errors = True
                #             pointer += 1
                #     elif(pointer + 1 < len(file_contents) and file_contents[pointer - 1] == "="):
                #         while pointer + 1 < len(file_contents) and file_contents[pointer + 1] != "'":
                #             pointer += 1
                #         if pointer + 1 < len(file_contents) and file_contents[pointer + 1] == "'":
                #             value = file_contents[start + 1:pointer + 1]
                #             tokens.append(f"STRING '{value}' {value}")
                #             pointer += 2
                #         else:
                #             tokens.append(f"[line {line_number}] Error: Unterminated string.")
                #             lexical_errors = True
                #             pointer += 1
                #     elif(file_contents[pointer - 1] != "="):
                #         if pointer + 2 < len(file_contents) and (file_contents[pointer + 1] == "'" and file_contents[pointer + 2] == "'" and file_contents[pointer - 1] != "="):
                #             pointer += 3
                #             while pointer < len(file_contents) and not(file_contents[pointer] == "'" and file_contents[pointer + 1] == "'" and file_contents[pointer + 2] == "'"):
                #                 pointer += 1
                #             pointer += 3
                #         else:
                #             tokens.append(f"[line {line_number}] Error: Multi-Line Comment.[''' ''']")
                #             lexical_errors = True
                #             pointer += 1
                #     else:
                #         tokens.append(f"[line {line_number}] Error: Invalid use of single quote.")
                #         lexical_errors = True
                #         pointer += 1