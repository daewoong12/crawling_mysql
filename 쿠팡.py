from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv

chrome_option = Options()
chrome_option.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_option)
driver.get('https://www.coupang.com/np/campaigns/82/components/194182?listSize=60&brand=&offerCondition=&filterType=&isPriceRange=false&minPrice=&maxPrice=&channel=user&fromComponent=Y&selectedPlpKeepFilter=&sorter=bestAsc&filter=&component=194182&rating=0')

time.sleep(5)  # 페이지가 완전히 로드될 때까지 대기

# 페이지 소스 가져오기
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

# 제품 리스트 추출
product_list = soup.select('ul#productList > li')


data = []

# 제품 정보 추출 (최대 40개)
for idx, product in enumerate(product_list):
    if idx >= 40:  # 40개 데이터만 추출
        break
    
    # 제품명
    name_tag = product.select_one('div.name')
    name = name_tag.get_text(strip=True)
    # print(name)

    # 제품 URL
    link_tag = product.select_one('a')
    product_url = 'https://www.coupang.com' + link_tag['href']
    # print(product_url)

    # 가격
    price_tag = product.select_one('strong.price-value')
    price = price_tag.get_text(strip=True)
    # print(price)

    # 평점
    rating_tag = product.select_one('em.rating')
    rating = rating_tag.get_text(strip=True)
    # print(rating)

    # 데이터 저장
    data.append({
        '제품명': name,
        'URL': product_url,
        '가격': price,
        '평점': rating
    })
    



# # 추출된 데이터 CSV로 저장
csv_file = 'products.csv'
csv_columns = ['제품명', 'URL', '가격', '평점']

with open(csv_file, mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(data)
        print(f"{csv_file} 데이터 저장O")

# WebDriver 종료
driver.quit()