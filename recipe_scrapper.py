from selenium import webdriver
from scrapper import scrap_recipe
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

def get_cuisine_url():

    cuisine_text = requests.get('https://food.ndtv.com/recipes/by-cuisine').text
    soup = bs(cuisine_text, 'lxml')
    list_cuisines = soup.find_all('a', class_ = "crd_ttl")
    cuisine_dict = {}
    for val in list_cuisines:
        cuisine_dict[val.text.strip()] = val.get('href')

    return cuisine_dict

def recipes_url(url):
    
    recipe_list_text = requests.get(url).text
    soup = bs(recipe_list_text, 'lxml')
    list_cuisines = soup.find_all('a', class_ = "crd_ttl")
    recipe_dict = {}
    for val in list_cuisines:
        link = val.get('href')
        if 'hindi' not in link:
            recipe_dict[val.text.strip()] = link

    return recipe_dict

def scrap_recipes(dict):
    main_recipes_dict = {key: [] for key in ('Title', 'Total Cook Time', 'Prep Time',
                                             'Cook Time', 'Recipe Servings', 'Difficulty',
                                             'Ingredients', 'Cuisine', 'Method', 'Link', 'Image')}
    recipe_counter = 0
    for cuisine, recipe in dict.items():
        for name, link in recipe.items():
            temp = scrap_recipe(link)
            recipe_counter += 1
            main_recipes_dict['Title'].append(temp.get('Title', ''))
            main_recipes_dict['Total Cook Time'].append(temp.get('Total Cook Time', ''))
            main_recipes_dict['Prep Time'].append(temp.get('Prep Time', ''))
            main_recipes_dict['Cook Time'].append(temp.get('Cook Time', ''))
            main_recipes_dict['Recipe Servings'].append(temp.get('Recipe Servings', ''))
            main_recipes_dict['Difficulty'].append(temp.get('Difficulty', ''))
            main_recipes_dict['Ingredients'].append(temp.get('Ingredients', ''))
            main_recipes_dict['Cuisine'].append(cuisine)
            main_recipes_dict['Method'].append(temp.get('Method', ''))
            main_recipes_dict['Link'].append(temp.get('Link', ''))
            main_recipes_dict['Image'].append(temp.get('Image', ''))
            print("Data Scrapping for Recipe ", recipe_counter, " is done.")
    print("All recipes data is scrapped.")
    return main_recipes_dict



def main():
    working_dict = {}
    cnt = 0
    cuisine_list = get_cuisine_url()
    for name, link in cuisine_list.items():
        working_dict[name] = recipes_url(link)
    
    recipes_dict = scrap_recipes(working_dict)
    df = pd.DataFrame(recipes_dict)
    df.to_csv('recipes_data.csv')
    


if __name__ == "__main__":
    main()

        
