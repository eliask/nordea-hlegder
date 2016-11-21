#!/usr/bin/env python3

from decimal import Decimal
import csv
import fileinput
import sys

KNOWN_FIRST_HEADER_COLUMNS = ('Kirjauspäivä', 'Entry date')

HEADER = '''Entry date|Value date|Payment date|Amount|Beneficiary/Remitter|Account number|BIC|Transaction|Reference number|Originator's reference|Message|Card number|Receipt|'''.split('|')
assert len(HEADER) == 14, len(HEADER)
IDX_AMOUNT = HEADER.index('Amount')

writer = csv.writer(sys.stdout)
header_written = False

reader = csv.reader(
    fileinput.input(),
    quoting=csv.QUOTE_NONE,
    delimiter='\t',
)

def read_row_col(idx, value):
    if idx == IDX_AMOUNT:
        # Validate the amount
        return Decimal(value.replace(',', '.'))

    elif value.count('"') % 2 == 1:
        # Mismatched quote marks screw up syntax highlighting for hledger.
        return '{}"'.format(value.strip())

    else:
        return value.strip()

for row in reader:
    if len(row) == 2:
        # Account number line
        continue

    elif len(row) == 0:
        # Empty line since the file has CRLF, LF line endings...
        continue

    assert len(row) == len(HEADER), row

    if row[0] in KNOWN_FIRST_HEADER_COLUMNS:
        if not header_written:
            header_written = True
            writer.writerow(row)
        continue

    writer.writerow(read_row_col(i,v) for i,v in enumerate(row))
