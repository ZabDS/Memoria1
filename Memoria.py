from random import shuffle
import time
import os

def CreateBoard(level):
    Board = []

    #4x4
    if level == '1':
        for i in range(0, 2):
            for j in range(0, 8):
                Board.append(j)
        print("Principiante")
    elif level == '2':
        #6x6
        for i in range(0, 2):
            for j in range(0, 18):
                Board.append(j)
        print("Avanzado")
    else:
        print("Error")
    #shuffle(Board)
    return  Board

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

def HiddenBoard(Coords,board,Hboard,level):
    x1 = int((Coords.split(";")[0]).split(",")[0])
    y1 = int((Coords.split(";")[0]).split(",")[1])
    x2 = int((Coords.split(";")[1]).split(",")[0])
    y2 = int((Coords.split(";")[1]).split(",")[1])
   
    indice1 = (y1*4+x1)
    indice2 = (y2*4+x2)

    if board[indice1] is board[indice2]:
        #print(board[indice1]," ",board[indice2])
        Hboard[indice1]=board[indice1]
        Hboard[indice2]=board[indice2]
        PrintBoard(level,Hboard)
    else:
        #print(board[indice1]," ",board[indice2])
        Hboard[indice1] = board[indice1]
        Hboard[indice2] = board[indice2]
        PrintBoard(level, Hboard)
        time.sleep(1)
        Hboard[indice1]='-'
        Hboard[indice2]='-'
        PrintBoard(level,Hboard)
    

def ValCoord(coord):
    aux1 = (coord.split(";")[0]).split(",")
    aux2 = (coord.split(";")[1]).split(",")

    if len(aux1) != 2 or len(aux2) != 2:
        return -1
    else:
        return 1

print("Bienvenido a Memoria")
level=input("Dificultad: ")

Board = CreateBoard(level)
HBoard = CreateHiddenBoard(level)
PrintBoard(level,Board)

coord=input("Ingrese las cordenadas de las cartas que desea ver en el formato x1,y1;x2,y2 ")
HiddenBoard(coord,Board,HBoard,level)
#print ((coord.split(";")[0]).split(","))
