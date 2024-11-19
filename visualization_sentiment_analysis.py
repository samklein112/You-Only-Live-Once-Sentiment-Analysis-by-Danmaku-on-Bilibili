from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps
import pandas as pd
import jieba
import random

# Generate the word cloud
background_Image = np.array(Image.open("boxing_glove.png"))

def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    colors = ['#F2293A', '#734044', '#A69151', '#BF6D4E', '#023E73']  # Define your color palette
    return random.choice(colors)

wc = WordCloud(
    width=1200,
    height=1200,
    background_color='white',
    scale=5,
    mask=background_Image,
    font_path='./font_type/DongFangDaKai_Regular.ttf',
    color_func=custom_color_func
)

# Process CSV data and cleansing them
data = pd.read_csv('danmaku_data.csv')
data = data.dropna(subset=['text'])
data['text'] = data['text'].str.replace(r'[^\w\s]', '', regex=True)
data['text'] = data['text'].str.strip()
danmaku_str = ' '.join(data['text'])

stopwords_danmaku = {"的", "是", "了", "和", "就", "都", "而", "及其", "或者", "因为", "所以", "然而", "而且", "并且",
                     "同时", "如果", "那么", "此", "还有", "不", "在", "于", "你", "我", "他", "她", "它", "们", "这",
                     "那", "呢", "啊", "啊啊啊", "吧", "哦", "呀", "哇", "哇哇", "嘿", "嘿嘿", "哼", "哟", "呃", "哒",
                     "嘻", "嘻嘻", "哈哈", "哈哈哈", "哈哈哈哈", "怎么", "这个", "一个", "觉得", "不是", "就是", "电影",
                     "这是", "BGM", "是不是", "知道", "这样", "还是", "什么", "这种", "时候", "不要", "完全", "只能",
                     "呜呜", "的"}

words_list = jieba.lcut(danmaku_str)
filtered_words_list = [
    word for word in words_list if word not in stopwords_danmaku and len(word) > 1
]
filtered_words_str = ' '.join(filtered_words_list)
word_cloud = wc.generate(filtered_words_str)

# Save and display the word cloud
word_cloud.to_file("word_cloud.jpg")
plt.imshow(word_cloud, interpolation='bilinear')
plt.axis('off')
plt.show()
#-------------------------------------------------------------------------------------------

# Sentiment analysis
from snownlp import SnowNLP
import pandas as pd

# Function to analyze sentiment with error handling
def analyze_sentiment_safe(text):
    try:
        if text and isinstance(text, str) and text.strip():
            return SnowNLP(text).sentiments
        else:
            return None
    except Exception as e:
        print(f"Error processing text: {text}. Exception: {e}")
        return None

# Apply the safe sentiment analysis function
data['sentiment'] = data['text'].apply(analyze_sentiment_safe)

# Drop rows where sentiment is None (optional, for plotting purposes)
data_cleaned = data.dropna(subset=['sentiment'])

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Set font properties for Chinese text
font_path = './font_type/DongFangDaKai_Regular.ttf'
font_properties = FontProperties(fname=font_path)

# Configure and plot sentiment distribution
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(12, 8), dpi=300)
sns.set(style='whitegrid')

# Plot sentiment distribution
sns.histplot(data_cleaned['sentiment'], bins=20, kde=True, color='blue')
plt.title("Sentiment Analysis of YOLO by Danmaku on Bilibili", fontproperties=font_properties, fontsize=16)
plt.xlabel("Sentiment Score", fontproperties=font_properties, fontsize=14)
plt.ylabel("Frequency", fontproperties=font_properties, fontsize=14)

# Save and display the plot
plt.savefig('sentiment_analysis_distribution.png', format='png', bbox_inches='tight')
plt.show()
