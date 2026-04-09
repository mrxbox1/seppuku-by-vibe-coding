import random as rand

print("16-character string generator")

gen_string = ""

for i in range(16):
    # codes 32-127 are printable, according to ascii-code.com
    gen_string += chr(rand.randint(32, 127))

print("Generated string:", gen_string)
