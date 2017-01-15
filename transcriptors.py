"""
    Transcriptor module
"""
import re


class Charsets:
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
        'о': u"о\u02B8"
    }


class Transcriptor(Charsets):
    """
    Transcriptor class
    """

    def __init__(self, word):
        self.original_word = word
        self.word = word
        self.accent_index = False
        self.transcription = ''
        self.chars = []
        self.clearly_chars = []
        self.syllables = []
        self.grouped_syllables = []
        self.groups = []

        self.transcript()

    def transcript(self):
        self.get_accent_index()
        self.replace_soft_sings()
        self.replace_complex_vowels()
        self.replace_complex_consonants()
        self.replace_double_consonants()
        self.replace_asyllabics_chars()
        self.remove_apostrophe()

        self.split_chars()
        self.make_mask_word()
        self.split_syllable()

        self.replace_unaccented_vowels()

        self.make_groups_by_rules()
        self.assort_characters_using_mask()

    def get_accent_index(self):
        """
        Find position of accent and remove it
        """
        accent_index = self.word.find('\N{COMBINING ACUTE ACCENT}')
        if accent_index > -1:
            self.accent_index = accent_index - 1
            self.word = self.word.replace('\N{COMBINING ACUTE ACCENT}', '')

    def replace_soft_sings(self):
        """
        Replace soft sing to singe quotes
        """
        self.word = self.word.replace("ь", "'")

    def replace_complex_vowels(self):
        """
        Replace complex vowels to equivalent characters
        """
        transcription = ''
        for index, char in enumerate(self.word):
            if char not in self.complex_vowels:
                transcription += char
                continue
            replace_char = self.complex_vowels.get(char)
            transcription += replace_char[1] if index - 1 >= 0 and self.word[index - 1] in self.all_consonants else replace_char[0]
        self.transcription = transcription

    def replace_complex_consonants(self):
        """
        Replace complex consonants to equivalent charsets
        """
        for complex_consonant, charsets in self.complex_consonants.items():
            self.transcription = self.transcription.replace(complex_consonant, charsets)

    def replace_double_consonants(self):
        """
        Replace double consonants to single consonants with colon
        """
        pattern = re.compile(r"(.)\1(\')?")
        match = re.search(pattern, self.transcription)
        if not match:
            return
        found_substring = match.group(0)
        char = match.group(1)
        apostrophe = match.group(2)
        if char not in self.all_consonants:
            return
        new_substring = '{}\':'.format(char) if apostrophe else '{}:'.format(char)
        self.transcription = self.transcription.replace(found_substring, new_substring)

    def replace_asyllabics_chars(self):
        """
        Find and replace asyllabic characters
        """
        transcription = self.transcription
        len_transcription = len(transcription) - 1
        for char, replace_char in self.asyllabics.items():
            matches = re.finditer(char, transcription)
            for match in matches:
                if match.start() == 0 and transcription[1] in self.all_consonants:
                    transcription = replace_char + transcription[1:]
                if match.start() == len_transcription and transcription[-2] in self.all_vowels:
                    transcription = transcription[:-1] + replace_char
                if 0 < match.start() < len_transcription and transcription[match.start() - 1] in self.all_vowels and transcription[match.start() + 1] in self.all_consonants:
                    transcription = transcription[:match.start()] + replace_char + transcription[match.start()+1:]
        self.transcription = transcription

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
            if char in {"'", ':'}:
                chars[-1] += char
            elif char == '\N{COMBINING INVERTED BREVE}':
                chars[-1] += char + next(iter_tr)
            else:
                chars.append(char)
        self.chars = chars
        self.clearly_chars = list(map(lambda ch: ch.replace(':', '').replace("'", ''), self.chars))

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
        if self.accent_index is False:
            return
        replacing_chars = []
        for index, char in enumerate(self.chars):
            if char in self.unaccented_vowels and index != self.accent_index:
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
            grouped_syllables.append(''.join(chars[:index]))
            chars = chars[index:]
        self.grouped_syllables = grouped_syllables

    def assort_for_one_syllable_word(self):
        groups = []
        for chars in self.syllables:
            groups.extend(list(chars))
        self.groups = [groups]

    def assort_for_multiple_syllable_word(self):
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
            elif piece in {'1331', '2331', '1231', '1321', '3331'} and index != 0:
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
        return '[{}]'.format('|'.join(self.grouped_syllables))
