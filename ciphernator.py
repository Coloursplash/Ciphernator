from collections import defaultdict # because normal dicts dont support default key-value values

class Ciphernator:
    CODE = ""
    solved_code = ""

    BIGRAMS = {}

    def __init__(self, code):
        self.CODE = code

        with open("bigrams", "r") as f:
            for line in f.readlines():
                temp_count_list = line.split()
                self.BIGRAMS[temp_count_list[0]] = float(temp_count_list[1][:-1]) # [:-1] to get rid of \n
    
    def get_output(self):
        return self.solved_code

    def solve_caesar(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz"

        solved_code = ""
        solved_code_score = 0

        for i in range(26):
            output = ""
            for letter in self.CODE:
                if letter.lower() in alphabet:
                    output += alphabet[(alphabet.index(letter.lower()) + i) % 26]
                else:
                    output += letter
            output_score = self.englishity(output)
            print(output[:50], output_score)
            if output_score > solved_code_score:
                solved_code = output
                solved_code_score = output_score
        
        self.solved_code = solved_code
    
    def solve_atbash(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        reversed_alphabet = alphabet[::-1]

        output = ""
        for letter in self.CODE:
            if letter.lower() in alphabet:
                output += reversed_alphabet[alphabet.index(letter.lower())]
            else:
                output += letter
        
        self.solved_code = output
    
    # rates how close the text is to "english"
    # uses bigram detection and chi squared formula
    def englishity(self, code) -> float:

        total = 0

        # occurences of bigrams in the code
        codecount = {}

        # occurences of bigrams in real life
        realcount = self.BIGRAMS

        # creates defaultdict because then the += operator wont work on empty keys
        codecount = defaultdict(lambda:0,codecount)

        # counts bigrams
        for i in range(len(code)-1):
            total += 1
            if code[i]+code[i+1] in realcount:
                codecount[code[i]+code[i+1]]+=1
        
        # converts codecount to a percentage instead of raw occurences (so we can compare with realcount)
        for i in codecount.keys():
            codecount[i] = float(codecount[i]/total)
        
        # chi squared formula, which is basically just standard deviation
        chisquared = 0
        for i in realcount.keys():
            chisquared += pow(codecount[i]-realcount[i],2)/realcount[i]

        return 1 - chisquared
