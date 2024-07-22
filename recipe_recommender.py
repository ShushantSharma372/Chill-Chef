import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import ast

american_ingredients = [
    'beef', 'pork', 'chicken', 'bacon', 'potato', 'corn', 'tomato', 'onion',
    'garlic', 'bell pepper', 'cheddar cheese', 'mayonnaise', 'mustard',
    'ketchup', 'pickles', 'barbecue sauce', 'maple syrup', 'apple', 'blueberry',
    'pecan', 'peanut butter', 'pumpkin', 'cranberry', 'molasses', 'cinnamon',
    'vanilla', 'bourbon', 'beer', 'whiskey', 'coffee', 'bread', 'butter', 'egg',
    'pancake', 'lettuce', 'spinach', 'mushroom', 'green bean', 'zucchini',
    'squash', 'honey', 'walnut', 'almond', 'oat', 'cranberry', 'lemon', 'lime',
    'orange', 'grapefruit'
]

chinese_ingredients = [
    'soy sauce', 'ginger', 'garlic', 'rice vinegar', 'sesame oil', 'hoisin sauce',
    'oyster sauce', 'star anise', 'five-spice powder', 'shaoxing wine', 'spring onion',
    'bean sprouts', 'shiitake mushroom', 'bok choy', 'pak choi', 'water chestnut',
    'bamboo shoots', 'tofu', 'egg noodles', 'rice noodles', 'wonton wrappers', 'chinese cabbage',
    'chili paste', 'black bean sauce', 'chinese sausage', 'dried shrimp', 'fermented black beans',
    'white pepper', 'dark soy sauce', 'sesame seeds', 'chinese parsley', 'cilantro', 'chinese broccoli',
    'japanese eggplant', 'sichuan pepper', 'chinese mustard greens', 'snow peas', 'lotus root',
    'chinese red vinegar', 'chinese black vinegar', 'chinese white vinegar', 'chinese rice wine vinegar',
    'chinese cooking wine', 'chinese rock sugar', 'maltose', 'douhua', 'xiangchun',
    'jiang', 'yuba'
]

continental_ingredients = [
    'olive oil', 'butter', 'cream', 'parmesan cheese', 'mozzarella', 'prosciutto', 'salami',
    'parma ham', 'anchovies', 'balsamic vinegar', 'arborio rice', 'basmati rice', 'risotto rice',
    'penne', 'spaghetti', 'tagliatelle', 'lasagna sheets', 'gnocchi', 'artichoke', 'asparagus',
    'bell pepper', 'caper', 'mushroom', 'rosemary', 'thyme', 'oregano', 'basil', 'sage', 'bay leaf',
    'nutmeg', 'garlic', 'shallot', 'onion', 'tomato', 'zucchini', 'eggplant', 'bell pepper',
    'rocket', 'spinach', 'radicchio', 'endive', 'chicory', 'rucola', 'rucoli', 'radicchios',
    'valerianella', 'pumpkin', 'squash', 'beetroot', 'aubergine'
]

french_ingredients = [
    'butter', 'cream', 'wine', 'champagne', 'cognac', 'calvados', 'truffle', 'foie gras',
    'croissant', 'baguette', 'brie', 'camembert', 'roquefort', 'chevre', 'raclette', 'gruyere',
    'comte', 'emmental', 'lavender', 'thyme', 'rosemary', 'tarragon', 'parsley', 'chervil',
    'shallot', 'garlic', 'onion', 'potato', 'leek', 'carrot', 'celery', 'chervil',
    'lentil', 'beans', 'courgette', 'zucchini', 'aubergine', 'bell pepper', 'beetroot', 'radish',
    'mushroom', 'asparagus', 'artichoke', 'cucumber', 'squash', 'pumpkin', 'shallots', 'herbes', 'chicory',
    'rucola', 'rucoli'
]

greek_ingredients = [
    'olive oil', 'feta cheese', 'olive', 'yogurt', 'honey', 'oregano', 'thyme', 'rosemary',
    'mint', 'dill', 'garlic', 'onion', 'lemon', 'spinach', 'cucumber', 'tomato', 'eggplant',
    'zucchini', 'bell pepper', 'fennel', 'artichoke', 'lamb', 'pork', 'chicken', 'octopus',
    'squid', 'shrimp', 'anchovy', 'sardine', 'rice', 'pasta', 'bread', 'phyllo dough',
    'almond', 'walnut', 'pistachio', 'fig', 'date', 'grape', 'pomegranate', 'watermelon', 'melon',
    'orange', 'apricot', 'peach', 'plum', 'cherry', 'apple', 'pear'
]

