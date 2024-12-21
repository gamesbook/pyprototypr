"""
Deck and Card example using list data for pyprototypr

Written by: Derek Hohls
Created on: 21 December 2024
"""
from pyprototypr import *

Create(filename='cards_lotr.pdf')

# deck data
lotr = [
    ['ID', 'Name', 'Age', 'Race'],
    [1, "Gimli", 140, "Dwarf"],
    [2, "Legolas", 656, "Elf"],
    [3, "Aragorn", 88, "Human"],
    [4, "Frodo", 51, "Hobbit"],
    [5, "Pippin", 29, "Hobbit"],
    [6, "Merry", 37, "Hobbit"],
    [7, "Samwise", 39, "Hobbit"],
    [8, "Boromir", 41, "Human"],
    [9, "Gandalf", None, "Maia"],
]
Data(data_list=lotr)

# design the deck
Deck(cards=1, skip="{{ Race == 'Hobbit' }}")
# Deck(cards=9) # uncomment this line to show all cards

# background color per Race
back_race = Common(x=0.5, y=0.5, width=5.3, height=7.9, rounded=0.2)
back_hum = rectangle(common=back_race, fill_stroke=tomato)
back_elf = rectangle(common=back_race, fill_stroke=gold)
back_dwa = rectangle(common=back_race, fill_stroke=aqua)
back_hob = rectangle(common=back_race, fill_stroke=lime)
Card("all", S("{{ Race == 'Human' }}", back_hum))
Card("all", S("{{ Race == 'Elf' }}", back_elf))
Card("all", S("{{ Race == 'Dwarf' }}", back_dwa))
Card("all", S("{{ Race == 'Hobbit' }}", back_hob))

# character Name
name_box = rectangle(x=0.5, y=7.0, width=5.3, height=1.5, rounded=0.2)
Card("*", name_box)
Card("all", text(text=T("{{ Name }}"), x=3.3, y=7.5, font_size=18))

# character Age
power = text(text=T("<i>Long-lived</i> <b>({{ Age or '\u221E' }})</b>"),  # infinity
             x=0.5, y=1.2, width=5, font_size=18,
             align="centre", wrap=True, fill=None)
Card("all", S("{{ Race == 'Elf' }}", power))
Card("all", S("{{ Race == 'Maia' }}", power))

# no effect!
Card("all", S("{{ foo == 'Orc' }}", power))

Save()
