# Translates a text file of ABF (Assembly BF) into actual BF
# ALWAYS HOME TO NEG1
# INPUT1 INPUT2 OUTPUT1 SCRATCH/OUTPUT2/COPYBUFFER NEG1MARK STORAGE1 STORAGE2 ..
# SUPPORTED:
# Current:
#   m0 = 5 #m0 - 5      Comment (nothing happens after #)
#   del m0              Deletes m0
#   m0 + 5              Adds 5 to m0
#   m0 - 5              Subtracts 5 from m0
#   m0 = 5              Sets m0 to 5
#   m0 = m1             Copies m1 into m0
#   m0 + m1             Adds the value m1 into m0
#   m0 - m1             Subtracts the value m1 from m0 (and stores there)
#   m0 * 5              m0 = m0 * 5
#   m0 * m1             m0 = m0 * m1
#   pr XXX              Print 'XXX' to the screen (just 'pr' for newline)
#   prw XXX             Printraw XXX (no newline)
#   in m0               Takes input into m0
#   for m0 : m1 + 3     Do operation(s) for each time of m0 (DESTRUCTIVE)
#   'loop' && '!loop'   Loops everything between forever (Don't put in conditionals!)
#   raw +[-<+]-         Adds the code '+[-<+]-' raw into the final code (CAREFUL start & end at NEG1)
#
#   if m0 = 5: m0 = 10 : m0 + 1     If m0 == 5, do operation m0 = 10 and m0 + 1 (for all if statements)
#   if m0 = m1: m0 = 10     If m0 == m1, do operation m0 = 10
#   If statements conditional ['<', '<=', '>', '>=']
#   If statements COMPLETELY isolate commands seperated by ':'! (not other ifs...)
#
# Future:
#   !m0             Logical not m0
#   switch statements?
#   other raw logical operations?
#   lda m0              Loads the value at m0 into register a
#   ldb m0              Loads the value at m0 into register b
#   store m1            Stores the value at output into m1
#
# EXTRA Features:
# Function to remove redundant movement '><' or '<>' or '>><<' or '<><>'
# Function to convert numbers from ASCII to decimal
#
# BUGS:
# Can't print any of the 'operation' characters

# C Ethan Brucker
# Version 12-4-19

import sys # For command-line arguments

def first():
    # Sets up the NEG1MARK and homes there
    return '>>>>-'

def remove_extra_movement(code):
    # Removes all '><' or '<>' or '>><<' or '<><>'
    output = code
    while True:
        hit = False
        skip = False
        new_output = ''
        for i in range(len(output) - 1):
            if not skip:
                if output[i] == '>' and output[i+1] == '<':
                    # Remove the offenders
                    new_output = output[:i] + output[i+2:]
                    hit = True
                    skip = True
                elif output[i] == '<' and output[i+1] == '>':
                    # Remove the offenders
                    new_output = output[:i] + output[i+2:]
                    hit = True
                    skip = True
            else:
                skip = False
        if not hit:
            return output
        output = new_output

def nav(pos, target=0):
    # Navigates from pos to target location
    # Positive is right of NEG1, negative is left, 0 is neg1
    # Returns BF navigation to the target
    if pos == target:
        return ''
    elif pos > target:
        output = ''
        for i in range((pos - target)):
            output += '<'
        return output
    elif pos < target:
        output = ''
        for i in range((target - pos)):
            output += '>'
        return output

def stringify(message, finish_value=-1, add_newline=True):
    # Modified version of stringer from toolkit.py
    # Get the input string
    if add_newline:
        message += '\n'
    # The BF output (reset to 0 at beginning)
    output = '[-]'
    # The last value that has been stored
    last = 0
    
    for char in message:
        # Get the ASCII numeral of each character as an offset from previous
        offset = ord(char)
        offset -= last
        last = ord(char)
        # Add the code
        if offset == 0:
            output += '.'
            continue # Issa same character
        elif offset > 0:
            output += '+' * offset
            output += '.'
        else: # Negative character
            output += '-' * abs(offset)
            output += '.'

    # Account for initial offset
    # FUTURE make cleaner? (remove '[-]')
    if finish_value > 0: # Starting value above 0
        output += '[-]' + ('+' * finish_value)
    elif finish_value < 0: # Starting value was negative
        output += '[-]' + ('-' * abs(finish_value))
    else: # Finish value is 0
        output += '[-]'
    
    return output

