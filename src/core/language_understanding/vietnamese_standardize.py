import regex as re

class VietnameseStandardize:
    def __init__(self):
        self.list_vowels = [
            ['a', 'à', 'á', 'ả', 'ã', 'ạ', 'a'],
            ['ă', 'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ', 'aw'],
            ['â', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ', 'aa'],
            ['e', 'è', 'é', 'ẻ', 'ẽ', 'ẹ', 'e'],
            ['ê', 'ề', 'ế', 'ể', 'ễ', 'ệ', 'ee'],
            ['i', 'ì', 'í', 'ỉ', 'ĩ', 'ị', 'i'],
            ['o', 'ò', 'ó', 'ỏ', 'õ', 'ọ', 'o'],
            ['ô', 'ồ', 'ố', 'ổ', 'ỗ', 'ộ', 'oo'],
            ['ơ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ', 'ow'],
            ['u', 'ù', 'ú', 'ủ', 'ũ', 'ụ', 'u'],
            ['ư', 'ừ', 'ứ', 'ử', 'ữ', 'ự', 'uw'],
            ['y', 'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ', 'y']
        ]

        self.telex_tone_marks = ['', 'f', 's', 'r', 'x', 'j']

        self.vowel_to_idx = {}

        for i in range(len(self.list_vowels)):
            for j in range(len(self.list_vowels[i]) - 1):
                self.vowel_to_idx[self.list_vowels[i][j]] = (i, j)

    def word_to_chars(self, src_word):
        """
        Convert the word to characters in TELEX
        Example: 
            source word: "trường",
            target word: "truowngf"
        """
        punctuation = 0
        target_word = ''
        for char in src_word:
            x, y = self.vowel_to_idx.get(char, (-1, -1))
            if x == -1:
                target_word += char
                continue
            if y != 0:
                punctuation = y
            target_word += self.list_vowels[x][-1]
        target_word += self.telex_tone_marks[punctuation]
        return target_word


    def sentence_to_chars(self, sentence):
        """

        """
        words = sentence.split()
        for index, word in enumerate(words):
            words[index] = self.word_to_chars(word)
        return ' '.join(words)

    def _is_valid_vietnamese(self, word):
        chars = list(word)
        vowel_index = -1
        for index, char in enumerate(chars):
            x, y = self.vowel_to_idx.get(char, (-1, -1))
            if x != -1:     ## x != consonant
                if vowel_index == -1:   ## initial value
                    vowel_index = index
                else:
                    if index - vowel_index != 1:
                        return False
                    vowel_index = index
        return True

    def standardize_tone_marks(self, src_word):
        chars = list(src_word)
        punctuation = 0
        vowel_index = []
        qu_or_gi = False
        for index, char in enumerate(chars):
            x, y = self.vowel_to_idx.get(char, (-1, -1))
            if x == -1:
                continue
            elif x == 9:  # check qu
                if index != 0 and chars[index - 1] == 'q':
                    chars[index] = 'u'
                    qu_or_gi = True
            elif x == 5:  # check gi
                if index != 0 and chars[index - 1] == 'g':
                    chars[index] = 'i'
                    qu_or_gi = True
            if y != 0:
                punctuation = y
                chars[index] = self.list_vowels[x][0]
            if not qu_or_gi or index != 1:
                vowel_index.append(index)
        if len(vowel_index) < 2:
            if qu_or_gi:
                if len(chars) == 2:
                    x, y = self.vowel_to_idx.get(chars[1])
                    chars[1] = self.list_vowels[x][punctuation]
                else:
                    x, y = self.vowel_to_idx.get(chars[2], (-1, -1))
                    if x != -1:
                        chars[2] = self.list_vowels[x][punctuation]
                    else:
                        chars[1] = self.list_vowels[5][punctuation] if chars[1] == 'i' else self.list_vowels[9][punctuation]
                return ''.join(chars)
            return src_word

        for index in vowel_index:
            x, y = self.vowel_to_idx[chars[index]]
            if x == 4 or x == 8:  # ê, ơ
                chars[index] = self.list_vowels[x][punctuation]
                return ''.join(chars)

        if len(vowel_index) == 2:
            if vowel_index[-1] == len(chars) - 1:
                x, y = self.vowel_to_idx[chars[vowel_index[0]]]
                chars[vowel_index[0]] = self.list_vowels[x][punctuation]
            else:
                x, y = self.vowel_to_idx[chars[vowel_index[1]]]
                chars[vowel_index[1]] = self.list_vowels[x][punctuation]
        else:
            x, y = self.vowel_to_idx[chars[vowel_index[1]]]
            chars[vowel_index[1]] = self.list_vowels[x][punctuation]
        return ''.join(chars)

    def standardize_sentence(self, sentence: str):
        """
            :param sentence:
            :return:
            """
        sentence = sentence.lower()
        words = sentence.split()
        for index, word in enumerate(words):
            cw = re.sub(r'(^\p{P}*)([p{L}.]*\p{L}+)(\p{P}*$)', r'\1/\2/\3', word).split('/')
            # print(cw)
            if len(cw) == 3:
                cw[1] = self.standardize_tone_marks(cw[1])
            words[index] = ''.join(cw)
        return ' '.join(words)

if __name__ == '__main__':
    standardizer = VietnameseStandardize()
    raw_text = "hoà bình"
    
    result = standardizer.standardize_sentence(sentence=raw_text)
    print(result)
