accession_numbers = [
    ("98-2716", "98-2719"),
    ("98-866", "98-886"),
    ("98-1023", "98-1059"),
    ("98-1403", "98-1405"),
    ("98-1250", "98-1255"),
    ("98-1878", "98-1885"),
    ("98-1091", "98-1150"),
    ("98-780", "98-802")
]

for accession_number in accession_numbers:
    prefix = accession_number[0].split("-")[0]
    start, end = [int(x.split("-")[1]) for x in accession_number]
    if end<1000:
        accession_numbers_range = [f"{prefix}-{str(x)}" for x in range(start+1, end)]
    else:
        accession_numbers_range = [f"{prefix}-{str(x).zfill(4)}" for x in range(start+1, end)]
    print(accession_numbers_range)

