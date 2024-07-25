import requests
from bs4 import BeautifulSoup
from collections import Counter
import re


def count_word_frequency(url, target_word):
    # this function counts the number of occurrences of the target vocab 該函數用來統計目標詞彙出現次數
    # get website content 獲取網站內容·
    response = requests.get(url)
    ab = BeautifulSoup(response.content, 'html.parser')

    # get the main content of the website 獲取網站正文內容
    paragraphs = ab.find_all('p')

    # combine all text into a string 合併網站內所有文字到字符串內
    text = ' '.join([p.get_text() for p in paragraphs])

    # count the number of occurrences of target words 統計目標詞彙（target word)的出現次數
    word_count = text.lower().count(target_word.lower())

    # output result 輸出結果
    print(f"The word '{target_word}' appears {word_count} times in the article.")

# this function counts high frequency words 該函數統計高頻詞彙
def count_words_occurrences(url, min_occurrences=5,filter_common=True ):
    # get website content 獲取網站內容·
    response = requests.get(url)
    ab = BeautifulSoup(response.content, 'html.parser')

    # get the main content of the website 獲取網站正文內容
    paragraphs = ab.find_all('p')

    # combine all text into a string 合併網站內所有文字到字符串內
    text = ' '.join([p.get_text() for p in paragraphs])

    # counts the number of occurrences of each word 統計每個詞彙出現次數
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)

    if filter_common:
        word_counts = filter_common_words(word_counts)

    selected_words = [word for word, count in word_counts.items() if count >= min_occurrences]

    # filter out words that appear at least(min_occurrences)time 篩選出現至少 min_occurrences 次的詞彙
    print(f"Words appearing at least {min_occurrences} times in the article:")
    for i, word in enumerate(selected_words, start=1):
        print(f"{i:02d}. {word}")

    return selected_words

def top_n_words(url, n, filter_common=True):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)

    if filter_common:
        word_counts = filter_common_words(word_counts)

    top_words = word_counts.most_common(n)
    print(f"Top {n} words appearing on the website:")
    for i, (word, count) in enumerate(top_words, start=1):
        print(f"{i}. {word} - {count} times")

def filter_common_words(word_counts):

    for common_word in COMMON_WORDS:
        if common_word in word_counts:
            del word_counts[common_word]
    return word_counts



COMMON_WORDS = ["a", "the", "is", "and", "of", "to", "in", "that", "it", "for", "with", "as", "on", "at", 
                "I", "you", "he", "she", "we", "they", "me", "him", "her", "us", "them", 
                "this", "that", "these", "those", "here", "there", "when", "where", 
                "why", "how", "which", "what", "who", "whom", "whose", 
                "if", "then", "else", "not", "be", "have", "do", "can", "will", 
                "would", "could", "should", "might", "must",
                "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

print('ruler/規則')
print('the program is used to help acount the vocab of the website')
print('本軟件用於幫助統計網站詞彙')
print('--------------------------------------')
print('Select function/選擇功能')
print('Function 1: Count the number of occurrences of target words')
print('Function 2: List words that appear more frequently')
print('Function 3: List top  words with highest frequency')
print('---------------------------------------')
apo = int(input('Enter your selection (1,2 or 3): '))
print('---------------------------------------')

if apo == 1:
    url = input("Enter the URL of the website: ")
    target_word = input("Enter the target word to count: ")
    count_word_frequency(url, target_word)

elif apo == 2:
    url = input("Enter the URL of the website: ")
    min_occurrences = int(input('Minimum occurrences: '))
    filter_common = input("Filter common words? (y/n): ").lower() == 'y'
    selected_words = count_words_occurrences(url, min_occurrences, filter_common)



elif apo == 3:
    url = input("Enter the URL of the website: ")
    n = int(input('How many you need '))
    filter_common = input("Filter common words? (y/n): ").lower() == 'y'
    top_n_words(url, n, filter_common)

input("Press' Enter 'to exit")
