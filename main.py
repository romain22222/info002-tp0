import math
import random
import sys

couples = []
sumInstances = 0

itos = {}
def intToString(i):
	res = ""
	for _ in range(4):
		res = chr(ord('A') + i % 25 + (i%25 > 8)) + res
		i //= 25
	return res

def loadProbs():
	global couples, sumInstances, itos
	for i in range(25 ** 4):
		itos[intToString(i)] = i
	with open("4-grams-francais-ALPHA.save", "r") as f:
		lines = f.readlines()
		sumInstances = 0
		couples = [0] * 25**4
		for line in lines:
			line = line.split(' ')
			line[0] = "".join([l if l != 'J' else 'I' for l in line[0]])
			couples[itos[line[0]]] += int(line[1])
			sumInstances += int(line[1])
		backup = math.log(0.01/sumInstances)
		for k, v in enumerate(couples):
			couples[k] = backup if v == 0 else math.log(v / sumInstances)

def fitness(c):
	sProb = 0
	for i in range(len(c) - 3):
		sProb += couples[itos[c[i:i+4]]]
	return sProb

def genereCle(initStr=""):
	initStr = trimTexte(initStr)
	key = []
	letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
	letters.remove('J')
	if initStr == "":
		random.shuffle(letters)
		return letters
	chars = list(initStr)
	while len(chars) > 0:
		while len(chars) > 0 and chars[0] not in letters:
			chars.pop(0)
		if len(chars) > 0:
			key.append(chars.pop(0))
			letters.remove(key[-1])
	key += letters
	return key

def afficheCle(key):
	for i in range(5):
		[print(key[5*i+j], end=" ") for j in range(5)]
		print()
	print("".join(key))

def coordLet(l, key):
	pos = key.index(l)
	return pos // 5, pos % 5

def chiffrePaire(letPaire, key):
	"""
	Chaque lettre de la paire est remplacée par l'autre coin sur la même ligne. Ainsi, QG est remplacé par WU plutôt que UW.

Si les deux lettres à remplacer sont sur la même ligne (TH par exemple), elles sont remplacées par les lettres juste à droite (QW dans le cas de TH).

Les lignes sont cycliques, et la paire LS sera remplacée par CE.

Si les deux lettres à remplacer sont sur la même colonne, elles sont remplacées par les lettres juste en dessous.

Comme les lignes, les colonnes sont cycliques. Par exemple, la paire KY sera remplacée par DT.
	"""
	(x1, y1), (x2, y2) = coordLet(letPaire[0], key), coordLet(letPaire[1], key)
	if x1 == x2:
		return key[5*x1+(y1+1)%5] + key[5*x2+(y2+1)%5]
	if y1 == y2:
		return key[5*((x1+1)%5)+y1] + key[5*((x2+1)%5)+y2]
	return key[5*x1+y2] + key[5*x2+y1]

def trimTexte(texte):
	"""
	Le texte est d'abord converti en majuscules, puis tous les caractères non alphabétiques sont supprimés. Les lettres J sont remplacées par des I.
	"""
	texte = texte.upper()
	texte = "".join([c for c in texte if c.isalpha()])
	texte = texte.replace('J', 'I')
	return texte

def chiffreTexte(texte, key):
	"""
	Pour chiffrer une lettre double TT par exemple, on insère un X au milieu pour chiffrer TXT.... (Pour cette raison, il est interdit d'avoir un XX dans le texte clair !)

Par contre, il n'est pas nécessaire d'insérer de X lors du chiffrement de COOL, qui donnera simplement LHLR.

Si le nombre de lettres ne tombe pas juste, on ajoute un X pour compléter la dernière paire. (Si cette dernière lettre est déjà un X, on ajoute n'importe quelle autre lettre.)
	"""
	texte = trimTexte(texte)
	res = ""
	i = 0
	while i < len(texte)//2:
		if texte[2*i] == texte[2*i+1]:
			if texte[2*i] == 'X':
				i += 1
				continue
			texte = texte[:2*i+1] + 'X' + texte[2*i+1:]
		res += chiffrePaire(texte[2*i:2*i+2], key)
		i += 1
	if len(texte) % 2 == 1:
		res += chiffrePaire((texte[-1] + 'X') if texte[-1] != 'X' else (texte[-1] + random.choice([c for c in key if c != 'X'])), key)
	return res

