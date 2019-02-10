from io import open

plik = open("codes.txt", "w")

c1 = chr(ord('a') - 1)

for i in range(0, 16):
    if c1 == 'f':
        c1 = chr(ord('0') - 1)
    c1 = chr(ord(c1) + 1)
    c2 = chr(ord('a') - 1)

    for j in range(0, 16):
        if c2 == 'f':
            c2 = chr(ord('0') - 1)
        c2 = chr(ord(c2) + 1)
        c3 = chr(ord('a') - 1)

        for k in range(0, 16):
            if c3 == 'f':
                c3 = chr(ord('0') - 1)
            c3 = chr(ord(c3) + 1)
            c4 = 'a'

            for l in range(0, 16):
                new_str = c1 + c2 + c3 + c4
                print(new_str)
                plik.write(new_str + '\n')
                if c4 == 'f':
                    c4 = chr(ord('0') - 1)
                c4 = chr(ord(c4) + 1)