indian_ingredients = [
    'ghee', 'paneer', 'coconut', 'curry leaves', 'mustard seeds', 'cumin', 'coriander',
    'turmeric', 'chili powder', 'garam masala', 'cardamom', 'cinnamon', 'cloves', 'fenugreek',
    'asafoetida', 'tamarind', 'coconut milk', 'cashew nuts', 'almonds', 'pistachios',
    'raisins', 'saffron', 'basmati rice', 'chickpeas', 'lentils', 'kidney beans', 'black lentils',
    'green peas', 'potato', 'cauliflower', 'okra', 'spinach', 'eggplant', 'tomato', 'onion',
    'garlic', 'ginger', 'green chili', 'yogurt', 'paneer', 'chicken', 'lamb', 'fish', 'prawn',
    'mango', 'banana', 'papaya', 'guava', 'fig', 'dates'
]

indonesian_ingredients = [
    'coconut milk', 'lemongrass', 'galangal', 'turmeric', 'ginger', 'kaffir lime leaves',
    'candlenut', 'shallot', 'garlic', 'chili', 'terasi', 'palm sugar', 'tamarind',
    'lime', 'banana leaf', 'pandan leaf', 'rice', 'noodles', 'tofu', 'tempeh', 'soy sauce',
    'shrimp paste', 'coriander', 'cumin', 'nutmeg', 'cloves', 'cardamom', 'cinnamon',
    'lemongrass', 'basil', 'lime leaves', 'chili peppers', 'coconut oil', 'coconut sugar',
    'galangal', 'chicken', 'beef', 'pork', 'seafood', 'rice', 'vegetables', 'chicken',
    'fried shallots', 'fried garlic', 'turmeric', 'wheat', 'rice vinegar', 'rice flour',
    'rice flour', 'palm sugar', 'coconut sugar'
]

italian_ingredients = [
    'olive oil', 'garlic', 'tomato', 'basil', 'oregano', 'parsley', 'thyme', 'rosemary',
    'sage', 'bay leaf', 'mozzarella', 'parmesan', 'ricotta', 'provolone', 'gorgonzola',
    'pecorino', 'fontina', 'gnocchi', 'risotto', 'polenta', 'lasagna', 'tagliatelle',
    'spaghetti', 'penne', 'cannelloni', 'calamari', 'shrimp', 'clam', 'mussel', 'anchovy',
    'octopus', 'veal', 'beef', 'pork', 'chicken', 'rabbit', 'sausage', 'pancetta', 'prosciutto',
    'mortadella', 'salami', 'capicola', 'bresaola', 'truffle', 'fennel', 'artichoke', 'zucchini',
    'eggplant', 'bell pepper', 'mushroom', 'rocket', 'spinach'
]

japanese_ingredients = [
    'soy sauce', 'mirin', 'sake', 'rice vinegar', 'miso', 'dashi', 'nori', 'wasabi',
    'ginger', 'garlic', 'green onion', 'sesame oil', 'sesame seeds', 'shiso', 'daikon',
    'bamboo shoots', 'shiitake', 'mushroom', 'enoki', 'udon', 'soba', 'ramen', 'sushi rice',
    'tempura', 'tofu', 'seaweed', 'kombu', 'konbu', 'wakame', 'sakura', 'matcha', 'sake', 'mochi',
    'azuki bean', 'soba', 'yakitori', 'sashimi', 'sukiyaki', 'yakiniku', 'okonomiyaki', 'takoyaki',
    'karaage', 'katsu', 'tonkatsu', 'soba', 'udon', 'yaki', 'soba', 'tororo', 'jiru', 'buri',
    'jiru', 'hojicha'
]

korean_ingredients = [
    'gochujang', 'doenjang', 'ganjang', 'soy sauce', 'sesame oil', 'garlic', 'ginger',
    'green onion', 'kimchi', 'tofu', 'sesame seeds', 'perilla leaves', 'kelp', 'noodles',
    'rice', 'beef', 'pork', 'chicken', 'tofu', 'fish', 'octopus', 'shrimp', 'squid',
    'vegetables', 'cucumber', 'zucchini', 'mushrooms', 'bean sprouts', 'korean radish',
    'garlic chives', 'carrot', 'onion', 'green pepper', 'dried seaweed', 'chestnuts',
    'japanese raisin tree', 'pine nuts', 'gingko nuts', 'pumpkin', 'sesame leaf', 'fermented bean paste',
    'fermented soybean paste', 'soybean paste', 'red pepper paste', 'soybean paste',
    'doenjang', 'perilla oil', 'plum extract'
]