def copy(mem, target, overwrite=True, destructive=False, subtract=False):
    # Copies the value at memory location mem into target
    # Starts and ends at neg1
    # Overwrite: Kills previous value at target
    # Destructive: Kills value at mem
    # Subtract: Subtracts from the second memory value instead of add 
    output = ''
    if overwrite:
        output += nav(0, target) + '[-]' + nav(target) # Wipe value & return
        
    output += nav(0, mem) # Navigate from NEG1 to mem
    
    if not destructive:
        output += '[-' # Start of copy loop
        output += nav(mem, -1) + '+' # Go to buffer and add
        output += nav(-1, target) # Go to target and add/subtract
        if subtract:
            output += '-'
        else: # Add
            output += '+'
        output += nav(target, mem) # Go back to mem
        output += ']'
        output += nav(mem, -1) # Go to Buffer
        output += '[-' # Start of buffer loop
        output += nav(-1, mem) + '+' # Go to memory location and add
        output += nav(mem, -1) # Return to buffer
        output += ']'
        output += nav(-1, 0) # Goes back to NEG1
    else: # Is destructive
        output += '[-'  # Start of move loop
        output += nav(mem, target) + '+' + nav(target, mem) # Move value
        output += ']'
        output += nav(mem, 0) # Return to NEG1
    return output

def lda(mem, overwrite=True, destructive=False):
    # Copies the value at memory location mem into INPUT1
    # Starts and ends at neg1
    # Overwrite: Kills previous value at INPUT1
    # Destructive: Kills value at mem
    # >>[-<<<+<<<+>>>>>>]<<, for location 2
    return copy(mem, -4, overwrite, destructive) # Location for INPUT1

def ldb(mem, overwrite=True, destructive=False):
    # Copies the value at memory location mem into INPUT2
    # Starts and ends at neg1
    # Overwrite: Kills previous value at INPUT2
    # Destructive: Kills value at mem
    return copy(mem, -3, overwrite, destructive) # Location for INPUT2

def store(mem, overwrite=True, destructive=True):
    # Stores value in input buffer to mem location
    # Starts and ends at NEG1
    # Overwrite: Kills old value at mem
    # Destructive: Kills transferring value
    return copy(-2, mem, overwrite, destructive)

def bump(val, mem, destructive=False, subtract=False):
    # Bumps the value val at location mem
    # Destructive: Effectively creates the value
    # Subtract: Subtracts instead
    # Starts and ends at NEG1
    output = ''
    output += nav(0, mem)
    if destructive:
        output += '[-]'
    for i in range(val):
        if subtract:
            output += '-'
        else: # Add
            output += '+'
    output += nav(mem, 0)
    return output

def ascii_decimal(to_decimal=True):
    # Translates a number back and forth into decimal and ASCII int
    # Currently unused...
    output = ''
    if to_decimal:
        output += '-'*48
    else:
        output += '+'*48
    return output

