
# Simple dictionary-based G2P

DICTIONARY = {
    # Common words
    "hello": ["h", "ɛ", "l", "o", "u"],
    "world": ["w", "ɝ", "l", "d"],
    "hi": ["h", "ɑ", "i"],
    "yes": ["j", "ɛ", "s"],
    "no": ["n", "o", "u"],
    "okay": ["o", "u", "k", "e", "i"],
    "thanks": ["θ", "æ", "n", "k", "s"],
    "please": ["p", "l", "i", "z"],
    "help": ["h", "ɛ", "l", "p"],
    "good": ["g", "ʊ", "d"],
    "bad": ["b", "æ", "d"],
    
    # Articles/pronouns
    "the": ["ð", "ə"],
    "a": ["ə"],
    "an": ["æ", "n"],
    "is": ["ɪ", "z"],
    "it": ["ɪ", "t"],
    "i": ["ɑ", "i"],
    "you": ["j", "u"],
    "we": ["w", "i"],
    "me": ["m", "i"],
    "my": ["m", "ɑ", "i"],
    "your": ["j", "ɔ", "r"],
    
    # Common verbs
    "am": ["æ", "m"],
    "are": ["ɑ", "r"],
    "can": ["k", "æ", "n"],
    "see": ["s", "i"],
    "say": ["s", "e", "i"],
    "do": ["d", "u"],
    "have": ["h", "æ", "v"],
    "get": ["g", "ɛ", "t"],
    "make": ["m", "e", "i", "k"],
    "know": ["n", "o", "u"],
    "think": ["θ", "ɪ", "n", "k"],
    "want": ["w", "ɑ", "n", "t"],
    "need": ["n", "i", "d"],
    "like": ["l", "ɑ", "i", "k"],
    
    # Question words
    "how": ["h", "ɑ", "u"],
    "what": ["w", "ʌ", "t"],
    "where": ["w", "ɛ", "r"],
    "when": ["w", "ɛ", "n"],
    "why": ["w", "ɑ", "i"],
    "who": ["h", "u"],
    
    # Common nouns
    "robot": ["r", "o", "u", "b", "ɑ", "t"],
    "name": ["n", "e", "i", "m"],
    "time": ["t", "ɑ", "i", "m"],
    "day": ["d", "e", "i"],
    "thing": ["θ", "ɪ", "n"],
    "way": ["w", "e", "i"],
    
    # Misc
    "this": ["ð", "ɪ", "s"],
    "that": ["ð", "æ", "t"],
    "test": ["t", "ɛ", "s", "t"],
    "one": ["w", "ʌ", "n"],
    "two": ["t", "u"],
    "three": ["θ", "r", "i"],
    "with": ["w", "ɪ", "θ"],
    "for": ["f", "ɔ", "r"],
    "not": ["n", "ɑ", "t"],
    "just": ["dʒ", "ʌ", "s", "t"],
    "here": ["h", "ɪ", "r"],
    "there": ["ð", "ɛ", "r"],
}

# Simple letter-to-phoneme fallback
LETTER_MAP = {
    "a": "æ", "b": "b", "c": "k", "d": "d", "e": "ɛ",
    "f": "f", "g": "g", "h": "h", "i": "ɪ", "j": "dʒ",
    "k": "k", "l": "l", "m": "m", "n": "n", "o": "ɑ",
    "p": "p", "q": "k", "r": "r", "s": "s", "t": "t",
    "u": "ʌ", "v": "v", "w": "w", "x": "k", "y": "j",
    "z": "z"
}

def text_to_phonemes(text):
    """Convert text to phoneme sequence."""
    words = text.lower().strip().split()
    phonemes = []
    
    for word in words:
        # Clean punctuation
        word = ''.join(c for c in word if c.isalpha())
        
        if word in DICTIONARY:
            phonemes.extend(DICTIONARY[word])
        else:
            # Fallback: letter by letter
            for letter in word:
                if letter in LETTER_MAP:
                    phonemes.append(LETTER_MAP[letter])
        
        # Add pause between words
        phonemes.append("_pause")
    
    return phonemes
