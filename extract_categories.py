from bs4 import BeautifulSoup

with open('/Users/mygyan/Downloads/Code Arena/vanderbilt/product.html', 'r') as f:
    soup = BeautifulSoup(f, 'html.parser')

items = soup.find_all('a', attrs={'data-depth': '0'})
for item in items:
    label = item.find('span', class_='menu-label')
    if label:
        print(label.get_text().strip())
