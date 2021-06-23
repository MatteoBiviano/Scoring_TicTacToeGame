#Variabili globali
griglia = []
N = 5

#se il gioco continua
run_game = True   #il gioco continua finchè non avviene il game over, allora diventa false

#definizione turno

giocatore = "X"

scores = {"X":0, "O": 0}


def create_grid():
	global N
	global griglia
	N = int(input("Inserire il valore N di griglia: "))
	for i in range(N):
		griglia.append(["-" for i in range(N)])

def mostra_griglia():
	for i in range(N):
		for j in range(N-1):
			print(griglia[i][j] + " " + "|", end =" ")
		print(griglia[i][j+1])

#gestione dei turni dei giocatori
def choose_position():
	is_free()
	if run_game==True:
		valid = False
		while not valid:
			posizione_riga = int(input(f"Seleziona la coordinata di riga in [0, {N-1}]: "))
			while posizione_riga>=N:
				posizione_riga = int(input(f"Seleziona la coordinata di riga in [0, {N-1}]: "))
			posizione_colonna = int(input(f"Seleziona la coordinata di colonna in [0, {N-1}]: "))
			while posizione_colonna>=N:
				posizione_colonna = int(input(f"Seleziona la coordinata di colonna in [0, {N-1}]: "))

			#per evitare che un giocatore scegli una casella già selezionata in precedenza
			if griglia[posizione_riga][posizione_colonna] == "-":
				valid = True
			else:
				print("Posizione non valida. Scegli di nuovo ")

		griglia[posizione_riga][posizione_colonna] = giocatore
		return posizione_riga, posizione_colonna
	else:
		return -1, -1
def add_score(n):
	if n==3:
		scores[giocatore] = scores[giocatore] + 2
	if n==4:
		scores[giocatore] = scores[giocatore] + 10
	if n==5:
		scores[giocatore] = scores[giocatore] + 50

def update_scoores(riga, colonna):
	seq_righe = update_riga(riga, colonna, -1) + update_riga(riga, colonna+1, 1)
	add_score(seq_righe)
	seq_colonna = update_colonna(riga, colonna, -1) + update_colonna(riga+1, colonna, 1)
	add_score(seq_colonna)
	seq_diagonale_1 = update_diagonale_1(riga, colonna, -1) + update_diagonale_1(riga+1, colonna+1, 1)
	add_score(seq_diagonale_1)
	seq_diagonale_2 = update_diagonale_2(riga, colonna, -1, 1) + update_diagonale_2(riga+1, colonna-1, 1, -1)
	add_score(seq_diagonale_2)

def update_riga(riga, colonna, verso):
	if riga >-1 and riga < N:
		if colonna >-1 and colonna < N:
			if griglia[riga][colonna] == giocatore:
				return 1 + update_riga(riga, colonna+verso, verso)
	return 0

def update_colonna(riga, colonna, verso):
	if riga >-1 and riga < N:
		if colonna >-1 and colonna < N:
			if griglia[riga][colonna] == giocatore:
				return 1 + update_colonna(riga+verso, colonna, verso)
	return 0

def update_diagonale_1(riga, colonna, verso):
	if riga >-1 and riga < N:
		if colonna >-1 and colonna < N:	
			if griglia[riga][colonna] == giocatore:
				return 1 + update_diagonale_1(riga+verso, colonna+verso, verso)
	return 0

def update_diagonale_2(riga, colonna, verso1, verso2):
	if riga >-1 and riga < N:
		if colonna >-1 and colonna < N:
			if griglia[riga][colonna] == giocatore:
				return 1 + update_diagonale_2(riga+verso1, colonna+verso2, verso1, verso2)
	return 0

def check_win():
	global run_game
	score_= scores[giocatore]
	if score_ >= 50:
		print(f"Ha vinto il giocatore {giocatore} con {score_} punti")
		run_game = False

def cambia_turno():
	#imposto la variabile globale definita all'inizio
	global giocatore

	#se il giocatore è X, passa a O
	if giocatore == "X":
		giocatore = "O"

	#se il giocatore è O, passa a X
	elif giocatore == "O":
		giocatore = "X"

#Controllare se c'è una casella libera
def is_free():
	global run_game
	is_free = False
	for i in range(N):
		for j in range(N):
			if griglia[i][j]=="-":
				is_free = True
	if not is_free:
		run_game = False
		print("Nessuna cella libera, il gioco è finito in pareggio")

def main():
	create_grid()
	#mostro la griglia costruita all'inizio
	mostra_griglia()

	while run_game:
		print("È il turno di " + giocatore)
		riga, colonna = choose_position()
		if riga==colonna==-1:
			mostra_griglia()
		else:
			mostra_griglia()
			#Aggiornamento punteggio
			print(f"Scelta la posizione [{riga}, {colonna}]")
			update_scoores(riga, colonna)
			print(scores)
			check_win()
			cambia_turno()

main()