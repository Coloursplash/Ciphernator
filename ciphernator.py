from collections import defaultdict # because normal dicts dont support default key-value values
import math

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
            if output_score > solved_code_score:
                solved_code = output
                solved_code_score = output_score
        
        self.solved_code = solved_code#
    
    def encode_caesar(self, key: int):
        alphabet = "abcdefghijklmnopqrstuvwxyz"

        output = ""
        for letter in self.CODE:
            if letter.lower() in alphabet:
                output += alphabet[(alphabet.index(letter.lower()) + key) % 26]
            else:
                output += letter
        
        self.solved_code = output
    
    def solve_atbash(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        reversed_alphabet = alphabet[::-1] # reverse

        output = ""
        for letter in self.CODE:
            if letter.lower() in alphabet:
                output += reversed_alphabet[alphabet.index(letter.lower())]
            else:
                output += letter
        
        self.solved_code = output
    
    def encode_atbash(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        reversed_alphabet = alphabet[::-1] # reverse

        output = ""
        for letter in self.CODE:
            if letter.lower() in alphabet:
                output += alphabet[reversed_alphabet.index(letter.lower())]
            else:
                output += letter
        
        self.solved_code = output
    
    def solve_transposition_simple(self):
        sorted_code = ""
        sorted_score = 0

        # try key as 2-9
        # 0 cant work and 1 doesnt move anything
        for key in range(3, 4):
            row = len(self.CODE) // key
            code = ""

            for i in range(row):
                for j in range(key):
                    code += self.CODE[j * row + i]
            

            code_score = self.englishity(code)
            if code_score > sorted_score:
                sorted_code = code
                sorted_score = code_score
    
        self.solved_code = sorted_code
    
    def encode_simple_transposition(self, key: int):
        text = self.CODE
        output = []
        
        while text != "":
            temp = []
            for i in range(key):
                if i <= len(text):
                    temp.append(text[i])
            output.append(temp)
            text = text[key:]
        
        str_output = ""
        for i in range(key):
            for j in range(len(output)):
                str_output += output[j][i]

        self.solved_code = str_output
    
    def decode_railfence(self):
        cipher = self.CODE
        
        solved_code = ""
        solved_score = 0
        
        for key in range(10):
            # create the matrix to cipher
            # plain text key = rows ,
            # length(text) = columns
            # filling the rail matrix to
            # distinguish filled spaces
            # from blank ones
            rail = [['\n' for i in range(len(cipher))]
                        for j in range(key)]
            
            # to find the direction
            dir_down = None
            row, col = 0, 0
            
            # mark the places with '*'
            for i in range(len(cipher)):
                if row == 0:
                    dir_down = True
                if row == key - 1:
                    dir_down = False
                
                # place the marker
                rail[row][col] = '*'
                col += 1
                
                # find the next row
                # using direction flag
                if dir_down:
                    row += 1
                else:
                    row -= 1
                    
            # now we can construct the
            # fill the rail matrix
            index = 0
            for i in range(key):
                for j in range(len(cipher)):
                    if ((rail[i][j] == '*') and
                    (index < len(cipher))):
                        rail[i][j] = cipher[index]
                        index += 1
                
            # now read the matrix in
            # zig-zag manner to construct
            # the resultant text
            result = []
            row, col = 0, 0
            for i in range(len(cipher)):
                
                # check the direction of flow
                if row == 0:
                    dir_down = True
                if row == key-1:
                    dir_down = False
                    
                # place the marker
                if (rail[row][col] != '*'):
                    result.append(rail[row][col])
                    col += 1
                    
                # find the next row using
                # direction flag
                if dir_down:
                    row += 1
                else:
                    row -= 1
            
            output = "".join(result)
            output_score = self.englishity(output)
            if output_score > solved_score:
                solved_code = output
                solved_score = output_score
        
        self.solved_code = solved_code
    
    def encode_railfence(self, key: int):
        text = self.CODE
        rail = [['\n' for i in range(len(text))]
                      for j in range(key)]
        
        dir_down = False
        row, col = 0, 0
        
        for i in range(len(text)):
            if (row == 0) or (row == key - 1):
                dir_down = not dir_down
            
            rail[row][col] = text[i]
            col += 1
            
            if dir_down:
                row += 1
            else:
                row -= 1        

        result = []
        for i in range(key):
            for j in range(len(text)):
                if rail[i][j] != '\n':
                    result.append(rail[i][j])
        output = "".join(result)

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
