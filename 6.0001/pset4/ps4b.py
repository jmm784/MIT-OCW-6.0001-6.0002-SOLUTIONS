# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

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

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
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

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        list_lowerletters = list(string.ascii_lowercase)
        list_upperletters = list(string.ascii_uppercase)
        x = shift
        cipher_dict = {}
        for letter in list_lowerletters:
            if x > 25:
                cipher_dict[letter] = list_lowerletters[x - len(list_lowerletters)]
            else:
                cipher_dict[letter] = list_lowerletters[x]
            x += 1
        
        x = shift
        for letter in list_upperletters:
            if x > 25:
                cipher_dict[letter] = list_upperletters[x - len(list_upperletters)]
            else:
                cipher_dict[letter] = list_upperletters[x]
            x += 1
        
        return cipher_dict
        
    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        
        apply_shift_message = []
        cipher_dict_2 = self.build_shift_dict(shift)
        for character in self.get_message_text():
            if character in string.ascii_letters:
                apply_shift_message.append(cipher_dict_2[character])
            else:
                apply_shift_message.append(character)
        
        return "".join(apply_shift_message)
        
class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)
        

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.__init__(self.get_message_text(), shift)
        return None


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        dict_s_values = {}
        for s in range(26):
            word_counter = 0
            decrypted_message = self.apply_shift(26 - s)
            decrypted_message_list = list(decrypted_message.split())
            for word in decrypted_message_list:
                if is_word(self.get_valid_words(), word):
                    word_counter += 1
            dict_s_values[26 - s] = word_counter

        best_shift = max(dict_s_values, key=dict_s_values.get)
        return_tuple = (best_shift, self.apply_shift(best_shift))
        return return_tuple

if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('jgnnq')
#    print('Expected Output:', (24, 'hello'))
#    print('Actual Output:', ciphertext.decrypt_message())

# =============================================================================
#     plaintext1 = PlaintextMessage('Shed', 3)
#     print('Expected Output: Vkhg')
#     print('Actual Output:', plaintext1.get_message_text_encrypted())
#     
#     plaintext2 = PlaintextMessage('yelp!', 6)
#     print('Expected Output: ekrv!')
#     print('Actual Output:', plaintext2.get_message_text_encrypted())
#     
#     ciphertext1 = CiphertextMessage('Vkhg')
#     print('Expected Output:', (23, 'Shed'))
#     print('Actual Output:', ciphertext1.decrypt_message())
#     
#     ciphertext2 = CiphertextMessage('ekrv!')
#     print('Expected Output:', (20, 'yelp!'))
#     print('Actual Output:', ciphertext2.decrypt_message())
# =============================================================================
    
    #TODO: best shift value and unencrypted story 
    (12, """'Jack Florey is a mythical character created on the
     spur of a moment to help cover an insufficiently planned hack. 
     He has been registered for classes at MIT twice before, 
     but has reportedly never passed aclass. It has been the tradition
     of the residents of East Campus to become Jack Florey for
     a few nights each year to educate incoming students
     in the ways, means, and ethics of hacking.'""")

STORY_FILENAME = 'story.txt'
in_story = open(STORY_FILENAME, 'r')
cipher_story = CiphertextMessage(in_story.read())
print(cipher_story.decrypt_message())
















