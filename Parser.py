'''
Created on Oct 22, 2018

@author: gosha
'''

symbols = {"blank" : [" "], "digit" : ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], "operation" : ['+', '-', '=', '/', '*', '(', ')', '^'], "decimal" : ['.']}

def parse(eq):
    split_eq = split(eq)

def strType(s):
    if(s in symbols["blank"]):
        return("blank")
#------------------------------------------------------------------------------ 
    if(s in symbols["decimal"]):
        return("decimal")
#------------------------------------------------------------------------------ 
    if(type(s) == int or type(s) == float):
        return("number")
    
    for c in s:
        if((c not in symbols["digit"]) and c not in symbols["decimal"]):
            break
    else:
        return("number")
#------------------------------------------------------------------------------ 
    if(s in symbols["operation"]):
        return("operation")
#------------------------------------------------------------------------------ 
    return("object")


def split(eq):
    out = list(eq)
    while True:
        number_started = False
        
        for i in range(len(out)):
            if(len(out) > 1):
                pass
            
            str_type = strType(out[i])
            
            if(str_type == "blank"):
                del(out[i])
                break
            
            if(str_type == "number" or str_type == "decimal"):
                if(number_started):
                    out[i - 1] += out.pop(i)
                    break
                else:
                    number_started = True
            else:
                number_started = False
        else:
            break
    
    for i in range(len(out)):
        if(strType(out[i]) == "number"):
            out[i] = float(out[i])
    
    return(out)

def fixSyntax(eq):
    while(True):
        for i in range(len(eq) - 1):
            if(strType(eq[i]) == "number" and strType(eq[i + 1]) == "object"):
                eq = eq[0 : i + 1] + ["*"] + eq[i + 1 : len(eq)]
                break
        else:
            break
        
    return(eq)
    