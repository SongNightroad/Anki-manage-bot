# pyright: reportOptionalMemberAccess=false
import sys
import json
import requests
from dataclasses import dataclass
from typing import Optional, Tuple, List
from bs4 import BeautifulSoup, Tag
# you also will need lxml (pip install lxml)

DECK_NAME = "Китай Elementary 1 обратная"


@dataclass
class ChineseWord:
    characters: str
    audio_url: str
    pinyin: str
    meanings: str


class EmptySearchResults(Exception):
    pass


class DuplicateCardFound(Exception):
    pass


class AnkiRequestError(Exception):
    pass


def parse_page(search_term: str) -> BeautifulSoup:
    downloaded_page = requests.get(
        "https://chinese.yabla.com/chinese-english-pinyin-dictionary.php?define=" + search_term
    )
    downloaded_page.raise_for_status()
    return BeautifulSoup(downloaded_page.text, features="lxml")


def parse_word(word: Tag) -> Tuple[str, str]:
    word_chars = ''.join([char.text for char in word.find_all('a')])  # type:ignore
    audio_url: str = word.i['data-audio_url']  # type:ignore
    return word_chars, audio_url


def find_characters(search_term: str) -> List[ChineseWord]:
    page = parse_page(search_term)

    # The check for word.i is needed to exclude traditional characters
    words = [word for word in page.body.section.ul.find_all(class_="word") if word.i]  # type:ignore
    pinyins = [pinyin.text for pinyin in page.body.section.ul.find_all(class_="pinyin")]  # type:ignore
    meanings = [meaning.text for meaning in page.body.section.ul.find_all(class_="meaning")]  # type:ignore

    search_results = []
    for i, word in enumerate(words):
        word_chars, audio_url = parse_word(word)  # type:ignore
        search_results.append(ChineseWord(word_chars, audio_url, pinyins[i], meanings[i]))

    if not search_results:
        raise EmptySearchResults(search_term)
    return search_results


def exclude_surnames(word: ChineseWord) -> Optional[ChineseWord]:
    meanings = word.meanings.split('\n')
    meanings = [meaning for meaning in meanings if not meaning.lower().startswith('surname')]
    if not meanings:
        return None
    return ChineseWord(
        word.characters,
        word.audio_url,
        word.pinyin,
        '<br>'.join(meanings)
    )


def relevant_meanings(results: List[ChineseWord], search_term: str) -> List[ChineseWord]:
    new_results = []
    for word in results:
        filtered_word = exclude_surnames(word)
        if filtered_word is None:
            continue
        if filtered_word.characters == search_term:
            new_results.append(filtered_word)
    return new_results


def find_anki_card(character: str) -> bool:
    request_json = json.dumps({
        'action': 'findNotes',
        'version': 6,
        'params': {
            'query': f'deck:"{DECK_NAME}" ' + '"Иероглиф упрощенный:' + character + '"'
        }
    }).encode('utf-8')
    response = requests.post('http://localhost:8765', data=request_json).json()
    if response['error'] is not None:
        raise AnkiRequestError(response['error'])
    return bool(response['result'])


def add_anki_card(words: List[ChineseWord]) -> str:
    characters = words[0].characters
    audio_filename = characters + '.mp3'
    pinyins = '<br>———<br>'.join([word.pinyin for word in words])
    meanings = '<br>———<br>'.join([word.meanings for word in words])

    if find_anki_card(characters):
        raise DuplicateCardFound(characters)

    parameters = {'note': {
        'deckName': DECK_NAME,  # колода
        'modelName': 'Основная',
        'fields': {
            'Иероглиф упрощенный': characters,
            'Пиньинь': pinyins,
            'Перевод': meanings,
            'Аудио': ''
        },
        'options': {
            "allowDuplicate": False,
            "duplicateScope": "deck",
            "duplicateScopeOptions": {
                "deckName": "1",
                "checkChildren": False
            }
        },
        'tags': [],
        'audio': [{
            'url': word.audio_url,
            'filename': audio_filename,
            'fields': ['Аудио']
        } for word in words]
    }}

    request_json = json.dumps({'action': 'addNote', 'version': 6, 'params': parameters}).encode('utf-8')
    response = requests.post('http://localhost:8765', data=request_json).json()
    if response['error'] is not None:
        raise AnkiRequestError(response['error'])
    return response


def main():

    search_terms = sys.argv[1:]  # Get search terms from command line arguments

    for search_term in search_terms:
        for search_term_i in search_term.split():
                    try:
                        search_results = find_characters(search_term_i)
                    except EmptySearchResults:
                        print(f"\nNo results found for {search_term_i}")
                        continue

                    suitable_words = relevant_meanings(search_results, search_term_i)
                    if not suitable_words:
                        print(f"\nNo relevant meanings found for {search_term_i}\nThe full search results:\n")
                        for word in search_results:
                            print(word.characters, word.pinyin, word.meanings, word.audio_url, sep='\n')
                        continue

                    for word in suitable_words:
                        print(word.characters, word.pinyin, word.meanings, word.audio_url, sep='\n')

                    try:
                        add_anki_card(suitable_words)
                    except AnkiRequestError as err:
                        print(f"\nError in request to Anki server: {err}")
                    except DuplicateCardFound as characters:
                        print(f"\nThe card for {characters} already exists")


    

if __name__ == "__main__":
    main()