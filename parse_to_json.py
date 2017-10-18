from bs4 import BeautifulSoup as bs
import re
import json


def clean_text(s):
    s = re.sub("<[^>]*>", " ", s) # remove html tags
    s = s.replace("\n", " ") # remove newlines
    s = re.sub("\W\W+", " ", s) # remove multiple spaces
    return s

def parse_posts(all_rows, categorie, result, parent_dict):
    for row in all_rows:

        if row.get('posttypeid') == '1': # check if row is a post
            row_id = row.get('id')
            doc_id = categorie + row_id # create a doc_id
            result[doc_id] = {"answers":"", "comments":""}

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

            # get the parent doc and add it to the parent dictionary
            doc_id = categorie + row.get('parentid') 
            parent_dict[categorie + row.get('id')] = doc_id

            # add the answer to the answers of the post
            result[doc_id]["answers"] += clean_text(row.get('body'))  

def parse_comments(all_rows, categorie, result, parent_dict):
    for row in all_rows:
        doc_id = categorie + row.get('postid')
        try:
            result[doc_id]["comments"] += clean_text(row.get('text'))
        except:
            doc_id = parent_dict[doc_id]
            result[doc_id]["comments"] += clean_text(row.get('text'))

def dict_to_json(file , result_dict):
    with open(file, 'w') as outfile:  
        json.dump(result_dict, outfile, indent=4) # REMOVE INDENT LATER!!!!

def get_soup_from_xml(file):
    xml_file = open(file, 'r')
    soup = bs(xml_file, 'lxml')
    xml_file.close()
    return soup


def main(categorie):
    print("in function")
    result_dict = {}
    parent_dict = {}
    
    print("variables made")
    # get all info from the posts in the categorie     
    soup = get_soup_from_xml(categorie + "/Posts.xml")
    parse_posts(soup.findAll("row"), categorie, result_dict, parent_dict)

    print("Posts done")
    # get all info from the comments in the categorie
    soup = get_soup_from_xml(categorie + "/Comments.xml")
    parse_comments(soup.findAll("row"), categorie, result_dict, parent_dict)

    print("Comments done")
    # make a json from the dictionary
    dict_to_json('data.txt', result_dict)

    print("parsed")

main("dataset")
