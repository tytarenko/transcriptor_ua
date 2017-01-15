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
