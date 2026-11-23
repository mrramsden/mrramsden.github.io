PREDICT = {
 "h1": {"code": 'hero = {"name": "Ash", "gold": 20, "health": 100}\nprint(hero["gold"])',
        "q": "What will this print?", "o": ["Ash", "20", "gold", "100"], "a": 1,
        "e": "The key \"gold\" finds the value stored with it, which is 20. It doesn't matter where gold sits in the dictionary."},
 "h2": {"code": 'hero = {"health": 100}\nhero["helth"] = 60\nprint(hero["health"])',
        "q": "What will this print?", "o": ["60", "100", "An error", "helth"], "a": 1,
        "e": "The key is spelt helth, so Python adds a new key instead of changing the health. The health is still 100. Print the whole hero to see both keys."},
 "h3": {"code": 'def heal(hero):\n    hero["health"] = hero["health"] + 20\n\nhero = {"health": 50}\nhero = heal(hero)\nprint(hero)',
        "q": "What will this print?", "o": ["{'health': 70}", "{'health': 50}", "None", "An error"], "a": 2,
        "e": "heal has no return, so it sends back None. hero = heal(hero) then stores None in hero. That's why every room ends with return hero."},
}
