#!/usr/bin/python

"""Washington State License/ID Card Encoder/Decoder
Washington State licenses (and ID) numbers are encoded from Name & Birthdate in the format: LLLLLFMYYxMD
(L=LastName, F=FirstInitial, M=MiddleInitial, YY=100-BirthYear, M=MonthCode, D=DayCode, x=Checksum)
There is a primary encoding, and in the case of an ID collision a secondary encoding (aka twins with similar names).
So far it appears that since the index position of the two options maps the same in the checksum
both options for the license number will differ by the month character only (having the same checksum).

Based upon information from: http://www.dogberrypatch.com/archives/washington-driver-license-numbers-decoded/
"""

import re
import itertools
from datetime import *

monthcode = [[],['','B','C','D','J','K','L','M','N','O','P','Q','R'],['','S','T','U','1','2','3','4','5','6','7','8','9']]

daycode = ['','A','B','C','D','E','F','G','H','Z','S','J','K','L','M','N','W',
       'P','Q','R','0','1','2','3','4','5','6','7','8','9','T','U']

checksum = ['','AJ','BKS','CLT','DMU*','ENV','FOW','GPX','HQY','IRZ']

def encodeLicense(firstName, lastName, middleInit, birthday, licOption):
    birthday = birthday.split("/")

    if len(lastName) < 5:
        while len(lastName) < 5:
            lastName = lastName + '*'

    lastName = lastName[0:5].upper()

    if not len(middleInit) > 0:
        middleInit = '*'
    else:
        middleInit = middleInit[0].upper()

    firstName = firstName[0].upper()

    licMonth = int(birthday[0])
    licDay = int(birthday[1])
    licYear = str(100 - int(birthday[2]))

    license = lastName + firstName + middleInit + licYear + monthcode[licOption][licMonth] + daycode[licDay]

    def licChecksum(license):
        x = 0
        toggle = itertools.cycle((1, -1))

        for letter in license:
            if re.search('\d', letter):
                x = x + (int(letter) * toggle.next())
            elif re.search('\*', letter):
                for group in checksum:
                    if re.search('\*', group):
                        x = x + ((checksum.index(group)*toggle.next()))
            else:
                for group in checksum:
                    if re.search(letter, group):
                        x = x + ((checksum.index(group)*toggle.next()))

        return str(x % 10)

    license = license[:9] + licChecksum(license) + license[9:]
    return license


def decodeLicense(license, licOption):
    bDay = daycode.index(license[-1:])
    bMonth = monthcode[licOption].index(license[-2:-1])
    bYear = 100 - int(license[-5:-3])

    dob = str(bMonth) + "/" + str(bDay) + "/" + date.strftime(datetime.strptime(str(bYear), "%y"), "%Y")
    lName = license[:5].strip('*')
    fName = license[5:6]
    mName = license[6:7].strip('*')

    return [lName, fName, mName, dob]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Encode or Decode Washington State License/ID Number', version='%(prog)s 0.9')
    subparsers = parser.add_subparsers(help='Encode/Decode', dest='operation')

    encode_parser = subparsers.add_parser('E', description='Encode License')
    coding = encode_parser.add_mutually_exclusive_group()
    coding.add_argument('-C', choices=[1,2], default='1', dest='licOption', type=int, help='Primary Encoding')
    encode_parser.add_argument('-F', dest='firstName', help='First Name')
    encode_parser.add_argument('-L', dest='lastName', help='Last Name or Initial')
    encode_parser.add_argument('-M', dest='middleInit', default='', help='Middle Name or Initial')
    encode_parser.add_argument('-B', dest='birthday', required=True, help='Birthday in m/d/yy format')

    decode_parser = subparsers.add_parser('D', description='Decode License')
    coding = decode_parser.add_mutually_exclusive_group()
    coding.add_argument('-C', choices=[1,2], default='1', dest='licOption', type=int, help='Primary Encoding')
    decode_parser.add_argument('-L', dest='license', required=True, help='License Number to Decode')

    args = parser.parse_args()

    if args.operation == 'E':
        print encodeLicense(args.firstName, args.lastName, args.middleInit, args.birthday, args.licOption)

    if args.operation == 'D':
        print decodeLicense(args.license, args.licOption)