lebanese_ingredients = [
    'olive oil', 'garlic', 'lemon', 'mint', 'parsley', 'thyme', 'sumac', 'cinnamon',
    'allspice', 'nutmeg', 'cumin', 'coriander', 'sesame seeds', 'pita bread', 'bulgur',
    'rice', 'lentils', 'chickpeas', 'lamb', 'chicken', 'beef', 'eggplant', 'zucchini',
    'tomato', 'onion', 'garlic', 'cucumber', 'yogurt', 'labneh', 'feta cheese', 'halloumi',
    'kefalotyri', 'kasseri', 'saffron', 'pomegranate', 'dates', 'figs', 'walnuts',
    'almonds', 'pine nuts', 'pistachios', 'dates', 'figs', 'apples', 'bananas', 'pears', 'grapefruit',
    'lemon', 'orange', 'pomegranate', 'dates'
]

malaysian_ingredients = [
    'coconut milk', 'lemongrass', 'galangal', 'turmeric', 'ginger', 'kaffir lime leaves',
    'candlenut', 'shallot', 'garlic', 'chili', 'belacan', 'palm sugar', 'tamarind',
    'lime', 'banana leaf', 'pandan leaf', 'rice', 'noodles', 'tofu', 'tempeh', 'soy sauce',
    'shrimp paste', 'coriander', 'cumin', 'nutmeg', 'cloves', 'cardamom', 'cinnamon',
    'lemongrass', 'basil', 'lime leaves', 'chili peppers', 'coconut oil', 'coconut sugar',
    'galangal', 'chicken', 'beef', 'pork', 'seafood', 'rice', 'vegetables', 'chicken',
    'fried shallots', 'fried garlic', 'turmeric', 'wheat', 'rice vinegar', 'rice flour',
    'rice flour', 'palm sugar', 'coconut sugar'
]

mexican_ingredients = [
    'corn', 'black beans', 'pinto beans', 'avocado', 'tomato', 'jalapeno', 'chipotle',
    'cilantro', 'lime', 'garlic', 'onion', 'bell pepper', 'corn tortilla', 'flour tortilla',
    'queso fresco', 'cotija cheese', 'chihuahua cheese', 'chile peppers', 'taco seasoning',
    'enchilada sauce', 'adobo sauce', 'guacamole', 'salsa', 'tortilla chips', 'tequila', 'mezcal',
    'mole sauce', 'achiote', 'poblano', 'tomatillo', 'cumin', 'coriander', 'paprika',
    'oregano', 'epazote', 'vanilla', 'cocoa', 'piloncillo', 'honey', 'plantain', 'tamarind',
    'sweet potato', 'squash', 'cactus', 'amaranth', 'chia', 'pumpkin seed', 'aguamiel', 'maguey'
]

pakistani_ingredients = [
    'basmati rice', 'lentils', 'chickpeas', 'wheat flour', 'ghee', 'yogurt', 'milk',
    'paneer', 'chicken', 'lamb', 'beef', 'fish', 'prawns', 'spinach', 'fenugreek',
    'mustard greens', 'coriander', 'mint', 'parsley', 'green chili', 'garlic', 'onion',
    'ginger', 'cardamom', 'cinnamon', 'cloves', 'cumin', 'turmeric', 'nutmeg', 'bay leaf',
    'black pepper', 'coriander powder', 'cumin powder', 'red chili powder', 'garam masala',
    'safron', 'rose water', 'jaggery', 'dates', 'almonds', 'pistachios', 'coconut',
    'raisins', 'figs', 'mango', 'orange', 'banana', 'apple', 'pomegranate'
]

russian_ingredients = [
    'potato', 'beetroot', 'cabbage', 'carrot', 'onion', 'garlic', 'dill', 'sour cream',
    'kefir', 'rye bread', 'buckwheat', 'millet', 'kasha', 'pelmeni', 'vodka', 'kvass',
    'borscht', 'schi', 'smoked fish', 'caviar', 'sausage', 'pickles', 'cucumber', 'tomato',
    'cabbage rolls', 'blini', 'pierogi', 'syrniki', 'tvorog', 'smetana', 'pumpkin', 'turnip',
    'mushrooms', 'goose', 'duck', 'pork', 'beef', 'chicken', 'lamb', 'game', 'pear', 'apple',
    'berry', 'cranberry', 'lingonberry', 'mushroom', 'currant', 'gooseberry', 'blueberry'
]

singapore_ingredients = [
    'rice', 'noodles', 'chili', 'laksa leaf', 'galangal', 'lemongrass', 'coconut milk',
    'fish sauce', 'oyster sauce', 'soy sauce', 'dark soy sauce', 'light soy sauce',
    'belacan', 'candlenut', 'palm sugar', 'tamarind', 'turmeric', 'ginger', 'garlic',
    'shallot', 'sambal', 'chili paste', 'curry powder', 'curry leaf', 'cinnamon', 'star anise',
    'cloves', 'cardamom', 'fennel seeds', 'coriander', 'cumin', 'nutmeg', 'sesame oil',
    'sesame seeds', 'peanut', 'cashew nut', 'coconut', 'green bean', 'spinach', 'okra',
    'eggplant', 'pumpkin', 'cucumber', 'tomato', 'onion', 'spring onion', 'coriander leaf',
    'cilantro'
]

