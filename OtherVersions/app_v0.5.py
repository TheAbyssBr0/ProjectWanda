import os


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

target_file = open(os.path.join(__location__, "targets.txt"), 'r')

catch_continious = True

sw_targets = set()
mw_targets = dict()

for line in target_file:

	word = ""
	has_space = False
	first_space_location = 0

	for letter in line:

		if letter.isalpha():
			word += letter.lower()

		elif letter == ' ' and len(word) > 0:
			if not has_space:
				has_space = True
				first_space_location = len(word)
			word += ' '

		elif letter == ',' or '\n':
			if not has_space:
				sw_targets.add(word)
			else:
				key_string = word[:first_space_location]
				if key_string not in mw_targets:
					mw_targets[key_string] = [word[first_space_location:]]
				else:
					mw_targets[key_string].append(word[first_space_location:])
				first_space_location = 0
				has_space = False
			word = ""

target_file.close()


in_raw_file = open(os.path.join(__location__, "input.txt"), 'r')
in_file_string = ""

for line in in_raw_file:
	in_file_string += line

in_raw_file.close()


coordinates = []

word = ""
for i in range(len(in_file_string)):

	if in_file_string[i].isalpha():
		word += in_file_string[i].lower()
	
	else:		
		if (word in sw_targets) or (word[-3:] == "ing" and catch_continious):
			coordinates.append((i-len(word), len(word)))
		
		elif word in mw_targets:
			
			for target_word in mw_targets[word]:
				spotlight_word = in_file_string[i:i+len(target_word)]
				
				spotlight_word.replace('\n', ' ')
				'''
				for j in range(len(spotlight_word)):
					if not spotlight_word[j].isalpha():
						spotlight_word = spotlight_word[:j] + ' ' + spotlight_word[j+1:]
				'''				
				if target_word == spotlight_word:
					coordinates.append((i - len(word), len(word + target_word)))

		word = ""

print()
latest = 0
for i in range(len(coordinates)):
	print(in_file_string[latest:coordinates[i][0]], end='')
	print("\033[44;33m" + in_file_string[coordinates[i][0]:coordinates[i][0] + coordinates[i][1]] + "\033[m", end='')
	latest = coordinates[i][0] + coordinates[i][1]
print(in_file_string[latest:] + '\n')