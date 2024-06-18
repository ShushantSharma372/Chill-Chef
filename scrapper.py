import requests
from bs4 import BeautifulSoup as bs

def scrap_recipe(url):

    site_data = requests.get(url).text
    soup = bs(site_data, 'lxml')

    title = soup.find('h1', class_="sp-ttl").text
    time_title_list = soup.find_all('span', class_ = "RcpInf_crd_tx1")
    time_value_list = soup.find_all('span', class_ = "RcpInf_crd_tx2")
    ingredients = soup.find_all('li', class_ = "RcpIngd-tp_li")

    info_dict = {}

    info_dict['Title'] = title
    for name, value in zip(time_title_list,time_value_list):
        info_dict[name.text.strip()] = value.text.strip()
    info_dict['Difficulty'] = time_title_list[-1].text.strip()

    ingre_list = [x.text.strip() for x in ingredients]
    info_dict['Ingredients'] = ingre_list

    return info_dict



if __name__ == "__main__":
    url = 'https://food.ndtv.com/recipe-beetroot-idli-fry-958470'
    val = scrap_recipe(url)
    print(val)
