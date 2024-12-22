"""
Deck and hexagonal Card example using list data for pyprototypr

Written by: Derek Hohls
Created on: 21 December 2024
"""
from pyprototypr import *

Create(filename='cards_hexagonal.pdf', paper=landscape(A4))

# deck data
lotr = [
    ['ID', 'Name', 'Age', 'Race', 'Copies'],
    [1, "Gimli", 140, "Dwarf", 1],
    [2, "Legolas", 656, "Elf", 1],
    [3, "Aragorn", 88, "Human", 1],
    [4, "Frodo", 51, "Hobbit", 1],
    [5, "Pippin", 29, "Hobbit", 1],
    [6, "Merry", 37, "Hobbit", 1],
    [7, "Samwise", 39, "Hobbit", 1],
    [8, "Boromir", 41, "Human", 1],
    [9, "Gandalf", None, "Maia", 1],
    [10, "RingWraith", 4300, "Nazgul", 9],
]
Data(data_list=lotr)

# design deck
Deck(cards=6, shape='hexagon', copy='Copies', height=6.3)

# background color per Race
back_race = Common(x=0.45, y=0.35, height=5.6)
back_hum = hexagon(common=back_race, fill_stroke=tomato)
back_elf = hexagon(common=back_race, fill_stroke=gold)
back_dwa = hexagon(common=back_race, fill_stroke=aqua)
back_hob = hexagon(common=back_race, fill_stroke=lime)
back_naz = hexagon(common=back_race, fill_stroke=grey)
Card("all", S("{{ Race == 'Human' }}", back_hum))
Card("all", S("{{ Race == 'Elf' }}", back_elf))
Card("all", S("{{ Race == 'Dwarf' }}", back_dwa))
Card("all", S("{{ Race == 'Hobbit' }}", back_hob))
Card("all", S("{{ Race == 'Nazgul' }}", back_naz))

# # character Name
name_box = rectangle(x=2, y=4.5, width=3.2, height=1.25, rounded=0.2)
Card("*", name_box)
Card("all", text(text=T("{{ Name }}"), x=3.6, y=4.8, font_size=18))

# # character Age
power = text(text=T("<i>Long-lived</i> <b>({{ Age or '\u221E' }})</b>"),  # infinity
             x=1.9, y=1., width=3.5, font_size=12,
             align="centre", wrap=True, fill=None)
Card("all", S("{{ Race == 'Elf' }}", power))
Card("all", S("{{ Race == 'Maia' }}", power))
Card("all", S("{{ Race == 'Nazgul' }}", power))

# # no effect!
Card("all", S("{{ foo == 'Orc' }}", power))

Save()
