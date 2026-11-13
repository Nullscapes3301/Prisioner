import sys
import os
import random

def get_points(a, b):
    p1 = bool(a)
    p2 = bool(b)
    if p1 and p2:
        return [3,3]
    elif p1 and not p2:
        return [0,5]
    elif not p1 and p2:
        return [5,0]
    elif not p1 and not p2:
        return [1,1]
    else:
        raise ValueError("Invalid player answers")

class Player:
    def __init__(self, name="Default", func=None):
        self.name = name
        self.func = func
        self.score = 0
    def __call__(self, last_move, hist):
        if self.func is None:
            t = input(f"{self.name} >>> ")
        else:
            t = str(self.func(last_move, hist))

        if t in ["0", 0, False]:
            return 0 # Traiciona
        return 1 # Colabora
    def __repr__(self):
        return str(self.name)


# Dos algoritmos clasicos: Tit-for-tat y Random

def rnd(last_move, hist):
    return str(random.randint(0,1))

def tft(last_move, hist):
    if last_move is None:
        return 1
    return last_move

algo1 = Player(name="Random", func=rnd)
algo2  = Player(name="Tit for that", func=tft)

w = 100 # numero de jugadas
ww = -1 # jugada actual
spec = "" # resumen
tung = [None, None] # respuestas actuales
h = [] # historial visual hecho para humanos
moves = [[None,None]] # historial de movimientos
table = [f"| Move | {algo1.name} | {algo2.name} |",
         f"|------|{'-'*(len(algo1.name)+2)}|{'-'*(len(algo2.name)+2)}|"] # tabla mas visual para analizar resultados

stable = True  # ¿Hay que mostrar la tabla?
shist  = False # ¿Hay que mostrar el historial?

shows = [False,False]
# Que respuesta de que algoritmo hay que mostrar
# shows[0] es si hay que mostrar el movimiento del primer algoritmo(algo1)
# shows[1] es lo mismo pero con el segundo algoritmo (algo2)

def gtrs(hist, index):
    ret = []
    for x in hist:
        ret.append(x[index])
    return ret

while True:
    ww += 1
    if w == ww:
        break
    temp = [algo1.score, algo2.score] # no me acuerdo

    h.append(f"[Move {ww+1}]")

    # obtener respuestas
    trs = gtrs(moves, 1)
    tung[0] = algo1(moves[-1][1], trs)
    if shows[0]: print(f"{algo1.name} >>> {tung[0]} ")
    h.append(f"    {algo1.name}: {tung[0]}")
    trs = gtrs(moves, 0)
    tung[1] = algo2(moves[-1][0], trs)
    if shows[1]: print(f"{algo2.name} >>> {tung[1]} ")
    h.append(f"    {algo2.name}: {tung[1]}")

    # obtener puntos y registrar el historial
    moves.append([tung[0],  tung[1]])
    r = get_points(tung[0], tung[1])

    # sumar puntos
    algo1.score += r[0]
    algo2.score  += r[1]

    h.append(f"    {algo1.name} score earn +{algo1.score-temp[0]} point | {algo1.name} score = {algo1.score}")
    h.append( f"    {algo2.name} score earn +{algo2.score-temp[1]} points | {algo2.name} score = {algo2.score}")

    if stable:
        table.append(
            f"| {ww+1}{" "*( 4-len(str(ww+1)) )} | {str(tung[0])+(" "*(len(algo1.name)-1))} | {str(tung[1])+(" "*(len(algo2.name)-1))} |"
        )
    else:
        table = ["Show visual results isn't enabled"]

    tung = [None, None]

if algo1.score > algo2.score:
    winner = algo1.name
elif algo2.score > algo1.score:
    winner = algo2.name
else:
    winner = "None"
spec = f"""\
[END OF GAME]
Results:
    {algo1.name}: {algo1.score}
    {algo2.name}: {algo2.score}
Moves: {ww}
Winner: {winner}

History:
{"\n".join(h) if shist else "Show history isn't enabled"}

Visual:
{"\n".join(table)}
"""
print(spec)
