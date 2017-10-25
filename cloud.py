from wordcloud import WordCloud
import create_wordcloud as creator
from os import path

# Read the whole text.
text = creator.create_wordcloud()

# Generate a word cloud image
cloud = WordCloud().generate(text)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(cloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
cloud = WordCloud(max_font_size=40).generate(text)
# store file
cloud.to_file("first.png")

plt.figure()
plt.imshow(cloud, interpolation="bilinear")
plt.axis("off")
plt.show()
