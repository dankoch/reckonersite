'''
Created on Oct 1, 2011
@author: danko
'''
from decimal import *

def computeReckoningAnswerPercentages(reckoning):
    totalVotes = 0

    if (reckoning):
        for answer in reckoning.answers:
            totalVotes += int(answer.vote_total)
        for answer in reckoning.answers:
            answer.percentage = str(computePercentage(answer.vote_total, totalVotes, 1))

    return reckoning


def computePercentage(dividend, divisor, places=1, label='%', dp='.', neg='-', pos=''):
    """Computes a percentage and returns as a formatted string.

    dividend: numerator in percentage calculation
    divisor: denominator in percentage calculation
    places:  required number of places after the decimal point
    label:   optional symbol after the percentage (may be blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank """
       
    if (Decimal(divisor) == Decimal(0)):
        percentage_val = Decimal(0)
    else:
        percentage_val = (Decimal(dividend) * Decimal(100)) / Decimal(divisor)
       
    q = Decimal(10) ** -places      # 1 places --> '0.1'
    sign, digits, exp = percentage_val.quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if (label):
        build(label)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    while digits:
        build(next())
    build(neg if sign else pos)
    
    return ''.join(reversed(result))

