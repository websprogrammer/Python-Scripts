from typing import List

REPRESENTATIONS = {
    0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
    6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven',
    12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen',
    17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty', 30: 'thirty',
    40: 'forty', 50: 'fifty', 60: 'sixty', 70: 'seventy', 80: 'eighty', 90: 'ninety',
}

TITLES = ('', 'thousand', 'million', 'billion')


def get_chunks(number: int) -> List:
    """ Function splits the input number into small parts
    and adds a title to each block.

    :param number: input number
    :return: list of separated numbers with title
    """
    views = iter(TITLES)

    chunks = []
    block = []

    # Insert numbers from the end of the list.
    for i, char in enumerate(str(number)[::-1]):
        block.insert(0, int(char))
        if (i + 1) % 3 == 0:
            if block != [0, 0, 0]:
                chunks.insert(0, (block, next(views)))
            else:
                next(views)
            block = []

    if block:
        chunks.insert(0, (block, next(views)))

    return chunks


def handle_numbers(num: int) -> str:
    if num <= 20:
        return REPRESENTATIONS[num]
    elif num < 100:
        output = REPRESENTATIONS[(num // 10) * 10]
        if num % 10 > 0:
            output += '-' + REPRESENTATIONS[num % 10]
        return output
    else:
        output = REPRESENTATIONS[num // 100] + ' hundred'
        if num % 100 > 0:
            rest_num = num % 100
            output += f' and {handle_numbers(rest_num)}'
        return output


def wrapper(processed_string: str, title: str, prev_title: str) -> str:
    """
    :return: wrapped string with correct punctuation marks
    """
    string = processed_string

    if prev_title in TITLES[1:]:
        string = ', ' + string
    if title:
        string += ' ' + title

    return string


def get_representation(input_number: int) -> str:
    chunks = get_chunks(input_number)
    final_strings = []
    prev_title = ''

    for numbers, title in chunks:
        num = int(''.join(map(str, numbers)))

        if num == 0 and title != '':
            continue

        processed_string = handle_numbers(num)
        processed_string = wrapper(processed_string, title, prev_title)

        final_strings.append(processed_string)

        prev_title = title

    return ''.join(final_strings)


assert get_representation(0) == 'zero'
assert get_representation(3) == 'three'
assert get_representation(10) == 'ten'
assert get_representation(11) == 'eleven'
assert get_representation(19) == 'nineteen'
assert get_representation(20) == 'twenty'
assert get_representation(23) == 'twenty-three'
assert get_representation(34) == 'thirty-four'
assert get_representation(56) == 'fifty-six'
assert get_representation(80) == 'eighty'
assert get_representation(97) == 'ninety-seven'
assert get_representation(99) == 'ninety-nine'
assert get_representation(100) == 'one hundred'
assert get_representation(101) == 'one hundred and one'
assert get_representation(110) == 'one hundred and ten'
assert get_representation(117) == 'one hundred and seventeen'
assert get_representation(120) == 'one hundred and twenty'
assert get_representation(123) == 'one hundred and twenty-three'
assert get_representation(172) == 'one hundred and seventy-two'
assert get_representation(199) == 'one hundred and ninety-nine'
assert get_representation(200) == 'two hundred'
assert get_representation(201) == 'two hundred and one'
assert get_representation(211) == 'two hundred and eleven'
assert get_representation(223) == 'two hundred and twenty-three'
assert get_representation(376) == 'three hundred and seventy-six'
assert get_representation(767) == 'seven hundred and sixty-seven'
assert get_representation(982) == 'nine hundred and eighty-two'
assert get_representation(999) == 'nine hundred and ninety-nine'
assert get_representation(1000) == 'one thousand'
assert get_representation(1001) == 'one thousand, one'
assert get_representation(1017) == 'one thousand, seventeen'
assert get_representation(1023) == 'one thousand, twenty-three'
assert get_representation(1088) == 'one thousand, eighty-eight'
assert get_representation(1100) == 'one thousand, one hundred'
assert get_representation(1109) == 'one thousand, one hundred and nine'
assert get_representation(1139) == 'one thousand, one hundred and thirty-nine'
assert get_representation(1239) == 'one thousand, two hundred and thirty-nine'
assert get_representation(1433) == 'one thousand, four hundred and thirty-three'
assert get_representation(2000) == 'two thousand'
assert get_representation(2010) == 'two thousand, ten'
assert get_representation(7891) == 'seven thousand, eight hundred and ninety-one'
assert get_representation(89321) == 'eighty-nine thousand, three hundred and twenty-one'
assert get_representation(999999) == 'nine hundred and ninety-nine thousand, nine hundred and ninety-nine'
assert get_representation(1000000) == 'one million'
assert get_representation(2000000) == 'two million'
assert get_representation(2000000000) == 'two billion'
assert get_representation(1234567891) == 'one billion, two hundred and thirty-four million, five hundred and sixty-seven thousand, eight hundred and ninety-one'
