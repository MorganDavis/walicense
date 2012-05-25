##Washington State License/ID Card Encoder/Decoder Script/Module

Washington State licenses (and ID) numbers are not random, rather encoded from Name & Birthdate in the following format:

LLLLLFMYYxMD

(L=LastName, F=FirstInitial, M=MiddleInitial, YY=100-BirthYear, M=MonthCode, D=DayCode, x=Checksum)

There is a primary encoding, and in the case of an ID collision, a secondary encoding (aka twins with similar names).
So far it appears that since the index position of the two options maps the same in the checksum both options for the license number will differ by the month character only (having the same checksum).

This is based upon information from: http://www.dogberrypatch.com/archives/washington-driver-license-numbers-decoded/

You can check the status of a calculated license at: https://fortress.wa.gov/dol/dolprod/dsdDriverStatusDisplay/