def prepareText(lines):
	return trimTexte("".join(lines))

def loadText(inputFile):
	with open(inputFile, "r") as f:
		return prepareText(f.readlines())

def saveText(text, outputFile):
	with open(outputFile, "w") as f:
		f.write(text)

def encipher(inputFile, outputFile, passphrase=""):
	text = loadText(inputFile)
	key = genereCle(passphrase)
	saveText(chiffreTexte(text, key), outputFile)

def dechiffreTexte(text, key):
	"""
	Pour déchiffrer, on "inverse" la clé en renversant les lignes et les colonnes (K[i][j] := K[4-i][4-j]) et on effectue l'opération inverse pour les points 4. et 5.
	"""
	res = ""
	for i in range(len(text)//2):
		res += chiffrePaire(text[2*i:2*i+2], key)
	# Check for pattern lXl where l is at an even position
	for i in range(len(res)//2-2, -1, -1):
		if res[2*i] == res[2*i+2] and res[2*i+1] == 'X':
			res = res[:2*i+1] + res[2*i+2:]
	if res[-1] == 'X':
		res = res[:-1]
	return res

def perturbe_cle(cle):
	"""
	La fonction perturbe_cle prend en argument une clé de chiffrement et renvoie une clé perturbée. La perturbation consiste à échanger deux lettres de la clé choisies au hasard.
	"""
	if random.random() < 0.9:
		i, j = 0, 0
		while i == j:
			i, j = random.randint(0, 24), random.randint(0, 24)
		cle[i], cle[j] = cle[j], cle[i]
	elif random.random() < 0.5:
		i, j = random.randint(0, 4), random.randint(0, 4)
		for k in range(5):
			cle[5*i+k], cle[5*j+k] = cle[5*j+k], cle[5*i+k]
	else:
		i, j = random.randint(0, 4), random.randint(0, 4)
		for k in range(5):
			cle[5*k+i], cle[5*k+j] = cle[5*k+j], cle[5*k+i]
	return cle

def craque(text, nbIter, startKey):
	tmp = []
	[tmp.extend(startKey[5*i:5*i+5:][::-1]) for i in range(4, -1, -1)]
	key = tmp
	bestFitness = fitness(dechiffreTexte(text, key))
	for _ in range(nbIter):
		tmpKey = perturbe_cle(key[:])
		tmpFitness = fitness(dechiffreTexte(text, tmpKey))
		if tmpFitness > bestFitness:
			key = tmpKey
			bestFitness = tmpFitness
	return key

def craque_recuit(text, initT, stepT, finalT, nbKeysBeforeChange, startKey):
	T = initT
	tmp = []
	[tmp.extend(startKey[5*i:5*i+5:][::-1]) for i in range(4, -1, -1)]
	key = tmp
	bestKey = key
	currentFitness = fitness(dechiffreTexte(text, key))
	bestFitness = currentFitness
	turns = 0
	prevTempFitness = currentFitness
	curs = 100
	while T > finalT:
		for _ in range(nbKeysBeforeChange):
			tmpKey = perturbe_cle(key[:])
			tmpFitness = fitness(dechiffreTexte(text, tmpKey))
			delta = tmpFitness - currentFitness
			if delta > 0 or random.random() < math.exp(delta/T):
				key = tmpKey
				currentFitness = tmpFitness
				if currentFitness > bestFitness:
					bestKey = key
					bestFitness = tmpFitness
		if bestFitness == prevTempFitness:
			turns += 1
		else:
			turns = 0
			prevTempFitness = bestFitness
		if turns == 10:
			break
		if ((T+finalT)/(initT+finalT)) * 100 < curs:
			print()
			print(bestFitness)
			print(dechiffreTexte(text, bestKey))
			curs -= 10

		T -= stepT
	return bestKey


def crack(tool, inputFile, outputFile, remainingArgs):
	text = loadText(inputFile)
	remainingArgs = remainingArgs + [""] * (5 - len(remainingArgs))
	if tool == "hill":
		nbIter = int(remainingArgs[0]) if remainingArgs[0] != "" else 100
		startKey = list(remainingArgs[1]) if remainingArgs[1] != "" else genereCle()
		key = craque(text, nbIter, startKey)
	elif tool == "recuit":
		nbKeysBeforeChange = int(remainingArgs[0]) if remainingArgs[0] != "" else 50000
		startKey = list(remainingArgs[1]) if remainingArgs[1] != "" else genereCle()
		initT = float(remainingArgs[2]) if remainingArgs[2] != "" else len(text)/8
		stepT = float(remainingArgs[3]) if remainingArgs[3] != "" else (1 if len(text) > 400 else .2)
		finalT = float(remainingArgs[4]) if remainingArgs[4] != "" else .01
		key = craque_recuit(text, initT, stepT, finalT, nbKeysBeforeChange, startKey)
	else:
		print("Unknown crack tool: {}".format(tool))
		return
	saveText(dechiffreTexte(text, key), outputFile)

def decipher(inputFile, outputFile, passphrase=""):
	lines = loadText(inputFile)
	key = genereCle(passphrase)
	text = lines[1]
	saveText([dechiffreTexte(text, key)], outputFile)


if __name__ == '__main__':
	loadProbs()
	if len(sys.argv) < 2:
		sys.argv = ["", "help"]
	unusedArgs = sys.argv[2:]
	cmd = sys.argv[1]
	if cmd == "help":
		print("""usage: ./edc <CMD> ...

	available commands:
		key [STRING]									generate a key from string, or a random key (if no string is given)
		fitness <input>								compute score of file content
		encipher <input> <output> <key>				encipher file with the given passphrase as key (empty = random key), and put the result in output file
		decipher <input> <output> <key>				decipher file with the given passphrase as key (empty = use file's key), and put the result in output file
		crack <hill/recuit> <input> <output> [args]	crack file with the given number of iterations, and put the result in output file
		help											display this help message
	args order for crack:
		hill: <nbIter> <startKey>
		recuit: <nbKeysBeforeChange> <startKey> <initT> <stepT> <finalT>
	if no args are given or if there are not enough args, default values will be used
		""")
	elif cmd == "key":
		afficheCle(genereCle(unusedArgs[0] if len(unusedArgs) > 0 else ""))
	elif cmd == "fitness":
		if len(unusedArgs) == 0:
			print("usage: ./edc fitness <input>")
		else:
			print(fitness(loadText(unusedArgs[0])))
	elif cmd == "encipher":
		if len(unusedArgs) == 0:
			print("usage: ./edc encipher <input> <output> <key>")
		else:
			encipher(*unusedArgs)
	elif cmd == "decipher":
		if len(unusedArgs) == 0:
			print("usage: ./edc decipher <input> <output> <key>")
		else:
			decipher(*unusedArgs)
	elif cmd == "crack":
		if len(unusedArgs) == 0:
			print("""
usage: ./edc crack <hill/recuit> <input> <output> [args]
	args order for crack:
		hill: <nbIter> <startKey>
		recuit: <nbKeysBeforeChange> <startKey> <initT> <stepT> <finalT>
	if no args are given or if there are not enough args for the given method, default values will be used
			""")
		else:
			crack(unusedArgs[0], unusedArgs[1], unusedArgs[2], unusedArgs[3:])
