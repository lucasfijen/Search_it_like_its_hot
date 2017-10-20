from bs4 import BeautifulSoup as bs
import re
import json
import os
import sys

# def make_question_answer_dict(text_file):
# 	result = {}

# 	counter = 0
# 	for line in text_file:
# 		if counter < 2:
# 			counter += 1
# 			continue
# 		soup = bs(line, 'lxml')
# 		try:
# 			soup = soup.findAll('row')[0] 
# 		except:
# 			print('ERROR', soup)
# 			continue

# 		if soup['posttypeid'] == '2':
# 			if soup['parentid'] in result:
# 				x = result[soup['parentid']]
# 				x.append(soup['id'])
# 				result[soup['parentid']] = x
# 			else:
# 				result[soup['parentid']] = [soup['id']]
	
# 	return result


def main(file):
	os.system('7z e ' + 'dataset/' + file + ' Posts.xml Comments.xml -r')

	text_dict = {}
	text_file = open('Posts.xml', 'r')
	
	for i,line in enumerate(text_file):
		text_dict[i] = line

	print(sys.getsizeof(text_file))
	print(sys.getsizeof(text_dict))

	print(text_dict[200])
	text_file.close()

	os.system('rm Posts.xml Comments.xml')

file = "3dprinting.stackexchange.com.7z"

main(file)
#except: os.system('rm Posts.xml Comments.xml')