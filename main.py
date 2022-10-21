import os
import requests
from random import randrange
from functools import reduce


IMAGES = [
'''
             
             
             
             
             
             
            
~~~~~~~~~~~~~~ 
''',
'''
            |
            |
            |
            |
            |
            |
            |
~~~~~~~~~~~~~~ 
''',
'''
    --------|
            |
            |
            |
            |
            |
            |
~~~~~~~~~~~~~~ 
''',
'''
    --------|
    |       |
  (-.-)     |
            |
            |
            |
            |
~~~~~~~~~~~~~~ 
''',
'''
    --------|
    |       |
  (-.-)     |
    |       |
    |       |
            |
            |
~~~~~~~~~~~~~~ 
''',
'''
    --------|
    |       |
  (-.-)     |
   /|       |
    |       |
            |
            |
~~~~~~~~~~~~~~ 
''',
'''
    --------|
    |       |
  (-.-)     |
   /|\      |
    |       |
            |
            |
~~~~~~~~~~~~~~ 
''',
'''
    --------|
    |       |
  (-.-)     |
   /|\      |
    |       |
   /        |
            |
~~~~~~~~~~~~~~ 
''',
'''
    --------|
    |       |
  (-.-)     |
   /|\      |
    |       |
   / \      |
            |
~~~~~~~~~~~~~~ 
'''
]


class Game():
    def __init__(self, show_word = False):
        self.attempts = 0
        self.word = ''
        self.word_as_list = []
        self.show_word = show_word
        self.game_state = 'HOLD'

    def init_game(self):
        '''Starts the game configs'''

        current_word = self.fetch_word()
        
        if current_word['status_code'] != requests.codes.ok:
            print('Error getting the word!')
            return

        self.word = current_word['word']
        self.word_as_list = list('?' for _ in self.word)
        
        for _ in range(randrange(0, 3)):
            idx = randrange(0, len(self.word))
            self.word_as_list[idx] = self.word[idx]
        
        self.game_state = 'PLAYING'
        self.refresh_ui()
        self.game_start()


    def fetch_word(self):
        '''Fetch the word from external API'''

        api_url = 'https://api.api-ninjas.com/v1/randomword'
        response = requests.get(api_url, headers={'X-Api-Key': 'YOUR_API_KEY'})
        
        return {
            'status_code': response.status_code,
            'word': response.json()['word'] if 'word' in response.json() else ''
        }

    def game_start(self):
        '''Show the input to the user and handled the UI updates'''
        while self.game_state == 'PLAYING':
            current_character = input('\nPlease enter some character! ')
            self.refresh_ui(current_character)
       

    def refresh_ui(self, input_character = ''):
        '''Print the game elements in the UI'''

        os.system('clear')
        character_match = False

        if self.show_word:
            print(f'TO FIND: {self.word}')

        for idx, character in enumerate(self.word):
            if character.lower() == input_character.lower():
                character_match = True
                self.word_as_list[idx] = input_character.upper()
 
        if character_match == False and input_character != '':
            self.attempts += 1

        if self.word_as_list.count('?') <= 0:
            print(f'YOU WON!\n\n{IMAGES[self.attempts]}')
            self.game_state = 'WON'
            return

        if self.attempts + 1 >= len(IMAGES):
            print(f'YOU LOST!\n\n{IMAGES[self.attempts]}')
            self.game_state = 'LOST'
            return   

        boxes = reduce(lambda a, b: a + f'|_{b.upper()}_', self.word_as_list, '')
        print(f'{IMAGES[self.attempts]}\n{boxes + "|"}', end='\n')


if __name__ == '__main__':
    game = Game(True)
    game.init_game()

   
