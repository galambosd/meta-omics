#!/usr/bin/env python

def MCR(defs,bin_set):
    if len(defs) == 1:
        if defs in bin_set:
            return 1
        else:
            return 0
    elif ' ' in defs:
        parts=defs.split(' ')
        total = 0
        for part in parts:
            total+=MCR(part,bin_set)
        return total/len(parts)
    elif ',' in defs:
        parts=defs.split(',')
        total=[]
        for part in parts:
            part.rstrip(')')
            part.lstrip('(')
            total.append(MCR(part,bin_set))
        return max(total)
    elif '+' in defs:
        parts=defs.split('+')
        print(parts)
        total = 0
        for part in parts:
            part.rstrip(')')
            part.lstrip('(')
            print(part)
            total+=MCR(part, bin_set)
        return total/len(parts)

bin_set=['1','4','5','9']
defs='1 (2+3,4+5+6,7) ((8+9-10),11)'

MCR(defs, bin_set)
