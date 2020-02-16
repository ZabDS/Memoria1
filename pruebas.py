transitions = {
    ('q0', True): 'q1', 
    ('q0', '*'): 'q8', 
    ('q1', True): 'q1',
    ('q1', ','): 'q2',
    ('q2', True): 'q3',
    ('q3', True): 'q3',
    ('q3', ';'): 'q4',
    ('q4', True): 'q5',
    ('q5', True): 'q5',
    ('q5', ','): 'q6',
    ('q6', True): 'q7',
    ('q7', True): 'q7',
    }

def validarCad(cadena):
    estado='q0'
    for i in range(0,len(cadena)):
        if cadena[i].isdigit():
            estado=transitions[(estado,True)]
        else:
            estado=transitions[(estado,cadena[i])]

    if (estado == 'q8' or estado == 'q7'):
        return  True
    else:
        return False


Values = "0,3"
valor1 = Values.split(',')[0]
valor2 = Values.split(',')[1]

print(valor1)
print(valor2)