# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 14:22:52 2017

@authors: Luís Rei,   nº 78486
          João Girão, nº 78761
"""
import fileinput

def checkComp(clause, remC, safeC, index):
    """
    Verifies if there are complementary clauses with the input clause
    in the knowledge base, remove input from KB if not, for simplification
    """
    for c in clause:
        # Run through the clause
        end = 0
        if (c in safeC) or (c[0] == 'not' and c[1] in safeC):
                # Contains literal that doesn't have complementary, remove
            continue
        else:
            if c[0] == 'not':
                # Search for complementary clauses
                if c[1] in remC:
                    # Contains literal that doesn't have complementary, remove
                    KB.remove(clause)
                    return True
                for x in KB:
                    if c[1] in x:
                        # Found complementary
                        end = 1
                        safeC.append(c[1])
                        break
                if end == 0:
                    # No complementary clause, remove input from KB
                    remC.append(c[1])
                    for i in clause:
                        if i[0] == 'not':
                            i = i[1]
                        if i in safeC:
                            safeC.remove(i)
                    KB.remove(clause)
                    return True
            else:
                # Search for complementary clauses
                if c in remC:
                    # Contains literal that doesn't have complementary, remove
                    KB.remove(clause)
                    return True
                for x in KB:
                    if ('not', c) in x:
                        # Found complementary
                        end = 1
                        safeC.append(c)
                        break
                if end == 0:
                    # No complementary clause, remove input from KB
                    remC.append(c)
                    for i in clause:
                        if i[0] == 'not':
                            i = i[1]
                        if i in safeC:
                            safeC.remove(i)
                    KB.remove(clause)
                    return True
    return False
    
def remSuperSet(KB):
    "Removes sets from KB if there are subsets also in the KB"
    # Variable initialization
    index = 0
    for clause in KB:
        index = index + 1;
        # Run through clauses
        for x in KB[index:len(KB)]:
            # Run through Knowledge Base
            sub = 1
            for literal in clause:
                # Check if subset
                if literal not in x:
                    sub = 0
                    break
            if sub == 1:
                KB.remove(x)
                
def getKey(c):
    "Gets key for sorting alphabetically"
    if type(c) == str:
        return c[0]
    else:
        return c[1]
    
def getKey2(c):
    "Gets key for sorting by size and alphabetically"
    if type(c[0]) == str:
        return len(c), c[0], 1
    else:
        return len(c), c[0][1], 2
    
def getKey3(c):
    "Gets key for sorting by size and alphabetically"
    if len(c) > 0:
        if type(c[0]) == str:
            return len(c), c[0], 1
        else:
            return len(c), c[0][1], 2
    else: return 0, 'a'
    
def getEndCond(KB):
    "Returns the end condition of the resolution algorithm"
    l = len(KB) - 1
    n = 0
    while l > 0:
        n = n + l
        l = l - 1
    return n

def addClause(clauseSet, KB):
    "Adds clauses to the Knowledge Base"
    added = False
    for c in clauseSet:
        # Check if empty clause
        if len(c) == 0:
            return KB, added, 1
        # Check if clause in KB
        if c not in KB:
            KB.append(c)
            added = True
            
    KB = sorted(KB, key = lambda k: getKey2(k))
    return KB, added, -1
    
def resolution(clause1, clause2):
    "Resolution algorithm"
    clauseSet = []
    for x in clause1:
        for y in clause2:
            tempSet = []
            end = 0
            if x[0] == 'not':
                if x[1] == y:
                    for i in clause1:  
                        if i not in tempSet and i != x:
                            if type(i) == tuple:
                                if i[1] in tempSet:
                                    end = 1
                                    break
                            else:
                                if ('not', i) in tempSet:
                                    end = 1
                                    break
                            tempSet.append(i)
                        if end == 1:
                                break
                    for j in clause2:
                        if j not in tempSet and j != y:
                            if type(j) == tuple:
                                if j[1] in tempSet:
                                    end = 1
                                    break
                            else:
                                if ('not', j) in tempSet:
                                    end = 1
                                    break
                            tempSet.append(j)
                        if end == 1:
                                break
                    clauseSet.append(sorted(tempSet, key = lambda k: getKey(k)))
                    
            elif y[0] == 'not':
                if x == y[1]:
                    for i in clause1:  
                        if i not in tempSet and i != x:
                            if type(i) == tuple:
                                if i[1] in tempSet:
                                    end = 1
                                    break
                            else:
                                if ('not', i) in tempSet:
                                    end = 1
                                    break
                            tempSet.append(i)
                        if end == 1:
                                break
                    for j in clause2:
                        if j not in tempSet and j != y:
                            if type(j) == tuple:
                                if j[1] in tempSet:
                                    end = 1
                                    break
                            else:
                                if ('not', j) in tempSet:
                                    end = 1
                                    break
                            tempSet.append(j)
                        if end == 1:
                                break
                    clauseSet.append(sorted(tempSet, key = lambda k: getKey(k)))
    if len(clauseSet) > 0:
        clauseSet = sorted(clauseSet, key = lambda k: getKey3(k))
    return clauseSet
        

def checkPairs(KB, index, compPair):
    "Applies the resolution method to the pairs in KB"
    for x in KB:
        index = index + 1
        for y in KB[index:len(KB)]:
            if (x, y) not in compPair:
                KB, added, end = addClause(resolution(x, y), KB)
                if end == 1:
                    return KB, 1
                compPair.append((x, y))
                if added == True:
                    return KB, -1
    return KB, -1

def checkCNF(clause, KB):
    "Checks if clause is in simplified CNF"
    if len(clause) > 2:
        return KB
    elif clause not in KB:
        KB.append([clause])
    return KB    

if __name__ == "__main__":
    """
    Reconstructs the Knowledge Base from convert.py, simplifies it 
    and runs the resolution algorithm through it.
    """
    
    # Variable initialization
    KB = [] # Knowledge Base
    remC = [] # List of removed clauses (only literals)
    safeC = [] # List of variables with complementary literals (may change)
    compPair = [] # List of pairs of clauses that already went through resolution
    index = 0
    endCond = 0 # Number of pairs needed to return failure (changeable)
    end = -1
    i = 0

    # Reconstruct knowledge base
    with fileinput.input() as f:
        for line in f: 
            
            # End condition for input
            if line == '\n':
                    break
            # Error failsafe
            try:
                eval(line)
            except SyntaxError:
                continue
            except NameError: 
                continue
            except TypeError: 
                continue
            # Check if in simplified CNF
            if type(eval(line)) is list:
                # Literal
                if len(eval(line)) == 1:
                    if type(eval(line)[0]) is tuple:
                        KB = checkCNF(eval(line)[0], KB)
                    elif type(eval(line)[0]) is str:
                        if [eval(line)] not in KB:
                            KB.append([eval(line)[0]])
                # List of literals
                else:
                    lin = []
                    for l in eval(line):
                        if type(l) is tuple:
                            if len(l) > 2:
                                # not in simplified CNF
                                lin = []
                                break
                        # Remove repeated literals
                        if l not in lin:
                            lin.append(l)
                    if (len(lin) > 0) and (lin not in KB):
                        KB.append(sorted(lin, key=lambda k: getKey(k)))
            elif type(eval(line)) is tuple:
                KB = checkCNF((eval(line)), KB)
            elif type(eval(line)) is str:
                if [eval(line)] not in KB:
                    KB.append([eval(line)])   
                    

    KB = sorted(KB, key=lambda k: getKey2(k)) # Sort alphabetically
    
    remSuperSet(KB) # Remove supersets
    
    # Remove clauses without complementary clauses
    while index < len(KB):
        if checkComp(KB[index], remC, safeC, index + 1) == False:
            index = index + 1
    
    KB = sorted(KB, key = lambda k: getKey2(k)) # Sort by size and alphabetically
    
    endCond = getEndCond(KB)
    j = 0
    
    while len(compPair) < endCond:
        index = 0
        KB, end = checkPairs(KB, index, compPair)  
        endCond = getEndCond(KB)                     
        if end == 1:
            print("\nTrue")
            break
        
        j = j + 1
        if j == 200:
            break
    if end == -1:
        print("\nFalse")                