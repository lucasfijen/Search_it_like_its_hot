from wordcloud import WordCloud
import create_wordcloud as creator
import os
# import matplotlib.pyplot as plt
import time

start = time.time()
# Read the whole text.
folder = os.listdir('json_files')
doc_list = folder[:10]
#os.system('mkdir' + ' clouds')
for doc in doc_list:
    text = creator.create_wordcloud(doc = doc[:-5],lang='english')

    # Generate a word cloud image
    cloud = WordCloud().generate(text)

    # Display the generated image:

    # plt.imshow(cloud, interpolation='bilinear')
    # plt.axis("off")
    #plt.show()

    # # lower max_font_size
    # cloud = WordCloud(max_font_size=40).generate(text)
    # store file
    cloud.to_file('clouds/' + doc[:-5] + ".png")
    #
    # plt.figure()
    # plt.imshow(cloud, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()
end = time.time()
print(end - start)
