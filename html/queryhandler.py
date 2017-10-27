import search
import create_wordcloud

# Convert input_text to prepare for request
def query_handler(input_text):
    htmltext = ""
    input_dict = convert_string_to_dict(input_text)
    results = perform_search_from_dict(input_dict)
    if results['hits']['total'] > 0:
        htmltext += print_histo_values(results)
    # Add here extra data that needs to be showed above

    for article in results['hits']['hits']:
        htmltext += '<div id="resultdiv">'

        if input_dict['SHOWCLOUD']:
            htmltext += create_div_from_dict(article, 'query_result')
            htmltext += create_wordcloud.main(article['_source'])
        else:
            htmltext += create_div_from_dict(article, 'result_without')
        htmltext += '</div>'
    return htmltext

def perform_search_from_dict(input_dict):
    results = search.search_in_index(text=input_dict['TEXT'],
                                     categories=input_dict['CATEGORY'],
                                     date=input_dict['DATE'],
                                     datetype=input_dict['DATETYPE'],
                                     size=input_dict['SIZE'],
                                     exclude=input_dict['EXCLUDE'])
    return results

#convert_string_to_dict('cooking an egg EXCLUDE jan piet hein lul SIZE a0')
def convert_string_to_dict(input_text):
    # text="", categories=[], date=None, datetype=None, size=10
    results = {'TEXT':'', 'CATEGORY':[], 'EXCLUDE':[],
               'DATE':[], 'SIZE':10, 'SHOWCLOUD': False}

    # make splitted query dict
    splitsquery = input_text.split()
    current_cat = 'TEXT'
    startvalue = 0
    for i in range(len(splitsquery)):
        if splitsquery[i] in results.keys():
            if current_cat in ('CATEGORY', 'EXCLUDE', 'DATE'):
                results[current_cat] = splitsquery[startvalue:i]
            elif current_cat == 'SHOWCLOUD':
                results[current_cat] = True
            else:
                results[current_cat] = " ".join(splitsquery[startvalue:i])

            current_cat=splitsquery[i]
            startvalue = i + 1

    if startvalue < len(splitsquery):
        if current_cat in ('CATEGORY', 'EXCLUDE', 'DATE'):
            results[current_cat] = splitsquery[startvalue:]
        elif current_cat == 'SHOWCLOUD':
            results[current_cat] = True
        else:
            results[current_cat] = " ".join(splitsquery[startvalue:])
    if current_cat == 'SHOWCLOUD':
        results[current_cat] = True
    # CATEGORY (list of categories that should be searched)
    # and or not
    results['CATEGORY'] = handle_category(results['CATEGORY'])
    # EXCLUDE (list of all terms you want to exclude from search)
    # TIME  (split into starting date and value later, incl later, earlier)
    results['DATE'], results['DATETYPE'] = handle_time(results['DATE'])

    # AMOUNT (how many articles should be searched)
    try:
        results['SIZE'] = int(results['SIZE'])
    except:
        results['SIZE'] = 10

    return results

def handle_time(timeinput):
    datetype = None
    time = None
    if len(timeinput) == 1:
        time = timeinput[0]
        datetype = 'in'
    if len(timeinput) == 2:
        if timeinput[0] in ('from', 'since'):
            datetype = 'gte'
        if timeinput[0] in ('after'):
            datetype = 'gt'
        if timeinput[0] in ('before'):
            datetype = 'lt'
        if timeinput[0] in ('until'):
            datetype = 'lte'
        if timeinput[0] in ('in'):
            datetype = 'in'
        time = timeinput[1]
    return (time, datetype)


# parses input list for NOT and AND and OR, returns a list with
# Actual categories, if only negating list added, then these will be
# excluded from result
def handle_category(selected_cats):
    excluded_cats = []
    new_selection = []
    negation = False
    for i in range(len(selected_cats)):
        if selected_cats[i] in ('NOT' 'not'):
            negation = True
        elif selected_cats[i] in ('AND', 'OR', 'and', 'or'):
            if negation:
                negation = False
        else:
            if negation:
                excluded_cats.append(selected_cats[i])
                negation = False
            else:
                new_selection.append(selected_cats[i])

    all_categories = search.get_all_categories()
    if len(new_selection) < 1:
        new_selection = all_categories
    return [x for x in new_selection if \
                            x not in excluded_cats and \
                            x in all_categories]

# creates a single div for a articledict
def create_div_from_dict(article, title):
    article_dict = article['_source']
    resultstring = "<div id='"+ title + "'>"
    if 'title' in article_dict:
        if 'link' in article_dict:
            resultstring += '<a href="http://' + article_dict['link'] + \
                            '" target="_blank">' + article_dict['title'] + '</a>'
        else:
            resultstring += '<h1>' + article_dict['title'] + '</h1>'

    resultstring += "<h2>"
    if 'categorie' in article_dict:
        resultstring += article_dict['categorie'].title()
    if 'creation_date' in article_dict:
        resultstring += ', '+ article_dict['creation_date'][:10]
    resultstring += "</h2>"

    if 'body' in article_dict:
        # Something to only take the first x words
        splittext = article_dict['body'].split(' ')
        text = " ".join(splittext[:100])
        resultstring += '<p>' + text
        if(len(splittext) > 100):
            resultstring += '...'
        resultstring += '</p>'

    resultstring += '</div>'

    return resultstring

# Prints the histo values
def print_histo_values(res):
	title = "Timeline"
	data = res['aggregations']['hits_over_time']['buckets']

	titel = "dit moet een mooie titel worden"
	result = '''<div id='resultdiv'><h1>Total results: '''\
    + str(res['hits']['total']) + ' Runtime:  '+ str(res['took']) +  '''ms</h1>
    <div id='chartContainer'></div></div>
    <script type="text/javascript">
	function make_graph() {
	var chart = new CanvasJS.Chart("chartContainer",
	{
		title:{
		text:\"'''
	result += title
	result += '''\"},
		data: [
			{
			color: 'blue',
			dataPoints: ['''
	for line in data:
		result += "{label:" + "\"" + line['key_as_string'][:-12] + "\", y:" + str(line['doc_count']) + '},'
	result += ''']
				}
			]
		});

		chart.render();
		}
		make_graph()
	 </script>'''

	return result
