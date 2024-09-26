# This is just a weird project for 2021 APCSP in Tesla STEM High School,
# made by OOP 3.

#RUN BY PASTING INTO AN ONLINE INTERPRETER SUCH AS:
#https://www.tutorialspoint.com/execute_python_online.php

W = input("Type in the full URL you want to convert to a password. Thanks. ")

#Remove everything except core website name
try:
	import re
	W = re.split('[./]', W)[-2]
except:
	print("Your URL wasn't valid. Please run the program again.")

#convert any numbers to corresponding letters
result = ""
for char in W:
	if char.isdigit():
		result += chr(ord(char)+49)
	else:
		result += char
W = result

#Turn all characters of W to lowercase
W = W.lower()

#Double W if it's only one character long
if len(W)==1:
	W = W+W

#Set N & A as W's length
N = len(W)
A = len(W)

#Shift each letter by backward in the alphabet by N
result = ""
for char in W:
	result += chr((ord(char) - N - 97) % 26 + 97)
W = result

#Capitalize first letter of W
W = W.capitalize()

#Add 10 to N if it's a one digit number
if len(str(N))==1:
	N += 10

#Flip N
N = str(N)[::-1]

#Convert digits of N to symbols on number keys
N = N.replace("1", "!")
N = N.replace("2", "@")
N = N.replace("3", "#")
N = N.replace("4", "$")
N = N.replace("5", "%")
N = N.replace("6", "^")
N = N.replace("7", "&")
N = N.replace("8", "*")
N = N.replace("9", "(")
N = N.replace("0", ")")

#Add 13 to A if it's a one digit number
if len(str(A))==1:
	A += 13

#Flip A
A = int( str(A)[::-1] )

#Multiply A by 2
A *= 2
A = str(A)

#Glue N, W, and A together
P = N+W+A

#Double password if it's too short
if len(P)<8:
	P = P+P

print("and the password is, drumroll please: \n")
print(P)
