"""
Downloads several word frequency lists to be used later
"""
import requests

def download_frequency_lists():
    # A dictionary of reputable sources
    # 1. Google 10k: Very clean, based on Google's Trillion Word Corpus
    # 2. OpenSubtitles (HermitDave): Modern TV/Movie frequency (Successor to 2006 list)
    # 3. GitHub Wordlist: A larger general-purpose 100k list
    sources = {
        "google_10k.txt": "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt",
        "opensubtitles_2018.txt": "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/en/en_50k.txt",
        "general_english_100k.txt": "https://raw.githubusercontent.com/ManiacDC/TypingAid/master/Wordlists/Wordlist%20100000%20frequency%20weighted%20(Google%20Books).txt"
    }

    for filename, url in sources.items():
        print(f"Downloading {filename}...")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Successfully saved to {filename}")
            
        except Exception as e:
            print(f"Could not download {filename}: {e}")

if __name__ == "__main__":
    download_frequency_lists()