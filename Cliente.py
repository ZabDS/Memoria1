#!/usr/bin/env python3

import socket
from random import shuffle
import time
import os
import sys

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
buffer_size = 1024

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

def CreateHiddenBoard(level):
    Board = []

    # 4x4
    if level == '1':
        for i in range(0, 2):
            for j in range(0, 8):
                Board.append('-')
        #print("Principiante")
    elif level == '2':
        # 6x6
        for i in range(0, 2):
            for j in range(0, 18):
                Board.append('-')
        #print("Avanzado")
    else:
        print("Error")

    return Board

def PrintBoard(level,board):
    os.system("clear")
    if level == '1':
        for i in range(1,17):
            print(board[i-1],end="")
            print("\t",end="")
            if i%4 == 0:
                print()
    elif level == '2':
        for i in range(1,37):
            print(board[i-1],end="")
            print("\t",end="")
            if i%6 == 0:
                print()
    else:
        print("Error al imprimir")

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

def SeeCard(Coord, Board, Values, level):
    print("Juega")
    x1 = int((Coords.split(";")[0]).split(",")[0])
    y1 = int((Coords.split(";")[0]).split(",")[1])
    x2 = int((Coords.split(";")[1]).split(",")[0])
    y2 = int((Coords.split(";")[1]).split(",")[1])
    
    valor1 = Values.split(',')[0]
    valor2 = Values.split(',')[1]
    
    indice1 = (y1*4+x1)
    indice2 = (y2*4+x2)

    print(indice1)
    print(indice2)

    Board[indice1]=valor1
    Board[indice1]=valor2
    
    PrintBoard(level,Board)
    time.sleep(1)
    #if(int(valor1) == int(valor2)):
    #    PrintBoard(level, Board)
    #else:
    #    PrintBoard(level, Board)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Bienvenido a Memoria")
    
    while True:
        level=input("Dificultad: ")
        if(level.isdigit() != True):
            print("Ingrese un nivel valido (1 o 2)1")
        elif(level != '1'):
            if(level == '2'):
                break
            else:
                print("Ingrese un nivel valido (1 o 2)2")
        else:
            break

    TCPClientSocket.sendall(level.encode())
    Board = CreateHiddenBoard(level)
    PrintBoard(level,Board)
    #print("Esperando una respuesta...")
    data = TCPClientSocket.recv(buffer_size)
    #print("Recibido,", repr(data), " de", TCPClientSocket.getpeername())
    while True:
        coord=input("Ingrese las cordenadas de las cartas que desea ver en el formato x1,y1;x2,y2 ")
        try:
            if(validarCad(coord)):
                print("Coordenada Valida")
                if coord != "*":
                    print("Coordenada")
                    TCPClientSocket.sendall(coord.encode())
                    data = TCPClientSocket.recv(buffer_size)
                    print("Recibido,", repr(data), " de", TCPClientSocket.getpeername())
                    time.sleep(1)
                    if (data.decode() == "SAMECARD"):
                        print("La carta seleccionada es la misma")
                    else:
                        x1 = int((coord.split(";")[0]).split(",")[0])
                        y1 = int((coord.split(";")[0]).split(",")[1])
                        x2 = int((coord.split(";")[1]).split(",")[0])
                        y2 = int((coord.split(";")[1]).split(",")[1])
                        
                        Values = data.decode()
                        
                        valor1 = Values.split(',')[0]
                        valor2 = Values.split(',')[1]

                        indice1 = (y1*4+x1)
                        indice2 = (y2*4+x2)
                        
                        Board[indice1]=valor1
                        Board[indice2]=valor2
                        if valor1 != 'x':
                            if valor2 != 'x':
                                if(int(valor1) == int(valor2)):
                                    PrintBoard(level,Board)
                                else:
                                    indice3 = int(Values.split(',')[2])
                                    indice4 = int(Values.split(',')[3])
                                    valor3 = Values.split(',')[4]
                                    valor4 = Values.split(',')[5]
                                    
                                    PrintBoard(level,Board)
                                    print("JUGADOR")
                                    time.sleep(2)
                                    Board[indice1]="-"
                                    Board[indice2]="-"
                                    PrintBoard(level,Board)
                                    
                                    Board[indice3]=valor3
                                    Board[indice4]=valor4

                                    if int(valor3) == int(valor4):
                                        PrintBoard(level,Board)
                                    else:
                                        PrintBoard(level,Board)
                                        print("COMPUTADORA")
                                        time.sleep(2)
                                        Board[indice3]="-"
                                        Board[indice4]="-"
                                        PrintBoard(level,Board)
                                #SeeCard(coord,Board,data.decode(),level)

                        
                else:
                    print("Se ha detectado una señal de desconexion")
                    break
                if data == '*':
                    break;
            else:
                print("Ingrese una coordenada valida")
        except:
            print("Ingrese una cadena valida")
