import sys

argv = sys.argv

with open(argv[1], 'r') as f:
    content = f.read()
    csplit = content.split("\n")
    
    

#def tokenize():
#scanner

numOfLines = len(csplit)

for s in range(len(csplit)):
    newc = csplit[s].rstrip()
    if(newc != '' and newc[-1] != ':'):
        newc += ';'
        csplit[s] = newc

print(csplit)
def partTyping(part):
    #IF AND WHILE
    if(len(part) == 0):
        raise Exception("INVALID INPUT")
    
    if(part == "while"):
        return ("KEYWORD",part)
    
    if(part == "if"):
        return ("KEYWORD",part)

    if(part == "print"):
        return ("KEYWORD",part)
    
    if(part == "and"):
        return ("AND", part)

    if(part == "or"):
        return ("OR", part)

    #Check String
    if(part[0] == '"'):
        return ("STRING",part)

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

    
    raise Exception("INVALID INPUT")


def whitespaceCheck(l,whitespace):
    if(len(l) > 0):
        i = 0
        while(i < len(l)):
            if(l[i] != " "):
                return i 
            i += 1
    
    return whitespace


def tokenize(parselist):
    tokens = []
    part = ""

    whitespace = 0
    indentstack = []


    for l in parselist:

        emptycheck = 1
        if(len(l) == 0):
            emptycheck = 0
            tokens.append(('EMPTY',None))

        wsChecked = whitespaceCheck(l,whitespace)
    
        if(whitespace < wsChecked):
            indentstack.append(whitespace)

        elif(whitespace > wsChecked):
            emptycheck = 1
            while(indentstack[-1] != wsChecked):
                tokens.append(('SPACE',indentstack.pop(-1)))
                tokens.append(('END',None))
            tokens.append(('SPACE',indentstack.pop(-1)))
            tokens.append(('END',None))
                
        whitespace = wsChecked

        if(wsChecked > 0 and emptycheck):   
            tokens.append(('SPACE',wsChecked))
            
        notstring = True
        for i in l:

            if(notstring == False):
                part += i
                if(i == '"'):
                    notstring = True

            elif(i in '+-*/<>=!:'):
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
                if(part != ""):
                    tokens.append(partTyping(part))
                part = ""
                tokens.append(('SEMICOLON',i))
            elif(i in '(){}'):
                if(part != ""):
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
            elif(i == '"'):
                if(part != ""):
                    tokens.append(partTyping(part))
                    part = ""
                part += '"'
                notstring = False
            elif(i == ' '):
                if(part != ""):
                    tokens.append(partTyping(part))
                part = ""
                

    if(whitespace > 0):
        while(len(indentstack) > 0):
            tokens.append(('SPACE',indentstack.pop(-1)))
            tokens.append(('END',None))
    
    return tokens

print()
tokenslist = tokenize(csplit)
print(tokenslist)

#C Types int float char char[]

class Tokens:
    def __init__(self,tokenslist,linecount):
        self.tokenslist = tokenslist
        self.currentToken = tokenslist[0]
        self.assignTokens = {}
        self.linecount = linecount
    

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
    blockstr += ' '
    while(T.currentToken[0] == 'EQUAL' or T.currentToken[0] == 'GTHAN' 
          or T.currentToken[0] == 'LTHAN' or T.currentToken[0] == 'NOT'):
            if(accept(T,'EQUAL')):
                blockstr += '='
            elif(accept(T,'GTHAN')):
                blockstr += '>'
            elif(accept(T,'LTHAN')):
                blockstr += '<'
            elif(accept(T,'NOT')):
                blockstr += '!'
            
    blockstr += ' '
    return blockstr


def condition(T, blockstr):
    
    while(T.currentToken[0] != 'COLON' and T.currentToken[0] != 'CLOSEDPAR'):
        if(T.currentToken[0] == 'AND'):
            blockstr += " && "
            expect(T,'AND')
        if(T.currentToken[0] == 'OR'):
            blockstr += " || "
            expect(T,'OR')

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
            blockstr = str(T.assignTokens[var]).lower()+" "+blockstr
            
            blockstr = term(T,var,blockstr)
            blockstr = expression(T,var,blockstr)
            
        if(T.currentToken[0] == 'INT' or T.currentToken[0] == 'FLOAT'):
            T.assignTokens[var] = T.currentToken[0]
            blockstr = str(T.currentToken[0]).lower()+" "+blockstr
            
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
    spacecount = 0
    if(T.currentToken[0] == 'SPACE'):
        spacecount = T.currentToken[1]
        expect(T,'SPACE')

    #if a IDENTIFIER is seen first
    if(T.currentToken[0] == 'IDENTIFIER'):
        if(T.currentToken[1] not in T.assignTokens):
            T.assignTokens[T.currentToken[1]] = None

        

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
        blockstr = "\t"+blockstr
    
    #if a KEYWORD is seen first
    elif(T.currentToken[0] == 'KEYWORD'):
        if(T.currentToken[1] == 'while'):
            T.linecount += 1

            blockstr += "\t"
            expect(T,'KEYWORD')
            blockstr += "while"
            accept(T,'OPENPAR')
            blockstr += '('
            blockstr = condition(T,blockstr)
            accept(T,'CLOSEDPAR')
            expect(T,'COLON')
            blockstr += "{"
            blockstr += '\n'


        elif(T.currentToken[1] == 'if'):
            T.linecount += 1

            blockstr += '\t'
            expect(T,"KEYWORD")
            blockstr += "if"
            accept(T,"OPENPAR")
            blockstr += '('
            blockstr = condition(T,blockstr)
            accept(T,"CLOSEDPAR")
            expect(T,"COLON")
            blockstr += '{'
            blockstr += '\n'
        
        elif(T.currentToken[1] == 'print'):
            blockstr += "\t"
            expect(T,"KEYWORD")
            blockstr += "printf"
            expect(T,"OPENPAR")
            blockstr += '('

            blockstr += (T.currentToken[1][:-1]+chr(92)+'n'+'"')
            expect(T,"STRING")

            expect(T,"CLOSEDPAR")
            blockstr += ')'
            expect(T,"SEMICOLON")
            blockstr += ';'
            blockstr += '\n'
        
    if(T.currentToken[0] == 'END'):
        blockstr += '\t}\n'
        expect(T,'END')

    if(T.currentToken[0] == 'EMPTY'):
        blockstr += '\n'
        expect(T,'EMPTY')

    if(spacecount > 0):
        for sp in range(spacecount):
            blockstr = " "+blockstr
    
    return blockstr

  
tokens = Tokens(tokenslist,numOfLines)

newmessage = ""
linesnum = 0
while(linesnum < tokens.linecount):
    newmessage = newmessage+block(tokens)
    linesnum += 1
    


output = "#include <stdio.h>\n\nint main(int argc, char* argv[]){\n\n"+newmessage+"\n\treturn 0; \n}"
print(newmessage)

with open(argv[2], "w") as file:
    file.write(output)

print()
print(tokens.assignTokens)
#indentifier x, y, epic_value

#keywords if, while, return, print, def

#separator {}, (), ;

#operator x, <, =

#literal 2, true, 6.02, "STRING"

#comment //

#whilespace ""