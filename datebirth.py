from datetime import datetime as dt

cards = {1: "wizard", 
	 2: "highpriestess", 
	 3:"empress",
	 4:"emperor",
	 5:"hierophant",
	 6:"lovers",
	 7:"chariot",
	 8:"strength",
	 9:"hermit",
	10:"wheeloffortune",
	11:"justice",
	12:"hangedman",
	13:"death",
	14:"temperance",
	15:"devil",
	16:"tower",
	17:"stars",
	18:"moon",
	19:"sun",
	20:"judgement",
	21:"zawarudo",
	22:"fool"}

def choice(numofc):
	with open("srcfiles/"+cards[numofc]+'.txt', 'r+', encoding='utf-8-sig') as file:
		data = file.read()
		return data
	
def arkane(dmy):
	a = dmy[0]%22
	if a == 0:
		a = 22
	b = 0
	for i in range(len(dmy)):
		while dmy[i]>0:
			b+= dmy[i]%10
			dmy[i] = dmy[i]//10
	b = b%22
	if b == 0:
		b = 22 

	return (a, b)

def check_date(dmy):
	try:
		dmy = dmy.split(".")
	except AttributeError:
		return None
	if len(dmy) < 3 or len(dmy) >3:
		return None
	else:
		
		try:
			dt(int(dmy[2]), int(dmy[1]), int(dmy[0]))
			today = str(dt.today()).replace("-", " ").split(" ")			
		
			today = [int(today[i]) for i in range(len(today) - 1)]
		
			today = today[::-1]			

			dmy = [int(x) for x in dmy]

			if today[2] < dmy[2] or today[2] - dmy[2] >= 120:
				return "date1"
			elif today[2] == dmy[2]:
				if today[1]<dmy[1]:
					return "date1"
				elif today[1] == dmy[1]:
					if today[0] < dmy[0]:
						return "date1"

			return dmy

		except ValueError:
			return "date1"
							