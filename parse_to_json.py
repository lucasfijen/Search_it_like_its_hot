from bs4 import BeautifulSoup as bs
from multiprocessing import Process
import re
import json
import os
import sys
import time

########## cleanup ##########

def clean_text(s):
    if type(s) is not str:
        return ""
    s = re.sub("<[^>]*>", " ", s) # remove html tags
    s = s.replace("\n", " ") # remove newlines
    s = re.sub("\W\W+", " ", s) # remove multiple spaces
    return s

def clean_tags(s):
    if type(s) is not str:
        return ""
    s = re.sub("<|>"," ", s) # strip xml tags
    s = re.sub("\s\s+"," ", s) # change multiple spaces to single space
    return s.strip()

########## file management ##########

def dict_to_json(result_dict):
    file = result_dict['id']
    with open('json_files/' + file + '.json', 'w') as outfile:  
        json.dump(result_dict, outfile) # REMOVE INDENT LATER!!!!

def make_dicts_from_Posts(text_file):
    answer_dict = {}
    question_answer_dict = {}
    answer_question_dict = {}

    for line in text_file: # loop through file
        soup = bs(line, 'lxml')
        try:
            soup = soup.findAll('row')[0]
        except: continue

        if soup['posttypeid'] == '2': # check if the line is answer
            answer_dict[soup.get('id')] = line # add the answer to the dict
            answer_question_dict[soup.get('id')] = soup.get('parentid')

            try:
                x = question_answer_dict[soup.get('parentid')]
                x.append(soup.get('id'))
                
            except:
                question_answer_dict[soup.get('parentid')] = [soup.get('id')]

    return answer_dict, question_answer_dict, answer_question_dict

########## Parser ###########

def parse_answers(text_file, categorie, answer_dict, question_answer_dict):

    for line in text_file:
        try:
            soup = bs(line, 'lxml')
            soup = soup.findAll('row')[0]
        except:
            continue

        row_id = soup.get('id')
        if soup.get('posttypeid') != '1': # skip if not a question
            continue

        # get question info 
        result = {"answers":"", "comments":"", "answer_score":0, "comment_score":0}
        result['id'] = categorie + row_id
        result["categorie"] = categorie
        result["title"] = soup.get('title')
        result["tags"] = clean_tags(soup.get('tag'))
        result["body"] = clean_text(soup.get('body'))
        result["viewcount"] = int(soup.get('viewcount'))
        result["score"] = int(soup.get('score'))
        result["creation_date"] = soup.get('creationdate')
        result["link"] = categorie + ".stackexchange.com/questions/" + row_id + "/" \
                                        + result["title"].replace(" ", "-")

        # check if there are any answers to the question
        try:
            answers = question_answer_dict[row_id]

        # parse to json if no answers are present
        except:
            dict_to_json(result)
            continue

        # get the accepted answer 
        try:
            accepted_answer = soup.get('acceptedanswerid')
            answers.remove(accepted_answer)

            aa_soup = bs(answer_dict[accepted_answer], 'lxml')
            del answer_dict[accepted_answer]
            aa_soup = aa_soup.findAll('row')[0]
            result['accepted_answer'] = clean_text(aa_soup.get('body'))
            result['accepted_answer_score'] = int(aa_soup.get('score'))

        except: pass

        # get the other answers
        for answer in answers:
            a_soup = bs(answer_dict[answer], 'lxml')
            del answer_dict[answer]
            a_soup = a_soup.findAll('row')[0]
            result['answers'] += clean_text(a_soup.get('body'))
            result['answer_score'] += int(a_soup.get('score'))

        dict_to_json(result) # make a json file from the dict

def parse_comments(text_file, categorie, answer_question_dict):

    for line in text_file:
        soup = bs(line, 'lxml')
        try:
            soup = soup.findAll('row')[0]
        except: continue

        post_id = soup.get('postid')
        if post_id in answer_question_dict.keys():
            post_id = answer_question_dict[post_id]

        file = categorie + post_id

        try:
            with open('json_files/'+file+'.json', 'r') as data_file:
                data = json.load(data_file)
        except:
            continue
        data['comment_score'] += int(soup.get('score'))
        data['comments'] += soup.get('text')

        dict_to_json(data)


########## MAIN ##########

def main(file):
    categorie = file[:-21]
    print(categorie)
    os.system('mkdir' + categorie)
    os.system('7z e ' + 'dataset/' + file + ' Posts.xml Comments.xml -r -o' + categorie)

    print("Post dict")
    text_file = open(categorie+'/Posts.xml', 'r')
    answer_dict, question_answer_dict, answer_question_dict = make_dicts_from_Posts(text_file)
    text_file.close()

    print("Posts and Answers")
    text_file = open(categorie+'/Posts.xml', 'r')
    parse_answers(text_file, categorie, answer_dict, question_answer_dict)
    del answer_dict
    text_file.close()

    print("Comments")
    text_file = open(categorie+'/Comments.xml', 'r')
    parse_comments(text_file, categorie, answer_question_dict)
    text_file.close()

    os.system('rm -rf ' + categorie)

folder = os.listdir('dataset')

for file in folder:
    p = Process(target = main, args = [file,])

    p.start()
p.join()