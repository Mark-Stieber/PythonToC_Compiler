import sys

argv = sys.argv

with open(argv[1], 'r') as f:
    content = f.read()
    csplit = content.split("\n")
    #print(content.split("\n"))
    
    

#def tokenize():
#scanner

#65 - 90 Z
#97 a - 122 z
#95
numOfLines = len(csplit)

for s in range(len(csplit)):
    
    if(':' in csplit[s]):
       pass
    elif(csplit[s].lstrip() != ''):
        csplit[s] += ';'

def partTyping(part):
    #IF AND WHILE
    if(len(part) == 0):
        raise Exception("INVALD INPUT")
    
    if(part == "while"):
        return ("KEYWORD",part)
    
    elif(part == "if"):
        return ("KEYWORD",part)
    
    #Identifier
    if((65 <= ord(part[0]) <= 90) or (97 <= ord(part[0]) <= 122)):
        for i in part:
            if(not((65 <= ord(i) <= 90) or (97 <= ord(i) <= 122) or ord(i) == 95
             or (48 <= ord(i) <= 57))):
                raise Exception("IDENTIFIER WRONG")
        return ("IDENTIFIER",part)
    
    #Check float
    if('.' in part):
        try:
            return ("FLOAT",float(part))
        except:
            raise Exception("FLOAT WRONG")
    else:
        try:
            return ("INT",int(part))
        except:
            Exception("INT WRONG")


def whitespaceCheck(l,whitespace):
    if(len(l) > 0):
        i = 0
        while(l[i] == " "):
            i += 1
    
        return i
    return whitespace

print(csplit)
def tokenize(parselist):
    tokens = []
    part = ""

    whitespace = 0

    for l in parselist:

        wsChecked = whitespaceCheck(l,whitespace)
        if(wsChecked < whitespace):
            whitespace = wsChecked
            tokens.append(('END',None))
        whitespace = wsChecked

        for i in l:

            if(i in '+-*/<>=!:'):
                if(part != ""):
                    tokens.append(partTyping(part))
                part = ""
                if(i == '+'):
                    tokens.append(('PLUS',i)) 
                if(i == '-'):
                    tokens.append(('MINUS',i)) 
                if(i == '*'):
                    tokens.append(('MULT',i)) 
                if(i == '/'):
                    tokens.append(('DIV',i))
                if(i == '<'):
                    tokens.append(('LTHAN',i))
                if(i == '>'):
                    tokens.append(('GTHAN',i))
                if(i == '='):
                    tokens.append(('EQUAL',i))
                if(i == '!'):
                    tokens.append(('NOT',i))
                if(i == ':'):
                    tokens.append(('COLON',i))
                
            #characters or '_' or numbers or decimal
            elif((65 <= ord(i) <= 90) or (97 <= ord(i) <= 122) or ord(i) == 95
                or (48 <= ord(i) <= 57) or i == '.'):
                part+= i
                
            #semicolon
            elif(i == ';'):
                tokens.append(partTyping(part))
                part = ""
                tokens.append(('SEMICOLON',i))
            elif(i in '(){}'):
                tokens.append(partTyping(part))
                part = ""
                if(i == '('):
                    tokens.append(('OPENPAR',i))
                if(i == ')'):
                    tokens.append(('CLOSEDPAR',i))
                if(i == '{'):
                    tokens.append(('OPENCURLBRAC',i))
                if(i == '}'):
                    tokens.append(('CLOSEDCURLBRAC',i))
            elif(i == ' '):
                if(part != ""):
                    tokens.append(partTyping(part))
                part = ""

    if(whitespace > 0):
        tokens.append(('END',None))

    return tokens

print()
tokenslist = tokenize(csplit)
print(tokenslist)

#C Types int float char char[]

class Tokens:
    def __init__(self,tokenslist):
        self.tokenslist = tokenslist
        self.currentToken = tokenslist[0]
        self.assignTokens = {}
    

def accept(T,tokenName):
    if(len(T.tokenslist) > 0):
        if(T.currentToken[0] == tokenName):
            T.tokenslist.pop(0)
            if(len(T.tokenslist) > 0):
                T.currentToken = tokenslist[0]
            return True
        return False
    raise Exception("END OF LIST")

def expect(T,tokenName):
    if(accept(T,tokenName)):
        
        return True
    
    raise Exception("Unexpected Token")

def term(T,var,blockstr):
    if(T.currentToken[0] == 'EQUAL'):
        blockstr += '='
        expect(T,'EQUAL')
    
    if(T.currentToken[0] == 'IDENTIFIER'):
        if(T.currentToken[1] in T.assignTokens):
            if(T.assignTokens[var] == T.assignTokens[T.currentToken[1]]):
                blockstr += str(T.currentToken[1])
                expect(T,T.currentToken[0])
            else:
                raise Exception("TYPING ERROR")
        else:
            raise Exception("VAR NOT DEFINED")
    else:
        if(T.assignTokens[var] == T.currentToken[0]):
                blockstr += str(T.currentToken[1])
                expect(T,T.currentToken[0])
        else:
            raise Exception("TYPING ERROR")

    return blockstr

