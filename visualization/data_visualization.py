## Visualize data
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def visualization(year, text):
    # Start with one review:
    # Create and generate a word cloud image:
    plt.suptitle(year, fontsize=24, fontweight='bold')
    wordcloud = WordCloud().generate_from_frequencies(text)
    print("\n***",year,"***\n")
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()