import socket
import random
import re

#function to check if a player has won
def checkboard(in_board):
	#check for row of three in all 8 directions
	if(in_board[0] == in_board[1] == in_board[2]):
		return board[0]
	if(in_board[3] == in_board[4] == in_board[5]):
		return board[3]
	if(in_board[6] == in_board[7] == in_board[8]):
		return board[6]
	if(in_board[0] == in_board[3] == in_board[6]):
		return board[0]
	if(in_board[1] == in_board[4] == in_board[7]):
		return board[1]
	if(in_board[2] == in_board[5] == in_board[8]):
		return board[2]
	if(in_board[0] == in_board[4] == in_board[8]):
		return board[0]
	if(in_board[2] == in_board[4] == in_board[6]):
		return board[2]
	#return whitespace if no one has won yet
	return " "

board = [" "," "," "," "," "," "," "," "," "]
while True:
	#welcone text
	print("Welcome to 1337 x's and o's")
	#get input from user in relation to action they want to perform
	print("[1] Host a game")
	print("[2] Join a game on this pc")
	print("[3] join by IP")
	print("[4] quit")
	ans = raw_input(":>")
	#break if user wishes to quit
	if(ans == ""):
		print("goodbye")
		break
	#get name from user
	name = raw_input("What's your name?:")
	if ans == "1":
		#create connection
		#setup socket
		s = socket.socket()
		#set port
		port = 1337
		#bind connection to socket 's'
		s.bind(('',port))
		#listen for connections
		s.listen(5)
		while True:
			#setting up game and connection
			#accet connection
			c, addr = s.accept()
			#print connection status
			print('Got connection from',addr)
			#create message to send to client
			mes = "connection established with " + name 
			#encode and send message
			c.send(mes.encode())
			#inform user of state of current connection
			print("connection established with " + c.recv(1024).decode())
			print("ready to play, starting match")
			#send query as to clients readiness
			c.send(b"st")
			#check client is ready
			while True:
				#wait for return of 'st' to start round
				if(c.recv(23).decode() == "st"):
					break
			#get random player to start game
			cplayer = random.randint(0,1)
			#set game bool to false
			gameover = False
			#loop until game is killed
			while gameover == False:
				#if player is server
				if(cplayer == 0):
					print("It is your go, make a move")
					#tell client that the server is making a move
					c.send(b"wt")
					#get input from user
					while True:
						plc = raw_input("where would you like to place your piece?[1-9]")
						if(plc != ''):
							if(int(plc) > 0 and int(plc) < 10 and board[int(plc) - 1] == " "):
								board[int(plc) - 1] = "X"
								print("Piece placed")
								print("new board positions:")
								print("+-----+")
								print('|' + board[0] + '|' + board[1] + '|' + board[2] + '|')
								print('|' + board[3] + '|' + board[4] + '|' + board[5] + '|')
								print('|' + board[6] + '|' + board[7] + '|' + board[8] + '|')
								print("+-----+")
								#send move to client
								c.send(plc.encode())
								#confirmation
								c.recv(1)
								cplayer = 1
								break
							elif(int(plc) < 1 or int(plc) > 9):
								print("That position is out of bounds!")
							elif(board[int(plc)] != " "):
								print("That position is occupied!")
						else:
							print("that is not a number between 1 and 9")
				#check if game is over
				result = checkboard(board)
				if(result != " "):
					print("gameover")
					if(result == "X"):
						print("X has won")
					elif(result == "O"):
						print("O has won")
					#close connection
					c.close()
					gameover = True
					break
				#clients go
				if(cplayer == 1):
					print("it is your opponents go")
					#tell client to go
					c.send(b"go")
					#recieve move
					plc = c.recv(22).decode()
					board[int(plc) - 1] = "O"
					print("Piece placed")
					print("new board positions:")
					print("+-----+")
					print('|' + board[0] + '|' + board[1] + '|' + board[2] + '|')
					print('|' + board[3] + '|' + board[4] + '|' + board[5] + '|')
					print('|' + board[6] + '|' + board[7] + '|' + board[8] + '|')
					print("+-----+")
					cplayer = 0
					result = checkboard(board)
					if(result != " "):
						print("gameover")
						if(result == "X"):
							print("X has won")
						elif(result == "O"):
							print("O has won\n")
						#close connection
						c.close()
						break
			break
	if ans == "2":
		host = '127.0.0.1'
		j = socket.socket()         # Create a socket object
		port = 1337             # Reserve a port for your service.
	if ans == "3":
		j = socket.socket()         # Create a socket object
		host = raw_input("enter host address:") # Get local machine name
		port = 1337             # Reserve a port for your service.
	if ans == "2" or ans == "3":
		j.connect((host, port))
		#print initial message
		print(j.recv(1024).decode())
		j.send(name.encode())
		if j.recv(23).decode() == "st":
			j.send(b"st")
		while True:
			inp = j.recv(23).decode()
			if(inp == "wt"):
				plc = j.recv(22).decode()
				j.send('A')
				board[int(plc) - 1] = "X"
				print("Piece placed")
				print("new board positions:")
				print("+-----+")
				print('|' + board[0] + '|' + board[1] + '|' + board[2] + '|')
				print('|' + board[3] + '|' + board[4] + '|' + board[5] + '|')
				print('|' + board[6] + '|' + board[7] + '|' + board[8] + '|')
				print("+-----+")
				res = checkboard(board)
				if(res != " "):
					print("gameover")
					if(res == "X"):
						print("X has won")
					if(res == "O"):
						print("O has won")
					j.close()
					break
			if(inp == "go"):
				while True:
					plc = raw_input("Where would you like to place your piece?[1-9]")
					if(plc != ''):
						if(int(plc) > 0 and int(plc) < 10 and board[int(plc) - 1] == " "):
							board[int(plc) - 1] = "O"
							print("Piece placed")
							print("New board positions:")
							print("+-----+")
							print('|' + board[0] + '|' + board[1] + '|' + board[2] + '|')
							print('|' + board[3] + '|' + board[4] + '|' + board[5] + '|')
							print('|' + board[6] + '|' + board[7] + '|' + board[8] + '|')
							print("+-----+")
							j.send(plc.encode())
							break
						elif(int(plc) < 1 or int(plc) > 9):
							print("That position is out of bounds!")
						elif(board[int(plc)] != " "):
							print("That position is occupied!")
					else:
							print("that is not a number between 1 and 9")
					
				res = checkboard(board)
				if(res != " "):
					print("gameover")
					if(res == "X"):
						print("X has won")
					if(res == "O"):
						print("O has won")
					j.close()
					break
	elif(ans != "1" and ans != "2" and ans != "3" and ans !="4"):
		print("the choice you have entered is invalid please try again")
