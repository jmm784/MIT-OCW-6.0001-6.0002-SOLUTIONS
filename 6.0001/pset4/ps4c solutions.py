# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a_solutions_copy import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        transpose_dict = {}
        vowels_permutation_upper = vowels_permutation.upper()
        for letter in string.ascii_letters:
            transpose_dict[letter] = letter
            
        i = 0
        for letter in VOWELS_LOWER:
            transpose_dict[letter] = vowels_permutation[i]
            i += 1
        
        j = 0
        for letter in VOWELS_UPPER:
            transpose_dict[letter] = vowels_permutation_upper[j]
            j += 1
        
        return transpose_dict
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        encrypted_message_list = []
        for character in self.get_message_text():
            if character in string.ascii_letters:
                encrypted_message_list.append(transpose_dict[character])
            else:
                encrypted_message_list.append(character)
        
        return "".join(encrypted_message_list)
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        tdict_list = []
        words_in_message = {}
        vowel_perms = list(get_permutations(VOWELS_LOWER))
        
        for perm in vowel_perms:
            tdict_list.append(self.build_transpose_dict(perm))
        
        for trans_dict in tdict_list:
            i = 0
            decrypt_message = self.apply_transpose(trans_dict)
            
            for word in decrypt_message.split():
                if is_word(self.get_valid_words(), word):
                    i += 1
            
            words_in_message[i] = decrypt_message
            
        max_words = max(words_in_message.keys())
        return words_in_message[max_words]
        
        


if __name__ == '__main__':
    
    message1 = SubMessage("Hi there my friend!")
    permutation1 = 'aouie'
    enc_dict1 = message1.build_transpose_dict(permutation1)
    print("Original message:", message1.get_message_text(), "Permutation:", permutation1)
    print("Expected encryption:", "Hu thoro my fruond!")
    print("Actual encryption:", message1.apply_transpose(enc_dict1))
    enc_message1 = EncryptedSubMessage(message1.apply_transpose(enc_dict1))
    print("Decrypted message:", enc_message1.decrypt_message())
    print()
    
    message2 = SubMessage("Are the leeches out of my attic walls yet?")
    permutation2 = 'iuoea'
    enc_dict2 = message2.build_transpose_dict(permutation2)
    print("Original message:", message2.get_message_text(), "Permutation:", permutation2)
    print("Expected encryption:", "Iru thu luuchus eat ef my ittoc wills yut?")
    print("Actual encryption:", message2.apply_transpose(enc_dict2))
    enc_message2 = EncryptedSubMessage(message2.apply_transpose(enc_dict2))
    print("Decrypted message:", enc_message2.decrypt_message())
    print()
    
    #Example test case
#     message = SubMessage("Hello World!")
#     permutation = "eaiuo"
#     enc_dict = message.build_transpose_dict(permutation)
#     print("Original message:", message.get_message_text(), "Permutation:", permutation)
#     print("Expected encryption:", "Hallu Wurld!")
#     print("Actual encryption:", message.apply_transpose(enc_dict))
#     enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
#     print("Decrypted message:", enc_message.decrypt_message())




# =============================================================================
# test = SubMessage("whats up fool, how you been living cuz")
# tran_dic = test.build_transpose_dict('eioua')
# print(test.apply_transpose(tran_dic))
# 
# test2 = EncryptedSubMessage(test.apply_transpose(tran_dic))
# print(test2.decrypt_message())
# =============================================================================















