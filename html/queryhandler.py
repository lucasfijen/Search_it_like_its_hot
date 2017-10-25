


# Convert input_text to prepare for request
def query_handler(input_text):
    testdiv = {'title': 'Hallo ik ben lucas wat wil je hebben?',
               'link': 'http://nu.nl',
               'content': input_text}
    htmltext = create_div_from_dict(testdiv)
    return htmltext


# creates a single div for a articledict
def create_div_from_dict(article_dict):
    resultstring = "<div id='resultdiv'>"
    if 'title' in article_dict:
        resultstring += '<h1>' + article_dict['title'] + '</h1>'

    if 'link' in article_dict:
        resultstring += '<p>' + article_dict['link'] + '</h1>'

    if 'content' in article_dict:
        # Something to only take the first x words
        resultstring += '<p>' + article_dict['content'] + '</p>'

    resultstring += '</div>'

    return resultstring
