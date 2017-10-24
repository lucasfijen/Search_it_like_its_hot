from bs4 import BeautifulSoup as bs
import re
import json
import os
import sys

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
    s = re.sub("<|>"," ", s)
    s = re.sub("\s\s+"," ", s)
    return s.strip()

########## linking rows ##########

def make_accepted_answer_dict(question_dict):
    question_answer = {}
    answer_question = {}

    for question in question_dict.keys():
        soup = bs(question_dict[question], 'lxml')
        try:
            soup = soup.findAll('row')[0] 
        except:
            print('ERROR', soup)
            continue

        try:
            question_answer[str(question)] = soup['acceptedanswerid']
            answer_question[soup['acceptedanswerid']] = str(question) 

        except:pass

    return question_answer, answer_question


def make_answer_dict(answer_dict, accepted_answer_dict):
    question_answer = {}
    answer_question = {}

    for line in answer_dict.keys():
        soup = bs(answer_dict[line], 'lxml')
        soup = soup.findAll('row')[0]
        if soup['id'] in accepted_answer_dict.keys():
            continue

        try:
            x = question_answer[soup['parentid']]
            x.append(soup['id'])
            question_answer[soup['parentid']] = x
        except:
            question_answer[soup['parentid']] = [soup['id']]

        answer_question[soup['id']] = soup['parentid']
    
    return question_answer, answer_question

def make_question_comment_dict(question_dict, comment_dict, answer_dict, accepted_answer_dict):
    result = {}

    for line in comment_dict.keys():
        try:
            soup = bs(comment_dict[line], 'lxml')
            soup = soup.findAll('row')[0]
        except: continue

        parent = soup['postid']

        if parent in answer_dict:
            parent = answer_dict[parent]

        elif parent in accepted_answer_dict:
            parent = accepted_answer_dict[parent]

        if parent in question_dict:
            try:
                x = result[parent]
                x.append(soup['id'])
                result[parent] = x
            except:  
                result[parent] = [soup['id']]
    
    return result

########## file management ##########

def dict_to_json(result_dict):
    file = result_dict['id']
    with open('json_files/' + file + '.json', 'w') as outfile:  
        json.dump(result_dict, outfile, indent=4) # REMOVE INDENT LATER!!!!

def make_dicts_from_file(file):
    question_dict = {}
    answer_dict = {}
    comment_dict = {}

    os.system('7z e ' + 'dataset/' + file + ' Posts.xml Comments.xml -r')

    text_file = open('Posts.xml', 'r')

    # for i,line in enumerate(text_file):
    #     print(i)
    #     soup = bs(line, 'lxml')
    #     try:
    #         soup = soup.findAll('row')[0]
    #     except: continue

    #     if soup['posttypeid'] == '1':
    #         #question_dict[soup.get('id')] = line
    #         pass
    #     elif soup['posttypeid'] == '2':
    #         answer_dict[soup.get('id')] = line

    text_file.close()

    text_file = open('Comments.xml', 'r')
    
    for i,line in enumerate(text_file):
        print(i)
        if i >= 2:
            soup = bs(line, 'lxml')
            try:
                soup = soup.findAll('row')[0]
            except: continue
            comment_dict[soup.get('id')] = line

    text_file.close()

    os.system('rm Posts.xml Comments.xml')

    return question_dict, answer_dict, comment_dict

########## parser ##########

def make_dicts(file):

    print('first')
    question_dict, answer_dict, comment_dict = make_dicts_from_file(file)

    print('done')

    print('second')
    question_accepted_answer_dict, accepted_answer_question_dict = make_accepted_answer_dict(question_dict)

    print('done')

    print('third')
    question_answer_dict, answer_question_dict = make_answer_dict(answer_dict, accepted_answer_question_dict)

    print('done')

    print('fourth')
    question_comment_dict = make_question_comment_dict(question_dict, comment_dict, answer_question_dict, accepted_answer_question_dict)

    print('return')
    return question_dict, answer_dict, comment_dict, question_accepted_answer_dict, accepted_answer_question_dict, question_answer_dict, answer_question_dict, question_comment_dict

########## Parser ###########

def parse_file(categorie, question_dict, answer_dict, comment_dict, question_accepted_answer_dict, accepted_answer_question_dict,
            question_answer_dict, answer_question_dict, question_comment_dict):

    for question in question_dict.keys():
        soup = bs(question_dict[question], 'lxml')
        soup = soup.findAll('row')[0]
        row_id = soup.get('id')

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
        
        if row_id in question_accepted_answer_dict:
            accepted_answer = question_accepted_answer_dict[row_id]
            soup = bs(answer_dict[accepted_answer], 'lxml')
            soup = soup.findAll('row')[0]
            result['accepted_answer'] = clean_text(soup.get('body'))
            result['accepted_answer_score'] = soup.get('score')

        if row_id in question_answer_dict:
            answers = question_answer_dict[row_id]
            for a in answers:
                soup = bs(answer_dict[a], 'lxml')
                soup = soup.findAll('row')[0]
                result['answers'] += clean_text(soup.get('body')) + " "
                result['answer_score'] += int(soup.get('score'))

        if row_id in question_comment_dict:
            questions = question_comment_dict[row_id]
            for question in questions:
                soup = bs(comment_dict[question], 'lxml')
                soup = soup.findAll('row')[0]
                result['comments'] += clean_text(soup.get('text')) + " "
                result['comment_score'] += int(soup.get('score'))

        # print(soup)
        # print(result)

        dict_to_json(result)

    question_dict = answer_dict = comment_dict = question_answer_dict = question_comment_dict = question_accepted_answer_dict = answer_dict = accepted_answer_dict = {}
    print(question_dict)

########## MAIN ##########

def main():

    for file in os.listdir('dataset'):
        categorie = file[:-21]
        print(categorie)
        question_dict, answer_dict, comment_dict, question_accepted_answer_dict, accepted_answer_question_dict, question_answer_dict, answer_question_dict, question_comment_dict = make_dicts(file)
        parse_file(categorie, question_dict, answer_dict, comment_dict, question_accepted_answer_dict, accepted_answer_question_dict,
            question_answer_dict, answer_question_dict, question_comment_dict)

    print('done')



main()