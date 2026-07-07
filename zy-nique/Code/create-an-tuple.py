accession_numbers_list = [
    "98-2716 through 98-2719",
    "98-866 through 98-886",
    "98-1023 through 98-1059",
    "98-1403 through 98-1405",
    "98-1250 through 98-1255",
    "98-1878 through 98-1885",
    "98-1091 through 98-1150",
    "98-780 through 98-802"
]

accession_numbers = [(x.split(" through ")[0], x.split(" through ")[1]) for x in accession_numbers_list]
print(accession_numbers)

