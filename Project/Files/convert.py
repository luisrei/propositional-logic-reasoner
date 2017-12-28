# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 15:29:56 2017

@authors: Luís Rei,   nº 78486
          João Girão, nº 78761
"""

import fileinput
    
      
def insertSolution(s, KB):
    "Inserts the clauses into Knowledge base"
    for c in getClause(s, []):
        if type(c) == list:
            c = sorted(c, key=lambda k: getKey(k))
            if red_check(c) == 1:
                continue
        else:
            if type(c) == tuple:
                c = [c]
        if not (c in KB):
            KB.append(c)
    return KB
            
def red_check(clause):
    "Checks for redundancy in clauses"
    index = 0
    if len(clause) == 1:
        return 0
    for l in clause: 
        # For each literal check if there is also
        # its negation in the clause     
        index = index + 1
        if type(l) == tuple:
            for c in clause[index:len(clause)]:
                if type(c) == tuple: 
                    continue
                elif l[1] == c:
                    return 1
        else:
            for c in clause[index:len(clause)]:
                if type(c) == str: 
                    continue
                elif l == c[1]:
                    return 1
    return 0

def getKey(c):
    "Gets key for sorting"
    if type(c) == str:
        return c[0]
    return c[1]

def outputSolution(KB):
    "Prints Knowledge Base"
    for clause in KB:
        if type(clause) == str:
            print("'" + clause.strip("\n") + "'")
        else:
            print(clause)
    
def getClause(s, c):
    "Separates sentences in CNF into clauses"
    if (type(s) == str) or (s[0] == 'not'):
        # Literal, add to clause list
        if type(s) == str:
            # Remove ''
            if s[0] == "'" or s[0] == '"':
                s = s[1:len(s)]
            if s[len(s)-1] == "'" or s[len(s)-1] == '"':
                s = s[0:len(s)-1]
            c.append(s)
        else:
            c.append([s])
        return c
    else:
        # Check for conjunctions
        if s[0] == 'and':
            getClause(s[1], c)
            getClause(s[2], c)
            return c
        elif s[0] == 'or':
            clause = checkRed(elimDis(s, []))
            if len(clause) > 0:
                c.append(clause)
            return c
    return c
    
def checkRed(clause):
    "Checks and eliminates redundancies"
    for c in clause:
        # Checks for sentences that are always true 
        # E.g.{('or', 'a', ('not', 'a')}
        if c[0] == 'not':
            if c[1] in clause:
                return []
        else:
            if ('not', c) in clause:
                return []
        return clause
        
def elimDis(s, simple = []):
    "Eliminates disjunctions for simplification"
    if s[1][0] == 'or':
        elimDis(s[1], simple)
    else:
        if s[1] not in simple:
            simple.append(s[1])
    if s[2][0] == 'or':
        elimDis(s[2], simple)
    else:
        if s[2] not in simple:
            simple.append(s[2])
    return simple

def convert(s):
    "Convert sentence to CNF"
    s1 = runTree(s)
    s2 = applyDist(s1)
    return s2

def runTree(s):
    """ Runs tree and eliminates equivalences, implications and negations
     from the leafs, right to left"""
    if type(s) == str:
        # It's a literal
        return s
    elif type(s) == tuple:
        if s[0] == '<=>':
            # Not literal
            if s[1] == s[2]:
                # Both sides are equal, eliminate redundancy
                return s[1]
            # Not redundant, clear equivalence
            return runTree(clearEquiv(s[1], s[2]))
        elif s[0] == '=>':
            # Not literal
            if s[1] == s[2]:
                # Both sides are equal, eliminate redundancy
                return s[1]
            # Not redundant, clear implication
            return runTree(clearImp(s[1], s[2]))
        elif s[0] == 'not':
            # May not be a literal
            if s[1][0] == 'not':
                # Double negation, eliminate it
                return runTree(s[1][1])
            else:
                # Propagate negation
                return clearNeg(runTree(s[1]))
        else:
            # Not literal - 'and' or 'or' - run tree on both sides
            if s[1] == s[2]:
                # Both sides are equal, eliminate redundancy
                return s[1]
            return (s[0], runTree(s[1]), runTree(s[2]))
        
def clearEquiv(s1, s2):
    "Eliminate equivalences"
    return ('and', clearImp(s1, s2), clearImp(s2, s1))

def clearImp(s1, s2):
    "Eliminate implications"
    return ('or',('not', s1), s2)
    
def clearNeg(s):
    "Propagate 'not' inwards usig De Morgan's laws"
    if type(s) == tuple:
        if s[0] == 'and':
            # not(A ^ B) = (not(A) v not(B))
            return ('or', clearNeg(s[1]), clearNeg(s[2]))
        elif s[0] == 'or':
            # not(A v B) = (not(A) ^ not(B))
            return ('and', clearNeg(s[1]), clearNeg(s[2]))
        else: 
            # Double negation, eliminate it
            return s[1]
    else:
        # Found literal
        return ('not', s)
    
def applyDist(s):
    "Apply distributive property to the sentence"
    if (type(s) != str) and (s[0] != 'not'):
        s = (s[0], applyDist(s[1]), applyDist(s[2]))
        if s[0] == 'or':
            if s[1][0] == 'and':
                # Use De Morgan's law to correct
                return ('and', applyDist(('or', s[1][1], s[2])), applyDist(('or', s[1][2], s[2])))
            elif s[2][0] == 'and':
                # Use De Morgan's law to correct
                return ('and', applyDist(('or', s[1], s[2][1])), applyDist(('or', s[1], s[2][2])))
            # Already in correct form (Disjunction of conjunctions)
            return s
        else:
            # Do not care about it
            return s
    return s

def evalLine(line, KB):
    "Evaluates sentences/clauses"
    # Error handling
    try:
        eval(line)
    except SyntaxError:
        return KB
    except NameError:
        return KB
    except TypeError:
        return KB
    line = line.strip()
    if type(eval(line)) is list:
        # Check if in simplified CNF
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
        lin = sorted(lin, key=lambda k: getKey(k))
        if (len(lin) > 0) and (lin not in KB):
            KB.append(lin)
    elif type(eval(line)) is tuple:
        KB = insertSolution(convert(eval(line)), KB)
    elif type(eval(line)) is str:
        KB = insertSolution(convert(line), KB)
    return KB

# MAIN
if __name__ == "__main__":
    "Converts propositional sentences into CNF"
    # Parameter initialization
    KB = []
    
    with fileinput.input() as f:
        for line in f:
            if len(line) > 0:
                if line == '\n':
                    break
                KB = evalLine(line, KB)
    outputSolution(KB)
  
    
    