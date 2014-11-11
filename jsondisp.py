#!/usr/bin/python
b = ""
c = ""
do_break = 0
q_break = 0
breakit = 0
for a in data1 :
        if ( a == '{' or a == '[' ) :
                b = b + a + "\n"
                c = c + "    "
                b = b + c
                q_break = 0
        elif ( a == '"' ) :
                if q_break == 0 :
                        b = b + a
                else :
                        b = b + "\n" + c + a
                q_break = 1
        elif ( a == ':' ) :
                        b = b + a
                        q_break = 0
        elif ( a == '}' or a == ']' ) :
                do_break = 1
                c = c[:-4]
                b = b + '\n' + c + a
                q_break = 0
        elif ( a == ',' ) :
                if do_break == 1 :
                        b = b + a + '\n' + c
                        do_break = 0
        else :
                b = b + a
                q_break = 0
print b

