import search

# Convert input_text to prepare for request
def query_handler(input_text):
    htmltext = ""
    results = search.search_in_index(text=input_text)
    htmltext += print_histo_values(results)
    # Add here extra data that needs to be showed above

    for article in results['hits']['hits']:
        htmltext += create_div_from_dict(article)
    return htmltext


#convert_string_to_dict('cooking an egg EXCLUDE jan piet hein lul SIZE a0')
def convert_string_to_dict(input_text):
    # text="", categories=[], date=None, datetype=None, size=10
    results = {'TEXT':'', 'CATEGORY':[], 'EXCLUDE':[], 'TIME':[], 'SIZE':10}

    # make splitted query dict
    splitsquery = input_text.split()
    current_cat = 'TEXT'
    startvalue = 0
    for i in range(len(splitsquery)):
        if splitsquery[i] in results.keys():
            if current_cat in ('CATEGORY', 'EXCLUDE', 'TIME'):
                results[current_cat] = splitsquery[startvalue:i]
            else:
                results[current_cat] = " ".join(splitsquery[startvalue:i])

            current_cat=splitsquery[i]
            startvalue = i + 1

    if startvalue < len(splitsquery):
        if current_cat in ('CATEGORY', 'EXCLUDE', 'TIME'):
            results[current_cat] = splitsquery[startvalue:]
        else:
            results[current_cat] = " ".join(splitsquery[startvalue:])
    # CATEGORY (list of categories that should be searched)
    # and or not
    results['CATEGORY'] = handle_category(results['CATEGORY'])
    # EXCLUDE (list of all terms you want to exclude from search)
    # TIME  (split into starting date and value later, incl later, earlier)
    results['TIME'], results['DATETYPE'] = handle_time(results['TIME'])

    # AMOUNT (how many articles should be searched)
    try:
        results['SIZE'] = int(results['SIZE'])
    except:
        results['SIZE'] = 10

    print(results)

def handle_time(timeinput):
    datetype = ''
    time = ''
    if len(timeinput) == 1:
        time = timeinput[0]
    if len(timeinput) == 2:
        if timeinput[0] in ('from', 'since'):
            datetype = 'gte'
        if timeinput[0] in ('after'):
            datetype = 'gt'
        if timeinput[0] in ('before'):
            datetype = 'lt'
        if timeinput[0] in ('until'):
            datetype = 'lte'
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

    #all_categories = seach.get_all_categories()
    all_categories = ['hallo', 'paard']
    if len(new_selection) < 1:
        new_selection = all_categories
    return [x for x in new_selection if \
                            x not in excluded_cats and \
                            x in all_categories]

# creates a single div for a articledict
def create_div_from_dict(article):
    article_dict = article['_source']
    resultstring = "<div id='resultdiv'>"
    if 'title' in article_dict:
        if 'link' in article_dict:
            resultstring += '<a href="http://' + article_dict['link'] + \
                            '" target="_blank">' + article_dict['title'] + '</a>'
        else:
            resultstring += '<h1>' + article_dict['title'] + '</h1>'

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

def print_histo_values(res):
	title = "Timeline"
	data = res['aggregations']['hits_over_time']['buckets']

	titel = "dit moet een mooie titel worden"
	result = '''<div id='chartContainer'> </div>
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
