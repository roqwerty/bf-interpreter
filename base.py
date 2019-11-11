# Interpreter for Brainfuck (reading from file FUTURE line-by line w/visual)
# C Ethan Brucker
# Version 11-8-19
# Symbols:
#   + - : Increment, Decrement
#   > < : Shift right, shift left
#   [ ] : If value != 0, jump to end bracket; if value != 0, jump to beginning
#       bracket (do nesting correctly)

import colorama as co
co.init() # For colored text
import sys # If activated command-line with the name of the file, runs
    #   instructions and shows output the entire time

def parse(code):
    # Take a raw code input and format it nicely to be used by the program
    parsed = ''
    for char in code:
        if char in ['+', '-', '<', '>', '[', ']']:
            parsed += char
    return parsed

def display(mem, index): # FUTURE add current action
    # Displays all the values of memory in a nice fashion
    i = 0
    for element in mem:
        # Change the color if selected
        if index == i:
            print(co.Fore.LIGHTMAGENTA_EX, end='')
        # Formatting
        print("{:03.0f} ".format(element), end='')

        # Undo the color switch
        if index == i:
            print(co.Style.RESET_ALL, end='')
        
        i += 1
    print()

# 6 specific functions
def increment(mem, index): # Loops at 255
    mem[index] += 1
    if mem[index] >= 256:
        mem[index] = 0

def decrement(mem, index):
    mem[index] -= 1
    if mem[index] < 0:
        mem[index] = 255

def left(mem, index):
    # Move
    index -= 1

    # If we went back through the beginning, move the entire freaking memory
    if index < 0:
        index = 0
        mem.insert(0, 0) # Insert, at position 0, the value zero

    return index

def right(mem, index):
    # Move
    index += 1

    # Create a new value if it doesn't have it
    if len(mem) is index:
        mem.append(0)

    return index

def open_bracket(mem, index, code, code_index):
    # If @index = 0, jump to corresponding closing brace

    # Test to see whether the index is zero (if not, nothing happens)
    if mem[index] is 0:
        # Count through the code, modifying layer until we get one that matches
        layer = 0
        counter = code_index + 1 # Don't start right on the [
        while True:
            try:
                if (code[counter] is ']') and layer == 0:
                    return counter # This is the new code index
                elif code[counter] is '[':
                    layer += 1
                elif code[counter] is ']':
                    layer -= 1
                counter += 1
            except:
                # Ran out of code before closing bracket
                print("Expected closing bracket for opening at " + code_index)
                return code_index
    return code_index

def close_bracket(mem, index, code, code_index):
    # If index is not 0, jump back to corresponding opening brace

    # Test to see whether the index is not zero
    if mem[index] is not 0:
        # Count back through the code (much like open_bracket())
        layer = 0
        counter = code_index - 1 # Don't start on the ]
        while True:
            try:
                if (code[counter] is '[') and layer == 0:
                    return counter # This is the new index
                elif code[counter] is ']':
                    layer += 1
                elif code[counter] is '[':
                    layer -= 1
                counter -= 1
            except:
                # Ran out of code
                print("Expected opening bracket for closing at " + code_index)
                return code_index
    return code_index

# Main function
def main():
    # Help flag
    if "-h" in sys.argv:
        print()
        print("Activation: base.py <optional_code_file> <args>")
        print("Arguments:")
        print("   -h: This help menu")
        print("   -v: Verbose mode (telegraphs each step)")
        print()
        exit()
    
    # Assemble the "infinite" memory
    mem = []
    index = 0
    layer = 0 # Layer for brackets
    code_index = 0
    mem.append(0) # Create index 0

    # Total code
    #total_code = "" # A placeholder string to save the entire code, line by line

    # Verbose flag
    verbose = False
    if "-v" in sys.argv: # Literally just checks to see if it exists
        verbose = True

    # Run a file if input by the user
    try: # If they added the name of a file
        with open(sys.argv[1], "r") as file:
            code = parse(file.read())

        while code_index < len(code): # End by going through entire program

            if verbose:
                display(mem, index) # Display each step if verbose
            
            if code[code_index] is '+':
                increment(mem, index)
            elif code[code_index] is '-':
                decrement(mem, index)
            elif code[code_index] is "<":
                index = left(mem, index)
            elif code[code_index] is ">":
                index = right(mem, index)
            elif code[code_index] is '[':
                code_index = open_bracket(mem, index, code, code_index)
            elif code[code_index] is ']':
                code_index = close_bracket(mem, index, code, code_index)

            code_index += 1
    except:
        pass

    
    # Get input line by line from the user
    while True:
        display(mem, index) # Display the current situation of memory
        code = parse(input("Code: "))
        code_index = 0

        '''
        if code.lower() is "save":
            with open("output.txt", "w+") as f:
                f.write(total_code)
                
        total_code += code
        '''

        while code_index < len(code): # End by going through entire program

            if verbose:
                display(mem, index) # Display each step if verbose
            
            if code[code_index] is '+':
                increment(mem, index)
            elif code[code_index] is '-':
                decrement(mem, index)
            elif code[code_index] is "<":
                index = left(mem, index)
            elif code[code_index] is ">":
                index = right(mem, index)
            elif code[code_index] is '[':
                code_index = open_bracket(mem, index, code, code_index)
            elif code[code_index] is ']':
                code_index = close_bracket(mem, index, code, code_index)
            
            code_index += 1

        #total_code += "\n"

if __name__ == "__main__":
    main()
