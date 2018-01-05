import csv
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt


#read first column of csv file to string of words seperated
#by tab

filenames = ['quaran']
d = {}
for filename in filenames:
    
    file = open(filename + '_readable.dict', 'r')
    lines = file.readlines()
    file.close()
    
    
    index = 0
    for line in lines:
        if index != 0:
            print(line)
            row = line.split('\t')
            word = row[1]
            print(word)
            count = row[2]
            d[word] = float(count)
        index +=1
    
    # Generate a word cloud image
    wordcloud = WordCloud(width=1600, height=800,max_font_size=200,colormap='magma').generate_from_frequencies(d)
    
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    plt.savefig('./images/wordcloud/'+ filename )
    
    
