import json
import requests

class Glossary:

    def __init__(self):
        self.word = ''
        self.meanings = {}
        self.status = False
        self.ready_for_request = False
        self.phonetic = {}
        self.synonyms = []
        self.antonyms = []


    def new_word(self, word):
        self.word = word
        self.ready_for_request = True
        self.meanings = {}
        self.phonetic = {}
        self.synonyms = []
        self.antonyms = []
        self.status = False

    def get(self):
        '''
        If there is such a word in an API, it returns list of dictionaries. 
        In this realisation only first dictionary from the list is used
        If request returns dictionary, and not a list, it means that there is no such word.

        data of first dictionary in the list looks like:
        {
            word: 'WORD'
            phonetic: 'TRANSCRIPTION'
            phonetics: [
                        0: {text: 'transcription', audio: 'link for audio'}
                        .....
                        ]
            meanings: [
                        0: {
                            partOfSpeech = 'noun'
                            definitions: [
                                            0: {
                                                defintion = 'definition'
                                                synonyms = []
                                                antonyms = []
                                                example = 'example'
                                                }
                                            ....
                                            ]
                            }
                        .....
                        ]
        }


        We are constructing self.meanings to look like this:
        self.meanings = {
            
                        partOfSpeech1: {
                                        definition1: example1
                                        definition2: example2
                                        ....
                                        }

                        partOfSpeech2:  {....}

                        ....
                        }

        '''

        if self.ready_for_request:
            response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}').json()
            if type(response) != dict:
                self.status = True
        
        if self.status:
            data = response[0]
            if 'phonetic' in data.keys():
                self.phonetic['transcription'] = data['phonetic']

            for record in data['phonetics']:
                if record['audio'] != '' and len(record) != 0:
                    if 'audio' in record.keys():
                        self.phonetic['audio'] = record['audio']
                    if 'text' in record.keys():
                        self.phonetic['transcription'] = record['text']
                    break
            

            for meaning_in_data in data['meanings']:
                self.meanings[meaning_in_data['partOfSpeech']] = {}

                for definition in meaning_in_data['definitions']:
                    if 'example' in definition.keys():
                        if definition['example'] != '':
                            self.meanings[meaning_in_data['partOfSpeech']][definition['definition']] = definition['example']
                    else:
                        self.meanings[meaning_in_data['partOfSpeech']][definition['definition']] = ''
        

    def print(self):
        if self.status:
            print(f'\n-------------{self.word}------------\n')

            if 'transcription' in self.phonetic.keys():
                print('Transcription:', self.phonetic['transcription'])

            if 'audio' in self.phonetic.keys():
                print('Pronunciation:', self.phonetic['audio'])

            print()
            for part_of_speach in self.meanings.keys():
                print('Part of speech:', part_of_speach.upper())

                definitions_and_examples = self.meanings[part_of_speach]

                definitions = definitions_and_examples.keys()

                for definition in definitions:

                    if definitions_and_examples[definition] != '':
                        print('DEFINITION: ', definition)
                        print('EXAMPLE: ', definitions_and_examples[definition], '\n')
                    else:
                        print('DEFINITION: ', definition, '\n')

            print('-------------------------------------\n')
        else:
            print('Either no definitions, or might be an error')


    def build_string(self):
        string_for_output = ''
        if self.status:
            string_for_output += f'-------------{self.word}------------\n'

            if 'transcription' in self.phonetic.keys():
                string_for_output += f'\nTranscription: {self.phonetic["transcription"]}\n'
            
            if 'audio' in self.phonetic.keys():
                string_for_output += f'Pronunciation: {self.phonetic["audio"]}\n'

            for part_of_speach in self.meanings.keys():
                string_for_output += f'\nPart of speech: {part_of_speach.upper()}\n'

                definitions_and_examples = self.meanings[part_of_speach]

                definitions = definitions_and_examples.keys()

                for definition in definitions:

                    if definitions_and_examples[definition] != '':
                        string_for_output += f'DEFINITION: {definition}\n'
                        string_for_output += f'EXAMPLE: {definitions_and_examples[definition]}\n\n'
                    else:
                        string_for_output += f'DEFINITION: {definition}\n\n'

            string_for_output += '-------------------------------------\n'
        else:
            string_for_output += 'Either no definitions, or might be an error'

        return string_for_output

    def get_and_build(self, word):
        self.new_word(word)
        self.get()
        return self.build_string()

    def get_and_print(self, word):
        self.new_word(word)
        self.get()
        self.print()