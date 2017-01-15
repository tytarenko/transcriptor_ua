"""
    Transcriptor module
"""
import re
import string


class Characters:

    accent_char = '\N{COMBINING ACUTE ACCENT}'
    breve_char = '\N{COMBINING INVERTED BREVE}'

    VOWEL = '0'
    C_SONORANT = '1'
    C_VOICING = '2'
    C_VOICELESSNESS = '3'
    ASYLLABIC_CHAR = '5'

    asyllabics = {
        'в': 'ў',
        'й': 'ĭ'
    }

    all_vowels = ('а', 'е', 'и', 'і', 'о', 'у', 'є', 'ю', 'я', 'ї',)
    simple_vowels = ('а', 'е', 'и', 'і', 'о', 'у',)
    all_consonants = ('б', 'в', 'г', 'ґ', 'д', 'ж', 'з', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', )

    complex_vowels = {
        'я': ('йа', "'а"),
        'ю': ('йу', "'у"),
        'є': ('йе', "'е"),
        'ї': ('йі', "йі"),
        'і': ('і', "'і"),
    }

    complex_consonants = {
        'дз': 'д̑з',
        'дж': 'д̑ж',
        'щ': 'шч',
    }

    # excluded й
    consonants_sonorant = ("в", "м", "н", "л", "р",)
    consonants_voicing = ("б", "д", "г", "ґ", "з", "ж", 'д̑ж', 'д̑з', )
    consonants_voicelessness = ("п", "т", "к", "х", "с", "ш", "ч", "ц", "ф", )

    unaccented_vowels = {
        'е': u"е\u1D58",
        'и': u"и\u1D49",
        'о': u"о\u02B8",
        # 'у': u"у\u1D52",
        # 'i': u"i\u1D58",
    }


def assimilate(word):

    original_word = word

    # сш → [шш]: вирісши [ви́ріш: и]
    if word.find('сш') > -1:
        word = word.replace('сш', 'ш:')

    # зш → на початку слова [шш]: зши́ти [ш: и́ти]
    if word.startswith('зш'):
        word = word.replace('зш', 'ш:')

    # зш → в середині слова → [жш]: ви́візши [ви́вʻʻіжши],
    if not word.startswith('зш') and word.find('зш') > 0:
        word = word.replace('зш', 'жш')

    # зж → [жж]: зжо́вкнути [ж: о́ўкнути], безжа́лісний [беиж: а́лісниĭ]
    word = word.replace('зж', 'ж:')

    # зч → в середині слова [жч] безче́сний [беижче́сниĭ]
    if not word.startswith('зч') and word.find('зч') > 0:
        word = word.replace('зч', 'жч')

    # зч → на початку слова [шч]: зчи́стити [шчи́стиети]
    if word.startswith('зч'):
        word = word.replace('зч', 'шч')

    # шсь → [ссь]: милу́єшся [миелу́јиіс':а]
    word = word.replace("шс'", "с':")

    # жсь → [зьсь]: зва́жся [зва́з'с'а]
    word = word.replace("жс'", "з'с'")

    # чсь → [цьсь]: не моро́чся [моро́ц'с'а]
    word = word.replace("чс'", "ц'с'")

    # шць → [сьць]: на до́шці [на до́с'ц'і]
    word = word.replace("шц'", "с'ц'")

    # жць → [зьць]: на сму́жці [смуз'ц'і]
    word = word.replace("жц'", "з'ц'")

    # чць → [цць:]: у ху́сточці [ху́стоц':і]
    word = word.replace("чц'", "ц':")

    # дс → [дзс]: ві́дступ [вʻʻі́д̑зступ]
    word = word.replace('дс', 'д̑зс')

    # дц → [дзц]: відцура́тися [вʻʻід̑зцура́тиес'а]
    word = word.replace('дц', 'д̑зц')

    # дш → [джш]: відшліфува́ти [вʻʻід͡жшл'іфува́ти]
    word = word.replace('дш', 'д̑жш')

    # дч → [джч]: відчини́ти [вʻʻід͡жчиени́ти]
    word = word.replace('дч', 'д̑жч')

    # дж → [джж]: віджива́ти [вʻʻід͡жжиева́ти]
    word = word.replace('дж', 'д̑жж')

    # дз → [дзз]: ві́дзвук [вʻʻі́д̑ззвук]
    word = word.replace('дз', 'д̑зз')

    # тц → [цц]: кори́тце [кори́ц: е]
    word = word.replace('тц', 'ц:')

    # тьсь → [ц':]: говориться – [гово´риц‘:а]
    word = word.replace("т'с'", "ц:'")

    # тч → [чч]: кві́тчати [квʻʻіч: а́ти]
    word = word.replace('тч', 'ч:')

    # нтськ → [ньськ]: студе́нтський [студе́н'с'киĭ]
    word = word.replace("нтс'к", "н'с'к")

    # стч → [шч]: невістчин [неивʻʻі́шч иен]
    word = word.replace('стч', 'шч')

    # стд → [зд]: шістдесят [шʻʻіздеис'а́т]
    word = word.replace('стд', 'зд')

    # чн  → [шн]
    word = word.replace('чн', 'шн')

    # р’ = [рр]
    pos = word.find('’')
    if pos > -1:
        char = "':"
        word = word.replace('’й', char)

    # стськ → у звичайному темпі [ськ]: туристський [тури́с'киĭ],
    word1 = word.replace("стс'к", "с'к")
    # or
    # стськ → у повільнішому [сcьк]: [тури́с':киĭ]
    word2 = word.replace("стс'к", "с':к")

    if word != word1 != word2:
        return original_word, word1, word2,

    # стс → [сс]: шістсот [шʻіс: о́т]
    word = word.replace('стс', 'с:')

    # тс → [ц]: бра́тство [бра́цтво]
    word = word.replace('тс', 'ц')

    # тш → у нормальному темпі мовлення [чш]: бага́тшати [бага́чшати],
    word1 = word.replace('тш', 'чш')
    # or
    # тш → у жвавому мовленні [чч]: [бага́ч: ати]
    word2 = word.replace('тш', 'ч:')

    if word != word1 != word2:
        return original_word, word1, word2,

    # стць → [сьць ]: арти́стці [арти́с'ц'і],
    word1 = word.replace("стц'", "с'ц'")
    # or
    # стць → у старанній вимові→[с'ц':]: [арти́сʻʻц':і]
    word2 = word.replace("стц'", "с'ц'")

    if word != word1 != word2:
        return original_word, word1, word2,

    if original_word != word:
        return original_word, word,
    else:
        return original_word,


class FormatterWord(Characters):

    def __init__(self, word):
        self.word = word
        self.accent_index = False

        self.format()

    def format(self):
        self.replace_quotes_apostrophe()
        self.clear_punctuation_chars()
        self.get_accent_index()
        self.replace_soft_sings()
        self.replace_complex_vowels()
        self.replace_complex_consonants()
        self.replace_double_consonants()
        self.replace_asyllabics_chars()

    def replace_quotes_apostrophe(self):
        for char in ('"', "'"):
            self.word = self.word.replace(char, '’')

    def clear_punctuation_chars(self):
        for char in string.punctuation:
            self.word = self.word.replace(char, '')

    def get_accent_index(self):
        """
        Find position of accent and remove it
        """
        accent_index = self.word.find(self.accent_char)
        if accent_index > -1:
            self.accent_index = accent_index - 1

    def replace_soft_sings(self):
        self.word = self.word.replace("ь", "'")

    def replace_complex_vowels(self):
        """
        Replace complex vowels to equivalent characters
        """
        word = ''
        for index, char in enumerate(self.word):
            if char not in self.complex_vowels:
                word += char
                continue
            replace_char = self.complex_vowels.get(char)
            word += replace_char[1] if index - 1 >= 0 and self.word[index - 1] in self.all_consonants else replace_char[0]
        self.word = word

    def replace_complex_consonants(self):
        """
        Replace complex consonants to equivalent charsets
        """
        for complex_consonant, charsets in self.complex_consonants.items():
            self.word = self.word.replace(complex_consonant, charsets)

    def replace_double_consonants(self):
        """
        Replace double consonants to single consonants with colon
        """
        pattern = re.compile(r"(.)\1(\')?")
        match = re.search(pattern, self.word)
        if not match:
            return
        found_substring = match.group(0)
        char = match.group(1)
        apostrophe = match.group(2)
        if char not in self.all_consonants:
            return
        new_substring = '{}\':'.format(char) if apostrophe else '{}:'.format(char)
        self.word = self.word.replace(found_substring, new_substring)

    def replace_asyllabics_chars(self):
        """
        Find and replace asyllabic characters
        """
        word = self.word
        len_word = len(word) - 1
        for char, replace_char in self.asyllabics.items():
            matches = re.finditer(char, word)
            for match in matches:
                if match.start() == 0 and word[1] in self.all_consonants:
                    word = replace_char + word[1:]
                if match.start() == len_word and word[-2] in self.all_vowels:
                    word = word[:-1] + replace_char
                if 0 < match.start() < len_word and word[match.start() - 1] in self.all_vowels and word[match.start() + 1] in self.all_consonants:
                    word = word[:match.start()] + replace_char + word[match.start()+1:]
        self.word = word


class Transcriptor(Characters):

    def __init__(self, word, accent_index):
        self.word = word
        self.accent_index = accent_index
        self.transcription = word
        self.chars = []
        self.clearly_chars = []
        self.syllables = []
        self.grouped_syllables = []
        self.groups = []

        self.transcript()

    def transcript(self):
        self.remove_apostrophe()
        self.split_chars()
        self.make_mask_word()
        self.split_syllable()

        self.replace_unaccented_vowels()

        self.make_groups_by_rules()
        self.assort_characters_using_mask()

    def remove_apostrophe(self):
        """
        Remove apostrophe
        """
        self.transcription = self.transcription.replace('’', '')

    def split_chars(self):
        """
        Split transcription on phonetic sounds
        """
        chars = []
        iter_tr = iter(self.transcription)
        for char in iter_tr:
            if char in {"'", ':', self.accent_char}:
                chars[-1] += char
            elif char == self.breve_char:
                chars[-1] += char + next(iter_tr)
            else:
                chars.append(char)
        self.chars = chars
        self.clearly_chars = list(map(lambda ch: ch.replace(':', '').replace("'", '').replace(self.accent_char, ''), self.chars))

    def make_mask_word(self):
        """
        Make mask of word using typical characters groups
        """
        syllables = []
        for index, char in enumerate(self.clearly_chars):
            if char == 'й':
                type_char = self.get_type_of_char_for_j(index)
                syllables.append(type_char)
            elif char in self.consonants_sonorant:
                syllables.append(self.C_SONORANT)
            elif char in self.consonants_voicing:
                syllables.append(self.C_VOICING)
            elif char in self.consonants_voicelessness:
                syllables.append(self.C_VOICELESSNESS)
            elif char in self.all_vowels:
                syllables.append(self.VOWEL)
            elif char in self.asyllabics.values():
                syllables.append(self.ASYLLABIC_CHAR)
        self.syllables = syllables

    def get_type_of_char_for_j(self, index):
        """
        Get type of chat й witch depend on a position in word and adjacent characters
        :param index: int
        """
        if index == 0:
            if self.clearly_chars[1] in self.all_consonants:
                char = self.ASYLLABIC_CHAR
            else:
                char = self.C_SONORANT
        elif index == len(self.clearly_chars) - 1:
            return self.ASYLLABIC_CHAR
        elif self.clearly_chars[index - 1] in self.all_vowels:
            if index + 1 < len(self.clearly_chars) and self.clearly_chars[index + 1] not in self.all_vowels:
                char = self.ASYLLABIC_CHAR
            else:
                char = self.C_SONORANT
        else:
            char = self.C_SONORANT
        return char

    def split_syllable(self):
        """

        :return:
        """
        syllables = []
        new_syllable = ''
        for char in self.syllables:
            if char not in {self.ASYLLABIC_CHAR, self.VOWEL}:
                new_syllable += char
                continue
            if new_syllable:
                syllables.append(new_syllable)
                new_syllable = ''
            syllables.append(char)
        if new_syllable:
            syllables.append(new_syllable)
        self.syllables = syllables

    def replace_unaccented_vowels(self):
        """

        :return:
        """
        if self.accent_index is False:
            return
        replacing_chars = []
        for index, char in enumerate(self.chars):
            if char in self.unaccented_vowels and index != self.accent_index:
                # Голосний [о], тільки в одному випадку у вимові виближається до [у], коли в наступному складі  [у] стоїть під наголосом [коужух], [зоузул'а].
                if char == 'о':
                    if self.chars[self.accent_index] == 'у'+self.accent_char:
                        replacing_chars.append(self.unaccented_vowels.get(char))
                    else:
                        replacing_chars.append(char)
                else:
                    replacing_chars.append(self.unaccented_vowels.get(char))
            else:
                replacing_chars.append(char)
        self.chars = replacing_chars

    def make_groups_by_rules(self):
        """
        Assort characters using special rules
        """
        if self.syllables.count(self.VOWEL) == 1:
            self.assort_for_one_syllable_word()
        else:
            self.assort_for_multiple_syllable_word()

    def assort_characters_using_mask(self):
        """
        Assort characters using mask for splitting list of characters on syllables
        """
        chars = self.chars
        grouped_syllables = []
        for group in self.groups:
            index = len(group)
            grouped_syllables.append(chars[:index])
            chars = chars[index:]
        self.grouped_syllables = grouped_syllables

    def assort_for_one_syllable_word(self):
        """

        :return:
        """
        groups = []
        for chars in self.syllables:
            groups.extend(list(chars))
        self.groups = [groups]

    def assort_for_multiple_syllable_word(self):
        """

        :return:
        """
        groups = []
        next_syl = []
        len_syllables = len(self.syllables)
        for index, piece in enumerate(self.syllables):
            if piece in {'1', '2', '3'}:
                if index == len_syllables - 1:
                    groups[-1].append(piece)
                else:
                    next_syl.append(piece)
            elif piece in {'22', '21', '33', '32', }:
                next_syl.extend(list(piece))
            elif piece in {'12', '13', '23', '31', }:
                if 1 < index:
                    groups[-1].append(piece[0])
                    next_syl.extend(list(piece[1:]))
                else:
                    next_syl.extend(list(piece))
            elif piece in {'11', }:
                if 1 < index:
                    groups[-1].append(piece[0])
                    next_syl.extend(list(piece[1:]))
                else:
                    next_syl.extend(list(piece))
            elif piece in {'222', '333', '232', '323', '231', '321', '221', '331'}:
                next_syl.extend(list(piece))
            elif piece in {'131', '121', '231', '133', '233'} and index != 0:
                groups[-1].append(piece[0])
                next_syl.extend(list(piece[1:]))
            elif piece in {'1331', '2331', '1231', '1321', '3331', '3333'} and index != 0:
                groups[-1].append(piece[0])
                next_syl.extend(list(piece[1:]))
            elif piece == self.ASYLLABIC_CHAR:
                if len(groups) > 0:
                    groups[-1].append(piece)
                else:
                    next_syl.append(piece)
            elif piece == self.VOWEL:
                next_syl.append(piece)
                groups.append(next_syl)
                next_syl = []
        if next_syl.count(self.VOWEL) > 0:
            groups.append(next_syl)
        else:
            groups[-1].extend(next_syl)
        self.groups = groups

    def get_string_transcription(self):
        return '[{}]'.format('|'.join(map(lambda l: ''.join(l), self.grouped_syllables)))


class TranscriptionWord:
    """
    TranscriptionWord class
    """

    def __init__(self, word, assimilated=False):
        self.original_word = word
        self.assimilated = assimilated

        formatter_word = FormatterWord(word)

        self.word = formatter_word.word
        self.accent_index = formatter_word.accent_index

        self.transcriptions = []

        self.transcript()

    def transcript(self):

        if self.assimilated:
            words = assimilate(self.word)
        else:
            words = self.word,

        for word in words:
            transcriptor = Transcriptor(word, self.accent_index)
            self.transcriptions.append(transcriptor)

    def get_transcription(self):
        return [t.get_string_transcription() for t in self.transcriptions]
