with open('hangman_data.txt') as file:
    lines = file.readlines()

    for line in lines:
        temp = line.split(',')
        for word in temp:
            if word == '\n':
                continue
            else:
                print(f"'{word.strip()}', ", end='')
