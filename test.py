def hashPassword(password):
    hashedPassword = 0

    randomPrimeList1 = [17,71,43,41,37,73,19,97,67,29]
    randomPrimeList2 = [79,17,61,51,37,41,73,67,73,59]
    randomLargePrimeNumber = 87654219371

    for i in range(len(password)):
        hashedPassword = (hashedPassword * randomPrimeList1[i%len(randomPrimeList1)] + ord(password[i])*randomPrimeList2[i%len(randomPrimeList1)]) % randomLargePrimeNumber

    return hashedPassword

print(hashPassword("12345678"))