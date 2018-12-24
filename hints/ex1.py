import pandas as pd

#inputs
usa = {"car": "Ford", "food":"Hot-Dog", "president": "Trump"}
france = {"car": "Peugeot", "food":"Fois-Gra", "president": "Makaroon"}
russia = {"car": "GAZ", "food":"Borshch", "president": "Putin"}

#list of dicts as an input in DataFrame. Result: each item becomes a row
df = pd.DataFrame([usa, france, russia])
df.index = list(('usa', 'france', 'russia'))

#dict of dicts as an input in DataFrame. Result: each item becomes a column
dict1 = dict(usa = usa, france = france, russia = russia)
fd = pd.DataFrame(dict1)