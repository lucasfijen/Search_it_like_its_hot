from bs4 import BeautifulSoup as bs
import re
import json
import os


def clean_text(s):
    s = re.sub("<[^>]*>", " ", s) # remove html tags
    s = s.replace("\n", " ") # remove newlines
    s = re.sub("\W\W+", " ", s) # remove multiple spaces
    return s

def parse_posts(all_rows, categorie, result, parent_dict):
    accepted_answer_doc = {}

    for row in all_rows:

        if row.get('posttypeid') == '1': # check if row is a post
            row_id = row.get('id')
            doc_id = categorie + row_id # create a doc_id
            try:
                result_dict[doc_id]['answers']
            except:
                result[doc_id] = {"answers":"", "comments":"", "answer_score":0}

            try: 
                accepted_answer_doc[categorie + row.get("acceptedanswerid")] = doc_id
            except: pass

            # get all information of the post
            result[doc_id]["categorie"] = categorie
            result[doc_id]["title"] = row.get('title')
            result[doc_id]["tags"] = row.get('tag')
            result[doc_id]["body"] = clean_text(row.get('body'))
            result[doc_id]["viewcount"] = row.get('viewcount')
            result[doc_id]["score"] = row.get('score')
            result[doc_id]["creation_date"] = row.get('creationdate')
            result[doc_id]["link"] = categorie + ".stackexchange.com/questions/" + row_id + "/" \
                                    + result[doc_id]["title"].replace(" ", "-")

        elif row.get('posttypeid') == '2':
            doc_id = categorie + row.get('parentid')
            row_id = categorie + row.get('id')
            parent_dict[row_id] = doc_id
            
            if row_id in accepted_answer_doc:
                try:
                    result[doc_id]["accepted_answer"] = clean_text(row.get('body'))
                    result[doc_id]["accepted_answer_score"] = int(row.get('score'))

                except:
                    result[doc_id] = {"answers":"", "comments":"", "answer_score":0}
                    result[doc_id]["accepted_answer"] = clean_text(row.get('body'))
                    result[doc_id]["accepted_answer_score"] = int(row.get('score'))

            else:
                try:
                    result[doc_id]["answers"] += clean_text(row.get('body'))  
                    result[doc_id]["answer_score"] += int(row.get('score'))

                except:
                    result[doc_id] = {"answers":"", "comments":"", "answer_score":0}
                    result[doc_id]["answers"] += clean_text(row.get('body'))  
                    result[doc_id]["answer_score"] += int(row.get('score'))

def parse_comments(all_rows, categorie, result, parent_dict):
    for row in all_rows:
        doc_id = categorie + row.get('postid')

        try:
            result[doc_id]["comments"] += clean_text(row.get('text'))

        except:
            try:
                doc_id = parent_dict[doc_id]
                result[doc_id]["comments"] += clean_text(row.get('text'))
                result[doc_id]["answer_score"] += int(row.get('score'))

            except:
                print(doc_id)
                print(row.get('id'))
            
def dict_to_json(file , result_dict):
    with open(file, 'w') as outfile:  
        json.dump(result_dict, outfile) # REMOVE INDENT LATER!!!!

def get_soup_from_xml(file):
    xml_file = open(file, 'r')
    soup = bs(xml_file, 'lxml')
    xml_file.close()
    return soup


def parse_file_to_dict(file, categorie, result_dict):
    os.system('7z e ' + 'dataset/' + file + ' Posts.xml Comments.xml -r')

    print("in function")
    parent_dict = {}
    
    print("variables made")
    # get all info from the posts in the categorie     
    soup = get_soup_from_xml("Posts.xml")

    print('soup made')
    parse_posts(soup.findAll("row"), categorie, result_dict, parent_dict)

    print("Posts done")
    # get all info from the comments in the categorie
    soup = get_soup_from_xml("Comments.xml")

    print('soup made')
    parse_comments(soup.findAll("row"), categorie, result_dict, parent_dict)

    print("parsed")

    os.system('rm Posts.xml Comments.xml')


def main():
    all_files = os.listdir('dataset')
    result_dict = {}

    for file in all_files:
        print(file[:-21])
        parse_file_to_dict(file, file[:-21], result_dict)

    # make a json from the dictionary
    dict_to_json('data.txt', result_dict)

main()

