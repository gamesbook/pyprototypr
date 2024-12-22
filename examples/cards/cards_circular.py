"""
Deck and circular Card example using list data for pyprototypr

Written by: Derek Hohls
Created on: 22 December 2024
"""
from pyprototypr import *

Create(filename='cards_circular.pdf', paper=landscape(A4))

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
Deck(cards=1, shape='circle', radius=3.15, copy='Copies')

# background color per Race
back_race = Common(x=0.35, y=0.35,radius=2.8)
back_hum = circle(common=back_race, fill_stroke=tomato)
back_elf = circle(common=back_race, fill_stroke=gold)
back_dwa = circle(common=back_race, fill_stroke=aqua)
back_hob = circle(common=back_race, fill_stroke=lime)
back_naz = circle(common=back_race, fill_stroke=grey)
Card("all", S("{{ Race == 'Human' }}", back_hum))
Card("all", S("{{ Race == 'Elf' }}", back_elf))
Card("all", S("{{ Race == 'Dwarf' }}", back_dwa))
Card("all", S("{{ Race == 'Hobbit' }}", back_hob))
Card("all", S("{{ Race == 'Nazgul' }}", back_naz))

# # character Name
name_box = rectangle(x=1.5, y=4.2, width=3.4, height=1, rounded=0.2)
Card("*", name_box)
Card("all", text(text=T("{{ Name }}"), x=3.2, y=4.5, font_size=18))

# # character Age
power = text(text=T("<i>Long-lived</i> <b>({{ Age or '\u221E' }})</b>"),  # infinity
             x=1.4, y=1.4, width=3.5, font_size=12,
             align="centre", wrap=True, fill=None)
Card("all", S("{{ Race == 'Elf' }}", power))
Card("all", S("{{ Race == 'Maia' }}", power))
Card("all", S("{{ Race == 'Nazgul' }}", power))

# no effect!
Card("all", S("{{ foo == 'Orc' }}", power))

Save()
