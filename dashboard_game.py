import streamlit as st
import numpy as np
import streamlit.components.v1 as components



def is_winner(board, riga, colonna, actual_player):
	update_scoores(board, riga, colonna, actual_player)
	score_= st.session_state["scores"][actual_player]
	if score_ >= st.session_state["max_value"]:
		return actual_player


def add_score(n, giocatore):
	if n==3:
		st.session_state["scores"][giocatore] = st.session_state["scores"][giocatore] + 2
	if n==4:
		st.session_state["scores"][giocatore] = st.session_state["scores"][giocatore] + 10
	if n==5:
		st.session_state["scores"][giocatore] = st.session_state["scores"][giocatore] + 50

def update_scoores(board, riga, colonna, actual_player):
	seq_righe = update_riga(board, riga, colonna, -1, actual_player) + update_riga(board, riga, colonna+1, 1, actual_player)
	add_score(seq_righe, actual_player)
	seq_colonna = update_colonna(board, riga, colonna, -1, actual_player) + update_colonna(board, riga+1, colonna, 1, actual_player)
	add_score(seq_colonna, actual_player)
	seq_diagonale_1 = update_diagonale_1(board, riga, colonna, -1, actual_player) + update_diagonale_1(board, riga+1, colonna+1, 1, actual_player)
	add_score(seq_diagonale_1, actual_player)
	seq_diagonale_2 = update_diagonale_2(board, riga, colonna, -1, 1, actual_player) + update_diagonale_2(board, riga+1, colonna-1, 1, -1, actual_player)
	add_score(seq_diagonale_2, actual_player)

def update_riga(board, riga, colonna, verso, giocatore):
	if riga >-1 and riga < st.session_state["N"]:
		if colonna >-1 and colonna < st.session_state["N"]:
			if board[riga][colonna] == giocatore:
				return 1 + update_riga(board, riga, colonna+verso, verso, giocatore)
	return 0

def update_colonna(board, riga, colonna, verso, giocatore):
	if riga >-1 and riga < st.session_state["N"]:
		if colonna >-1 and colonna < st.session_state["N"]:
			if board[riga][colonna] == giocatore:
				return 1 + update_colonna(board, riga+verso, colonna, verso, giocatore)
	return 0

def update_diagonale_1(board, riga, colonna, verso, giocatore):
	if riga >-1 and riga < st.session_state["N"]:
		if colonna >-1 and colonna < st.session_state["N"]:	
			if board[riga][colonna] == giocatore:
				return 1 + update_diagonale_1(board, riga+verso, colonna+verso, verso, giocatore)
	return 0

def update_diagonale_2(board, riga, colonna, verso1, verso2, giocatore):
	if riga >-1 and riga < st.session_state["N"]:
		if colonna >-1 and colonna < st.session_state["N"]:
			if board[riga][colonna] == giocatore:
				return 1 + update_diagonale_2(board, riga+verso1, colonna+verso2, verso1, verso2, giocatore)
	return 0

def end_game(board):
	is_free = False
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == "_":
				is_free = True
	return is_free

def main():
	st.sidebar.title("Menu")
	game = st.sidebar.selectbox(
	    '',
	    ["Rules", "Play"], index = 0)
	if(game == "Play"):
		possible_values = [str(i) for i in range(5, 10)]		
		user_input = st.sidebar.selectbox("Select grid dimension", [""] + possible_values, index = 0)
		if user_input != "":
			
			max_score = st.sidebar.text_input("Insert max score threshold", value="")
			if max_score.isnumeric():

				if "board_"+user_input not in st.session_state:
					st.session_state["board_"+user_input] = np.full((int(user_input), int(user_input)), "_", dtype=str)
					st.session_state.next_player = "X"
					st.session_state.winner = None
					st.session_state.loser = None
					st.session_state["N"] = int(user_input)
					st.session_state["scores"] = {"X":0, "O": 0}
					st.session_state["max_value"] = int(max_score)

				html_temp = f"""
				<div style="background-color:#145796;padding:5px;border-radius:30px">
					<h1 style="color:white;text-align:center;"> Scoring <br/> X: {st.session_state["scores"]["X"]} &emsp; O: {st.session_state["scores"]["O"]} <br/> (win at: {st.session_state["max_value"]})</h1>
				</div>	
				"""
				components.html(html_temp, width = 400, height = 200)

				def on_click_callback(row, column):
					if not st.session_state.winner:
						if not st.session_state.loser:
							actual_player = st.session_state.next_player
							if st.session_state["board_"+user_input][row, column] == "_":
								st.session_state["board_"+user_input][row, column] = actual_player
								st.session_state.next_player = (
									"O" if st.session_state.next_player == "X" else "X"
								)

								winner = is_winner(st.session_state["board_"+user_input], row, column, actual_player)

								if winner != "_":
									st.session_state.winner = winner
								else:
									end = end_game(st.session_state["board_"+user_input])
									if not end:
										st.session_state.loser = True
							else:
								end = end_game(st.session_state["board_"+user_input])
								if not end:
									st.session_state.loser = True
								else:
									st.warning("Select another cell")

				for idx, row in enumerate(st.session_state["board_"+user_input]):
					cols = st.beta_columns([0.2 for i in range(int(user_input))] + [0.7])
					for jdx, field in enumerate(row):
						cols[jdx].button(
							field,
							key=f"{idx}-{jdx}",
							on_click=on_click_callback,
							args=(idx, jdx),
						)

				if st.session_state.winner:
					st.success(f"{st.session_state.winner} won the game, with " + str(st.session_state["scores"][st.session_state.winner]) + " points")

				if st.session_state.loser:
					st.error("None won the game")

				if st.sidebar.button("Clear State"):
					for i in st.session_state.keys():
						del st.session_state[i]
					st.sidebar.button("Rerun page")
					#st.caching.clear_cache()
if __name__ == '__main__':
	main()

