#!/usr/bin/env python3

import socket
import time
import os
import random

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
buffer_size = 1024
PlayerPoints = 0
ComputerPoints = 0

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
    #os.system("clear")
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

def GenRandIndex(level):
    if level == '1':
        return random.randrange(17)
    else:
        return random.randrange(37)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    print("Bienvenido a Memoria")

    Client_conn, Client_addr = TCPServerSocket.accept()
    with Client_conn:
        print("Conectado a", Client_addr)
        data = Client_conn.recv(buffer_size)
        #print ("Recibido,", data,"   de ", Client_addr)
        level = data.decode()
        Board = CreateBoard(level)
        PrintBoard(level,Board)
        Client_conn.sendall(b" ")
        while True:
            #print("Esperando a recibir datos... ")
            data = Client_conn.recv(buffer_size)
            if not data:
                break
            Coords = data.decode()
            print(Coords)
            x1 = int((Coords.split(";")[0]).split(",")[0])
            y1 = int((Coords.split(";")[0]).split(",")[1])
            x2 = int((Coords.split(";")[1]).split(",")[0])
            y2 = int((Coords.split(";")[1]).split(",")[1])

            indice1 = (y1*4+x1)
            indice2 = (y2*4+x2)
            Cards = "x"
            if Board[indice1] != 'x':
                if Board[indice2] != 'x':
                    if int(Board[indice1]==Board[indice2]):
                        Cards = str(Board[indice1])+","+str(Board[indice2])
                        if(Board[indice1] != 'x'):
                            PlayerPoints += 1
                            Board[indice1] = "x"
                            Board[indice2] = "x"
                    else:
                        while True:
                            indiceA = GenRandIndex(level) 
                            indiceB = GenRandIndex(level)
                            if(indiceA != indiceB):
                                if Board[indiceA] != 'x':
                                    if Board[indiceB] != 'x':
                                        break
                        Cards = str(Board[indice1])+","+str(Board[indice2])+","+str(indiceA)+","+str(indiceB)+","+str(Board[indiceA])+","+str(Board[indiceB])

                        if int(Board[indiceA]) == int(Board[indiceB]):
                            ComputerPoints += 1
                            Board[indiceA] = 'x'
                            Board[indiceB] = 'x'

                        PrintBoard(level,Board)
            if indice1 == indice2:
                Client_conn.sendall(b"SAMECARD")
            else:
                Client_conn.sendall(Cards.encode())
                #print("Enviando respuesta a", Client_addr)
            