spanish_ingredients = [
    'olive oil', 'garlic', 'onion', 'tomato', 'potato', 'bell pepper', 'chorizo', 'jamón',
    'serrano', 'manchego', 'mahón', 'idiazabal', 'gazpacho', 'paella rice', 'saffron',
    'paprika', 'chorizo', 'pimento', 'morcilla', 'white beans', 'almond', 'hazelnut',
    'orange', 'lemon', 'lime', 'fig', 'grape', 'raisin', 'date', 'apple', 'pear', 'peach',
    'plum', 'apricot', 'melon', 'watermelon', 'cherry', 'quince', 'quince', 'kiwi', 'peas',
    'cauliflower', 'broccoli', 'asparagus', 'spinach', 'chard', 'endive', 'lettuce', 'cabbage',
    'spinach', 'avocado'
]

thai_ingredients = [
    'lemongrass', 'galangal', 'kaffir lime leaves', 'fish sauce', 'oyster sauce',
    'soy sauce', 'coconut milk', 'coconut cream', 'curry paste', 'tamarind', 'palm sugar',
    'rice', 'rice noodles', 'rice flour', 'noodles', 'tofu', 'shrimp', 'prawn', 'fish',
    'crab', 'chicken', 'pork', 'beef', 'duck', 'egg', 'eggplant', 'bean sprout', 'bamboo shoot',
    'green bean', 'mushroom', 'coriander', 'cilantro', 'basil', 'mint', 'thai basil', 'garlic',
    'shallot', 'onion', 'ginger', 'chili', 'lime', 'lemon', 'orange', 'papaya', 'mango', 'pineapple',
    'banana', 'guava'
]

tibetan_ingredients = [
    'tsampa', 'yak butter', 'yak meat', 'mutton', 'cheese', 'dried cheese', 'yogurt',
    'rice', 'barley', 'buckwheat', 'sugar', 'salt', 'tea', 'butter tea', 'sweet tea', 'po cha',
    'chang', 'thenthuk', 'thukpa', 'shyakpa', 'momos', 'khapse', 'sha phaley', 'tingmo',
    'phagsha', 'shapta', 'balep', 'nyoma', 'dresil', 'tse ring', 'kamdi', 'balep', 'phagsha',
    'nakpi', 'peppers', 'chilies', 'noodles', 'pasta', 'bread', 'milk', 'cream', 'butter',
    'margarine', 'curd', 'yak curd', 'cream', 'milk tea', 'dough'
]

vietnamese_ingredients = [
    'fish sauce', 'soy sauce', 'rice vinegar', 'rice noodles', 'rice paper', 'lemongrass',
    'galangal', 'ginger', 'garlic', 'shallot', 'onion', 'lime', 'lemon', 'kaffir lime leaves',
    'coriander', 'cilantro', 'mint', 'thai basil', 'basil', 'perilla', 'star anise', 'cinnamon',
    'cloves', 'cardamom', 'fennel seeds', 'coriander seeds', 'cumin', 'nutmeg', 'turmeric',
    'annatto seeds', 'palm sugar', 'coconut milk', 'coconut cream', 'rice', 'rice noodles',
    'rice flour', 'noodles', 'tofu', 'shrimp', 'prawn', 'fish', 'crab', 'chicken', 'pork',
    'beef', 'duck', 'egg', 'eggplant', 'bean sprout', 'bamboo shoot', 'green bean', 'mushroom'
]

combined_ingredients = american_ingredients + chinese_ingredients + continental_ingredients + \
                       french_ingredients + greek_ingredients + indian_ingredients + \
                       indonesian_ingredients + italian_ingredients + japanese_ingredients + \
                       korean_ingredients + lebanese_ingredients + malaysian_ingredients + \
                       mexican_ingredients + pakistani_ingredients + russian_ingredients + \
                       singapore_ingredients + spanish_ingredients + thai_ingredients + \
                       tibetan_ingredients + vietnamese_ingredients

df2 = pd.read_csv('ingredients.csv')

# ingre = df2['Ingredients'].to_list()
# ingre = [ast.literal_eval(lst) for lst in ingre]
# text = ''.join([' '.join(x) for x in ingre])
# list_text = text.split()
# main_list_ingre = []
# for word in list_text:
#     if word in combined_ingredients and word not in main_list_ingre:
#         main_list_ingre.append(word)

temp_list = df2['Ingredients'][0].to_list()
print(temp_list)
