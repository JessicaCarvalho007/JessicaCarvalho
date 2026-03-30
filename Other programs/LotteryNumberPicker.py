from numpy.random import randint as r_int


def mega_millions():
    tickets = list()
    for ticket in range(5):
        numbers = list()
        for pick in range(5):
            num = r_int(1, 71, dtype='int32')
            while num in numbers:
                num = r_int(1, 71, dtype='int32')
            numbers.append(num)
        tickets.append(sorted(numbers))

    for i, ticket in enumerate(sorted(tickets), 1):
        ticket.append(r_int(1, 26, dtype='int32'))
        print(f"Ticket #{i:<2} picks are:  {', '.join(list(map(lambda x: f'{str(x):>2}', ticket)))}\n{'-' * 45}")


def power_ball():
    tickets = list()
    for ticket in range(5):
        numbers = list()
        for pick in range(5):
            num = r_int(1, 70, dtype='int32')
            while num in numbers:
                num = r_int(1, 71, dtype='int32')
            numbers.append(num)
        tickets.append(sorted(numbers))

    for i, ticket in enumerate(sorted(tickets), 1):
        ticket.append(r_int(1, 27, dtype='int32'))
        print(f"Ticket #{i:<2} picks are:  {', '.join(list(map(lambda x: f'{str(x):>2}', ticket)))}\n{'-' * 45}")


print(f'\n{"*"*53}\n* Getting the Mega Millions lottery numbers for you *\n{"*"*53}\n')
mega_millions()
print(f'\n\n{"*"*53}\n* Getting the Power Ball lottery numbers for you *\n{"*"*53}\n')
power_ball()
