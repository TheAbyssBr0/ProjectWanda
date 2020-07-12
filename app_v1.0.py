import os

# read the target files
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
target_file = open(os.path.join(__location__, "targets.txt"), 'r')
targets_string = target_file.read()
target_file.close()


def get_targets(in_string):
	"""
	Split the targets and arrange them into a set and a dictionary

	:param in_string: input string taken from targets text file
	:return: a tuple of a set of single word targets and a dictionary of multi word targets
	"""
	sw_set = set()
	mw_dict = dict()
	word = ""
	has_space = False
	first_space_location = 0

	for letter in in_string:

		if letter.isalpha():
			word += letter.lower()

		elif letter == ' ' and len(word) > 0:
			if not has_space:
				has_space = True
				first_space_location = len(word)
			word += ' '

		elif letter == ',' or letter == '\n':
			if not has_space:
				sw_set.add(word)
			else:
				key_string = word[:first_space_location]
				if key_string not in mw_dict:
					mw_dict[key_string] = [word[first_space_location:]]
				else:
					mw_dict[key_string].append(word[first_space_location:])
				first_space_location = 0
				has_space = False
			word = ""

	return sw_set, mw_dict


sw_targets, mw_targets = get_targets(targets_string)
catch_continuous = True                                # this is for catching continuous terms

# read the input file
in_raw_file = open(os.path.join(__location__, "input.txt"), 'r')
in_file_string = in_raw_file.read()
in_raw_file.close()


def calc_coordinates(in_string, sw_set, mw_dict):
	"""
	Finds the location of the target words in in_string

	:param mw_dict: a dictionary containing multiple word turgets
	:param sw_set: a set containing single word targets
	:param in_string: the input string
	:return: a list of (tuples of) coordinates
	"""
	coordinate_list = list()
	word = ""
	for i in range(len(in_string)):
		if in_string[i].isalpha():
			word += in_string[i].lower()
		else:
			if (word in sw_set) or (word[-3:] == "ing" and catch_continuous):
				coordinate_list.append((i-len(word), len(word)))
			elif word in mw_dict:
				for target_word in mw_dict[word]:
					spotlight_word = in_string[i:i+len(target_word)]
					spotlight_word.replace('\n', ' ')
					if target_word == spotlight_word:
						coordinate_list.append((i - len(word), len(word + target_word)))
			word = ""
	return coordinate_list


# prepare for coloring
coordinates = calc_coordinates(in_file_string, sw_targets, mw_targets)
latest = 0
out_string = ""
for i in range(len(coordinates)):
	out_string += in_file_string[latest:coordinates[i][0]]
	out_string += "\033[44;33m" + in_file_string[coordinates[i][0]:coordinates[i][0] + coordinates[i][1]] + "\033[m"
	latest = coordinates[i][0] + coordinates[i][1]
out_string += in_file_string[latest:]
print(out_string)                                      # single print function for output