def translate_line(line):
    # Translates a line into BF code
    # ALWAYS HOME TO NEG1MARK
    line = line.strip() # Cleaning
    pos = 0 # How far the position is removed from NEG1MARK at all times
    output = '' # Translated code
    operation = None # Last operation
    memory = [] # Significant locations of memory

    # Blank handling
    if line == '':
        return ''
    
    terms = line.split(' ')

    # More blank handling
    new_terms = []
    for term in terms:
        if term != '':
            new_terms.append(term)
    terms = new_terms
    
    # Find significant memory locations
    for term in terms:
        if term[0].lower() == 'm': # Term is memory location
            if term[1:].isdigit():
                memory.append((int(term[1:]) + 1)) # Stores just the ints in memory

    # Is it raw?
    if terms[0].lower() == 'raw':
        output += ' '.join(terms[1:])

    # Is it a print?
    if terms[0].lower() == 'pr':
        output += nav(pos, 0)
        pos = 0
        output += stringify(" ".join(terms[1:]))
    if terms[0].lower() == 'prw':
        output += nav(pos, 0)
        pos = 0
        output += stringify(" ".join(terms[1:]), add_newline=False)

    # Is it an input?
    if terms[0].lower() == 'in':
        # Home
        output += nav(pos, 0)
        pos = 0
        # Goto memory[1] and get
        output += nav(0, memory[0])
        output += ','
        output += nav(memory[0], 0)

    # Is it a loop? (is already homed, hopefully)
    if terms[0].lower() == 'loop':
        output += '['
    if terms[0].lower() == '!loop':
        output += ']'

    # Is it a for loop?
    if terms[0].lower() == 'for':
        # Split the string into condition and commands, separated by ':'s & clean
        group = ' '.join(terms[1:]).split(':')
        mem = int(group[0][1:]) + 1
        commands = []
        for command in group[1:]:
            commands.append(command.strip())

        # Nav home
        output += nav(pos, 0)
        pos = 0

        # Begin memory location destructive loop
        output += nav(0, mem)
        output += '[-'
        output += nav(mem, 0)
        # All conditional statements, recursively
        for command in commands:
            output += translate_line(command)
        output += nav(0, mem)
        output += ']'
        output += nav(mem, 0)
        

    # Is it an if statement?
    if terms[0].lower() == 'if':
        # Split the string into condition and commands, separated by ':'s & clean
        group = ' '.join(terms[1:]).split(':')
        condition = group[0]
        commands = []
        for command in group[1:]:
            strippedCommand = command.strip()
            if strippedCommand.split(' ')[0] == 'if': # If there is a nested if statement
                print("ERRROR: NESTED IF STATEMENTS NOT SUPPORTED. Ignoring conditional...")
            else:
                commands.append(strippedCommand) # Add the command to the list of commands to be executed


        # Nav home
        output += nav(pos, 0)
        pos = 0
        
        # Parse the condition
        parts = condition.split(' ') # One Comparison Two
        # Copy the memory location over
        output += lda(int(parts[0][1:]) + 1)
        # Is to int
        if parts[2].isdigit():
            # Create the value
            output += bump(int(parts[2]), -3, True)
        # Is to memory value
        else:
            output += copy((int(parts[2][1:]) + 1), -3)

        # Operations
        if parts[1] == '=': # Equality
            # Do comparison (result initially in input2)
            output += nav(0, -4)
            output += '>[-<->][-]+<[>-<[-]]' # If ONE == TWO, stores in TWO
            output += '>' # Goes to the result in TWO
            output += '[[-]' # Beginning of conditional
            output += nav(-3, 0) # Home
            # All conditional statements, recursively
            for command in commands:
                output += translate_line(command)
            output += nav(0, -3) # Return
            output += ']<' # End of conditional and return to ONE
            output += nav(-4, 0)
        elif parts[1] == '<=': # Less than or equal to
            # Do comparison
            output += nav(0, -4)
            output += '>>>[-]<<[->[-]<<-[>>[-]+>]+[->+]-<<-[<[-]>[+]+>]+[->+]-<<+<]>-<<[-]' # If ONE <= TWO
            output += '>>' # Goes to the result in TWO
            output += '[[-]' # Beginning of conditional
            output += nav(-2, 0) # Home
            # All conditional statements, recursively
            for command in commands:
                output += translate_line(command)
            output += nav(0, -2) # Return
            output += ']<<' # End of conditional and return to ONE
            output += nav(-4, 0)
        elif parts[1] == '<': # Less than
            # Do comparison
            output += nav(0, -4)
            output += '>>>[-]<<-[->[-]<<-[>>[-]+>]+[->+]-<<-[<[-]>[+]+>]+[->+]-<<+<]>-<<[-]' # If ONE <= TWO
            output += '>>' # Goes to the result in TWO
            output += '[[-]' # Beginning of conditional
            output += nav(-2, 0) # Home
            # All conditional statements, recursively
            for command in commands:
                output += translate_line(command)
            output += nav(0, -2) # Return
            output += ']<<' # End of conditional and return to ONE
            output += nav(-4, 0)
        elif parts[1] == '>=': # Greater than or equal to (NOT less than)
            # Do comparison
            output += nav(0, -4)
            output += '>>>[-]<<-[->[-]<<-[>>[-]+>]+[->+]-<<-[<[-]>[+]+>]+[->+]-<<+<]>-<<[-]' # If ONE <= TWO
            output += '>>' # Goes to the result in TWO
            output += '-[[-]' # Beginning of conditional
            output += nav(-2, 0) # Home
            # All conditional statements, recursively
            for command in commands:
                output += translate_line(command)
            output += nav(0, -2) # Return
            output += ']<<' # End of conditional and return to ONE
            output += nav(-4, 0)
        elif parts[1] == '>': # Greater than (NOT less than or equal to)
            # Do comparison
            output += nav(0, -4)
            output += '>>>[-]<<[->[-]<<-[>>[-]+>]+[->+]-<<-[<[-]>[+]+>]+[->+]-<<+<]>-<<[-]' # If ONE <= TWO
            output += '>>' # Goes to the result in TWO
            output += '-[[-]' # Beginning of conditional
            output += nav(-2, 0) # Home
            # All conditional statements, recursively
            for command in commands:
                output += translate_line(command)
            output += nav(0, -2) # Return
            output += ']<<' # End of conditional and return to ONE
            output += nav(-4, 0)
            
        return output

    # Is it something else?
    for term in terms:
        # Blank checking (doesn't work)
        if term == '':
            continue
        # Is it a comment?
        if term[0] == '#':
            return output # End the entire line
        # Check to see if the term is an operation
        if term.lower() in ['=', '-', '+', 'del', '*']:
            operation = term.lower()
        elif term.isdigit(): # If the term is an int
            if operation == '+': # Add
                # Nav to memory
                output += nav(pos, memory[0])
                pos = memory[0]
                # Add
                for i in range(int(term)):
                    output += '+'
                    operation = None
                # Return
                output += nav(pos)
                pos = 0
            elif operation == '-': # Subtract
                # Nav to memory
                output += nav(pos, memory[0])
                pos = memory[0]
                # Subtract
                for i in range(int(term)):
                    output += '-'
                    operation = None
                # Return
                output += nav(pos)
                pos = 0
            elif operation == '=':
                # Go to the first memory location
                output += nav(pos, memory[0])
                pos = memory[0]
                output += '[-]'
                for i in range(int(term)):
                    output += '+'
                # Return to neg1
                output += nav(pos, 0)
                pos = 0
            elif operation == '*':
                # Nav to NEG1
                output += nav(pos, 0)
                pos = 0
                # Copy memory into INPUT1
                output += lda(memory[0])
                # Create value at INPUT2
                output += bump(int(term), -3)
                # Navto ONPUT 1 and multiply
                output += nav(0, -4)
                output += '[>[->+>+<<]>>[-<<+>>]<<<-]>[-]<' # Multiply into output
                output += nav(-4, 0)
                output += store(memory[0])
        
        elif term[0].lower() == 'm': # Is a location
            if operation == None:
                pass # Or nav, if no operation...?
            elif operation == '=':
                # Set the first memory to the second
                try: # Two memory locations
                    # Nav to NEG1
                    output += nav(pos, 0)
                    pos = 0
                    # Copy second to first, overwriting
                    output += copy(memory[1], memory[0])
                except:
                    print("ERROR Incorrect usage of '=' in '{}'".format(line))
            elif operation == '+':
                # Add the second memory to the first
                try:
                    # Nav to NEG1
                    output += nav(pos, 0)
                    pos = 0
                    # Copy second to first, not overwriting
                    output += copy(memory[1], memory[0], False)
                except:
                    print("ERROR Incorrect usage of '+' in '{}'".format(line))
            elif operation == '-':
                # Subtract the second memory location from the first
                try:
                    # Nav to NEG1
                    output += nav(pos, 0)
                    pos = 0
                    # Sub copy second to first, not overwriting
                    output += copy(memory[1], memory[0], False, False, True)
                except:
                    print("ERROR Incorrect usage of '-' in '{}'".format(line))
            elif operation == 'del':
                # Delete the memory location
                try:
                    # Nav to memory
                    output += nav(pos, memory[0])
                    pos = memory[0]
                    # Delete
                    output += '[-]'
                    # Nav back
                    output += nav(pos, 0)
                    pos = 0
                except:
                    print("ERROR Incorrect usage of 'del' in '{}'".format(line))
            elif operation == '*':
                # Multiply
                try:
                    # Nav to neg1
                    output += nav(pos, 0)
                    pos = 0
                    # Copy first memory to INPUT1 and second to INPUT2
                    output += lda(memory[0])
                    output += ldb(memory[1])
                    # Navto ONPUT 1 and multiply
                    output += nav(0, -4)
                    output += '[>[->+>+<<]>>[-<<+>>]<<<-]>[-]<' # Multiply into output
                    output += nav(-4, 0)
                    output += store(memory[0])
                except:
                    print("ERROR Incorrect usage of '*' in '{}'".format(line))
    return output

def main():
    if '-h' in sys.argv: # Help menu
        print("Activation: ABF.py <optional_file> <args>")
        print("Arguments:")
        print("    -h: This help menu")
        exit()

    try:
        # Open a file that is passed in
        with open(sys.argv[1], 'r') as file:
            code = file.read()
    except:
        while True:
            filepath = input("Name of ABF code file: ")
            try:
                with open(filepath, 'r') as file:
                    code = file.read()
                    break
            except:
                print("File {} could not be found.".format(filepath))
    # Variable code now holds the entire instructions
    output = first()
    # Get lines
    lines = code.split('\n')
    total_lines = len(lines)
    completed_lines = 0
    # Compile lines and print output
    for line in lines:
        output += translate_line(line)
        completed_lines += 1
        print('\rCompiled line {} of {}'.format(completed_lines, total_lines), end='')
    # Clean output
    print('\nCleaning...')
    output = remove_extra_movement(output)
    # Store output in file
    with open('output.bf', 'w') as file:
        file.write(output)
    print('Saved output as "output.bf".')

if __name__ == '__main__':
    main()
