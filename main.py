import requests
from bs4 import BeautifulSoup
import nltk
import time
from colorama import Fore, Style
import os

nltk.download('brown')
corpus = nltk.corpus.brown
word_freq = nltk.FreqDist(corpus.words())

def main():
    os.system('clear')
    mode = input("1 - Starts With\n2 - Ends With\n\n> ")
    if mode == '2':
        ltr = input("\nEnter your string\n> ").lower()
        url = f"https://www.thefreedictionary.com/words-that-end-in-{ltr}"
        namem = "ends"
    elif mode == '1':
        ltr = input("\nEnter your string\n\n> ").lower()
        url = f"https://www.thefreedictionary.com/words-that-start-with-{ltr}"
        namem = "starts"
    else:
        print("\nInvalid input. Choose 1 or 2.")
        time.sleep(2)
        main()
        
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all(class_="TCont")

    words = []
    for link in links:
        for a_tag in link.find_all("a"):
            words.append(a_tag.text)

    filename = f"usernames_{namem}_{ltr}.txt"
    file_mode = 'a' if os.path.exists(filename) else 'w'
    with open(filename, file_mode) as file:
        unique_words = set(words)
        for word in words:
            file.write(f"{word}\n")

    with open(filename, file_mode) as file:
        for word in unique_words:
            frequency = word_freq[word.lower()]
            if frequency > 0:
                print("[+] '{}' is commonly used".format(Fore.GREEN + word + Style.RESET_ALL))
                file.write(f"{word}\n")
            else:
                print("[-] '{}' is uncommonly used".format(Fore.RED + word + Style.RESET_ALL))
    
    print(Fore.GREEN + "Finished scraping names! Press enter to continue" + Style.RESET_ALL)
    input()
    main()

main()