def expression(T,var,blockstr):
    op = T.currentToken
    
    while(op[0] == 'PLUS' or op[0] == 'MINUS' or op[0] == 'MULT' or op[0] == 'DIV'):
        blockstr += str(op[1])
        if(accept(T,'PLUS')):
            blockstr = term(T,var,blockstr)
        elif(accept(T,'MINUS')):
            blockstr = term(T,var,blockstr)
        elif(accept(T,'MULT')):
            blockstr = term(T,var,blockstr)
        elif(accept(T,'DIV')):
            blockstr = term(T,var,blockstr)
        else:
            raise Exception("ERROR HOW?!?!")
        
        op = T.currentToken

    return blockstr

def operator(T, blockstr):
    while(T.currentToken[0] == 'EQUAL' or T.currentToken[0] == 'GTHAN' or T.currentToken[0] == 'LTHAN'):
            if(accept(T,'EQUAL')):
                blockstr += '='
            elif(accept(T,'GTHAN')):
                blockstr += '>'
            elif(accept(T,'LTHAN')):
                blockstr += '<'

    return blockstr


def condition(T, blockstr):
    if(T.currentToken[0] == 'IDENTIFIER'):
        var = T.currentToken[1]
        blockstr = term(T,var,blockstr)
        blockstr = operator(T,blockstr)
        blockstr = term(T,var,blockstr)


    else:
        var = T.currentToken[1]
        blockstr = term(T,var,blockstr)
        blockstr = operator(T,blockstr)
        blockstr = term(T,var,blockstr)

    blockstr += ')'

    return blockstr

def assignment(T,var,blockstr):
    
    if(T.assignTokens[var] == None):
        if(T.currentToken[0] == 'IDENTIFIER'):
            T.assignTokens[var] = T.assignTokens[T.currentToken[1]]
            blockstr = str(T.assignTokens[var]).lower()+" "+blockstr[:1]
            
            blockstr = term(T,var,blockstr)
            blockstr = expression(T,var,blockstr)
            
        if(T.currentToken[0] == 'INT' or T.currentToken[0] == 'FLOAT'):
            T.assignTokens[var] = T.currentToken[0]
            blockstr = '\t'+str(T.currentToken[0]).lower()+" "+blockstr[1:]
            
            blockstr = term(T,var,blockstr)
            blockstr = expression(T,var,blockstr)
            
    else:
        if(T.currentToken[0] == 'IDENTIFIER'): 
            print("BELLO")
            if(T.assignTokens[var] != T.assignTokens[T.currentToken[1]]):
                T.assignTokens[var] = T.assignTokens[T.currentToken[1]]
                blockstr = str(T.assignTokens[var]).lower()+" "+blockstr
             
            blockstr = term(T,var,blockstr)
            blockstr = expression(T,var,blockstr)
    
        else:
            if(T.assignTokens[var] != T.currentToken[0]):
                T.assignTokens[var] = T.currentToken[0]
                blockstr = str(T.assignTokens[var]).lower()+" "+blockstr
            
            blockstr = term(T,var,blockstr)
            blockstr = expression(T,var,blockstr)
     
    
    return blockstr

#Takes in a block of the code and parses through it using the Tokens Class
def block(T):
    if(len(T.tokenslist) == 0):
        return ""

    blockstr = ""
    #if a IDENTIFIER is seen first
    if(T.currentToken[0] == 'IDENTIFIER'):
        if(T.currentToken[1] not in T.assignTokens):
            T.assignTokens[T.currentToken[1]] = None

        blockstr += "\t"

        var = T.currentToken[1]
        blockstr += var + ' '
        expect(T,'IDENTIFIER')
        
        #if(accept(T,'PLUS')):
        #    blockstr += '+'
        #elif(accept(T,'MINUS')):
        #    blockstr += '-'
        #elif(accept(T,'MULT')):
        #    blockstr += '*'
        #elif(accept(T,'DIV')):
        #    blockstr += '/'
        
        blockstr += '= '
        accept(T,'EQUAL')
        print(T.assignTokens)
        blockstr = assignment(T,var,blockstr)
        blockstr += ';'
        accept(T,'SEMICOLON') #change to expect later
        blockstr += '\n'
    
    #if a KEYWORD is seen first
    if(T.currentToken[0] == 'KEYWORD'):
        if(T.currentToken[1] == 'while'):
            blockstr += "\t"
            expect(T,'KEYWORD')
            blockstr += "while "
            accept(T,'OPENPAR')
            blockstr += '('
            blockstr = condition(T,blockstr)
            accept(T,'CLOSEDPAR')
            expect(T,'COLON')
            blockstr += "{"
            blockstr += '\n'


        if(T.currentToken[1] == 'if'):
            blockstr += "\t"

            blockstr += '\n'
        
    if(T.currentToken[0] == 'END'):
        blockstr += '}'
        expect(T,'END')
    
    return blockstr

  
tokens = Tokens(tokenslist)

newmessage = ""
for i in range(numOfLines):
    newmessage = newmessage+block(tokens)
    

print()
print(tokens.tokenslist)
print()
print(tokens.assignTokens)
print()
print(newmessage)

output = "#include <stdio.h>\n\nint main(int argc, char* argv[]){\n\n"+newmessage+"\n\treturn 0; \n}"

with open(argv[2], "w") as file:
    file.write(output)

#indentifier x, y, epic_value

#keywords if, while, return, print, def

#separator {}, (), ;

#operator x, <, =

#literal 2, true, 6.02, "STRING"

#comment //

#whilespace ""