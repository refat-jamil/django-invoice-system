# invoices/utils.py

def amount_to_words(amount):
    ones = [
        '', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
        'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen',
        'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'
    ]
    tens = [
        '', '', 'Twenty', 'Thirty', 'Forty', 'Fifty',
        'Sixty', 'Seventy', 'Eighty', 'Ninety'
    ]

    def below_thousand(n):
        if n == 0:
            return ''
        elif n < 20:
            return ones[n]
        elif n < 100:
            return tens[n // 10] + ((' ' + ones[n % 10]) if n % 10 != 0 else '')
        else:
            rest = below_thousand(n % 100)
            return ones[n // 100] + ' Hundred' + ((' and ' + rest) if rest else '')

    amount    = float(amount)
    integer   = int(amount)
    paisa     = round((amount - integer) * 100)

    if integer == 0:
        words = 'Zero'
    elif integer < 1000:
        words = below_thousand(integer)
    elif integer < 100000:
        words = below_thousand(integer // 1000) + ' Thousand'
        if integer % 1000:
            words += ' ' + below_thousand(integer % 1000)
    elif integer < 10000000:
        words = below_thousand(integer // 100000) + ' Lakh'
        integer %= 100000
        if integer >= 1000:
            words += ' ' + below_thousand(integer // 1000) + ' Thousand'
            integer %= 1000
        if integer:
            words += ' ' + below_thousand(integer)
    else:
        words = below_thousand(integer // 10000000) + ' Crore'
        integer %= 10000000
        if integer >= 100000:
            words += ' ' + below_thousand(integer // 100000) + ' Lakh'
            integer %= 100000
        if integer >= 1000:
            words += ' ' + below_thousand(integer // 1000) + ' Thousand'
            integer %= 1000
        if integer:
            words += ' ' + below_thousand(integer)

    result = words + ' Taka'
    if paisa > 0:
        result += ' and ' + below_thousand(paisa) + ' Paisa'
    result += ' Only'

    return result