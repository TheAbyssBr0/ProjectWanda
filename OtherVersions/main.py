import string
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

target_file = open(os.path.join(__location__, "targets.txt"), 'r')
target_file_text = ""

for i in target_file:
	target_file_text += i

target_list = target_file_text.split(",")

in_raw_file = open(os.path.join(__location__, "input.txt"), 'r')
in_raw = ""

for i in in_raw_file:
	in_raw += i

input_string = " " + in_raw.lower() + " "

for c in string.punctuation:
	input_string = input_string.replace(c, " ")

input_string.replace("\n", " ")

def normalise_targets(some_list):
	for word_num in range(len(some_list)):
		word = some_list[word_num]
		if word[0] != ' ':
			if word[0] != '*':
				word = ' ' + word
			else:
				word = word[1:]
				
		if word[len(word) - 1] != ' ':
			word = word + ' '
		some_list[word_num] = word
	return some_list

def finder(in_string, target):
	return_list = list()
	index = 0
	start = 0
	while (index != -1):
		index = in_string.find(target, start, len(in_string))
		if index != -1:
			return_list.append((index, len(target)))
		start = index + 1
	
	return return_list

def make_highlightable_list(list_of_tuples):
	return_list = list()
	for the_tuple in list_of_tuples:
		for i in range(the_tuple[1]-2):
			return_list.append(the_tuple[0] + i)
	return return_list


normalised_targets = normalise_targets(target_list)

list_of_tuples = list()

for i in normalised_targets:
	list_of_tuples.extend(finder(input_string, i))

list_of_nums = make_highlightable_list(list_of_tuples)
list_of_nums.sort()


for i in range(len(input_string) - 2):
	if i in list_of_nums:
		print("\033[44;33m" + in_raw[i] + "\033[m", end="")
	else:
		print(in_raw[i], end="")

print()