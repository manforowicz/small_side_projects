from random import randrange

for i in range(64):
	answer = randrange(1,10)
	a = randrange(10,answer+10)
	b = a-answer
	
	a,b,answer = map(str,[a,b,answer])
	response = 0
	while response != answer:
		response = input(a + '-' + b + '=')
		if response != answer:
			print('Try again')
	print('----Correct!----\n')
