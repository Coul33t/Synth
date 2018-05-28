# -*-coding:utf-8 -*
#!/usr/bin/env python2.7

import string
import random
from operator import itemgetter
import pdb

# LA FLEMME DE FAIRE UN TRUC PROPRE PUTAIN
punctuation_to_skip = string.punctuation
punctuation_to_skip = punctuation_to_skip[:12] + punctuation_to_skip[(13):]
punctuation_to_skip = punctuation_to_skip[:6] + punctuation_to_skip[(7):]

# Extracts all the words from the sentences.
def extract_words(data_file):
	with open(data_file,'r') as data:

		text = data.read()
		words = []

		for line in enumerate(text.split('\n')):
			splitted_line = line[1].split()
		
			if(len(splitted_line) > 0):
				for word in splitted_line:
					new_word = word.translate(string.maketrans('',''), punctuation_to_skip)	
					if(new_word not in words):
							words.append(new_word)
		
	return words

# RETURN FORMAT :
# [[probabilities for words][probabilities for the beggining of a sentence][probabilities for the end of a sentence]]
def extract_probability(data_file, words):
	frequency = [[0.0 for x in range(len(words))] for x in range(len(words))]
	begin_sentence = [0.0 for x in range(len(words))]
	end_sentence = [0.0 for x in range(len(words))]

	with open(data_file,'r') as data:
		text = data.read()
		
		for line in enumerate(text.split('\n')):
			splitted_line = line[1].split()
		
			if(len(splitted_line) > 0):
				splitted_line = map(lambda x: x.translate(string.maketrans('',''), punctuation_to_skip), splitted_line)
				for i,word in enumerate(splitted_line):
					#new_word = word.translate(string.maketrans('',''), ',.')
					#pdb.set_trace()

					
					
					# Why this ? Because if the sentence has only one word, it's the first and the last. But if it's the first (with a full sentence after),
					# we still have to get the next word.
					first_word = False
					if(i == 0):
						first_word = True

					# Case : last word of the sentence
					if(splitted_line.index(word)+1 == len(splitted_line)):
						if(first_word):
							begin_sentence[words.index(word)] += 1
						end_sentence[words.index(word)] += 1
					
					else:
						if(first_word):
							#pdb.set_trace()
							begin_sentence[words.index(word)] += 1
						#if(word == 'et'):
							#pdb.set_trace()
						frequency[words.index(word)][words.index(splitted_line[splitted_line.index(word)+1])] += 1



	# Turning frequencies into probabilities
	probability = []
	for i,frequency_line in enumerate(frequency):
		line_sum = sum(frequency_line)
		#if it's only an end word, it won't have any chance to appear anywhere, so the sum of its probabilities is 0.
		if(line_sum == 0):
			probability.append(frequency_line)
		else:
			probability.append(map(lambda x: x/line_sum, frequency_line))

	begin_sentence = map(lambda x: x/sum(begin_sentence), begin_sentence)
	end_sentence = map(lambda x: x/sum(end_sentence), end_sentence)

	return [probability,begin_sentence,end_sentence]



# Output the results to a txt file
def write_probabilities_to_file(words, probability):
	with open('results.txt', 'w') as output:
		for i, word in enumerate(words):
			output.write(word + ' ')
			output.write(str(probability[0][i]))
			output.write('\n')

		output.write('_BEGIN_SENTENCE_ ' + str(probability[1]) +'\n')
		output.write('_END_SENTENCE_ ' +str(probability[2]))


# Generate a sentence from a list of words and their probabilities
def generate_sentence(probability, words):

	sentence = ''
	sentence_end = False
	current_word = ''
	while(not sentence_end):
		# First word
		
		if not sentence:
			current_probability = probability[1]
		else:
			current_probability = probability[0][words.index(current_word)]
		#pdb.set_trace()
		intervals = [[x, e] for x, e in enumerate(current_probability) if e != 0]
		intervals = sorted(intervals, key=itemgetter(1))

		# Ugly :(
		for i, value in enumerate(intervals):
			if(i > 0):
				intervals[i][1] += intervals[i-1][1]


		rn = random.random()
		
		#if it's an ending word
		if(sum([d[1] for d in intervals]) == 0):
			sentence_end = True
		else:
			interval_value = next(x[0] for x in intervals if x[1] > rn)
		#if(current_word == 'qui'):
			#pdb.set_trace()


		#pdb.set_trace()
		if(not sentence_end):
			word_index = [i[0] for i in intervals if i[0] == interval_value]
			#pdb.set_trace()
			word = words[word_index[0]]

		current_word = word
		sentence = sentence + ' ' + word

		# End condition
		# If this word can be the last of a sentence
		#pdb.set_trace()
		if(not sentence_end):
			if(probability[2][words.index(current_word)] != 0):
				if (random.random() > probability[2][words.index(current_word)]):
					#pdb.set_trace()
					sentence_end = True

	return sentence


def write_sentences_to_file(name, str):
	with open(name, 'w') as output:
		for sentence in (str):
			#pdb.set_trace()
			sentence = ''.join(sentence).lower()
			sentence[0].capitalize()

			output.write(''.join(sentence) + '\n')


# [[probabilities for words][probabilities for the beggining of a sentence][probabilities for the end of a sentence]]
if __name__ == '__main__':
	txt_file = 'Shakespeare_input.txt'
	name = 'Shakespeare_output.txt'
	words = extract_words(txt_file)
	probability = extract_probability(txt_file, words)

	write_probabilities_to_file(words, probability)

	str_test = []
	for i in xrange(10):
		str_test.append(generate_sentence(probability, words))

	write_sentences_to_file(name, str_test)



'''
First sentence ever produced :

Malheureusement Malheureusement Malheureusement Malheureusement Malheureusement Malheureusement 
Malheureusement Malheureusement Malheureusement Malheureusement Malheureusement Malheureusement 
Prout Malheureusement Malheureusement Malheureusement  Prout Malheureusement Malheureusement 
Malheureusement Malheureusement Malheureusement Malheureusement Malheureusement Malheureusement 
Malheureusement Malheureusement Malheureusement  Prout Prout

Second one :

P
r
o
u
t

'''