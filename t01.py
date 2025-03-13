#=======================
#Programming question: Create a function that adds the ord value of all letters, but not anything else.
#skill:
#Description

def toaddall (string):
    return()

print( 'N o : ' + str(toaddall('N o') ))
# This should result in 189.
print( 'erm what the sigma : ' + str(toaddall('erm what the sigma') ))
# This should result in 1610.
print( 'Massive : ' + str(toaddall('Massive') ))
# This should result in 728.
print( 'Massive! : ' + str(toaddall('Massive!') ))
# This should also result in 728.
print( '!()#&(!)A@921009 : ' + str(toaddall('!()#&(!)A@921009') ))
# This should result in 65.


#Possible solution:
    
def toaddall (string):
    totalvalue = 0
    c = 0
    while c < len(string):
        if ord(string[c]) == 32 or ord(string[c]) < 65 or ord(string[c]) > 122:
            c+= 1
        else:
            totalvalue = totalvalue + ord(string[c])
            c+= 1
    return(totalvalue)
    

print( 'N o : ' + str(toaddall('N o') ))
# This should result in 189.
print( 'erm what the sigma : ' + str(toaddall('erm what the sigma') ))
# This should result in 1610.
print( 'Massive : ' + str(toaddall('Massive') ))
# This should result in 728.
print( 'Massive! : ' + str(toaddall('Massive!') ))
# This should also result in 728.
print( '!()#&(!)A@921009 : ' + str(toaddall('!()#&(!)A@921009') ))
# This should result in 65.
#=======================

