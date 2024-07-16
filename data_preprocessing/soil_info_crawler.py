"""
토양 pH, 전기전도도 데이터 수집
http://soil.rda.go.kr/soil/sibi/sibiExam.jsp
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select  
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 도롱뇽 분포 데이터 with 행정동 주소 파일 불러옴
df = pd.read_csv('dorong.csv')

# 주소를 광역시/도, 시/군/구, 읍/면/동, 리로 분리
address_parts = df['주소'].str.split(" ", expand=True)
df['시도'] = address_parts[0]
df['시군구'] = address_parts[1]
df['읍면동'] = address_parts[2]
df['리'] = address_parts[3] if address_parts.shape[1] > 0 else None
# 주소 형식 변환
full_names = {
    '경기': '경기도',
    '충남': '충청남도',
    '부산': '부산광역시',
    '경남': '경상남도',
    '경북': '경상북도',
    '울산': '울산광역시',
    '서울': '서울특별시',
    '대구': '대구광역시',
    '인천': '인천광역시',
    '광주': '광주광역시',
    '대전': '대전광역시',
    '제주': '제주특별자치도',
    '세종': '세종특별자치시',
    '강원': '강원도',
    '충북': '충청북도',
    '전남': '전라남도',
    '전북특별자치도': '전라북도'
}
df['시도'] = df['시도'].replace(full_names)

# 크롤링시작
driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
driver.get('http://soil.rda.go.kr/soil/sibi/sibiExam.jsp')

# 결과를 저장할 리스트
ph_values = []
conductivity_values = []
#ph_values = [None] * len(df)
#conductivity_values = [None] * len(df)

# 각 주소에 대해 매크로 실행
for index, row in df.iterrows():
    try:
        select_province = Select(driver.find_element(By.ID, 'sido_cd_mini'))
        select_province.select_by_visible_text(row['시도'])
        time.sleep(1)

        select_city = Select(driver.find_element(By.ID, 'sgg_cd_mini'))
        select_city.select_by_visible_text(row['시군구'])
        time.sleep(1)

        select_town = Select(driver.find_element(By.ID, 'umd_cd_mini'))
        select_town.select_by_visible_text(row['읍면동'])
        time.sleep(1)

        if row['리']:
            select_village = Select(driver.find_element(By.ID, 'ri_cd_mini'))
            select_village.select_by_visible_text(row['리'])
            time.sleep(1)

        time.sleep(2)  # 결과 조회 대기
        result_table = driver.find_element(By.CSS_SELECTOR, 'table.item_b tbody')
        rows = result_table.find_elements(By.TAG_NAME, 'tr')
        
        # pH 값
        ph_value = rows[2].find_elements(By.TAG_NAME, 'td')[0].text   
        # 전기전도도 값
        conductivity_value = rows[2].find_elements(By.TAG_NAME, 'td')[6].text

        # 결과 저장
        ph_values[index] = ph_value
        conductivity_values[index] = conductivity_value
    except Exception as e:
        # 에러 처리
        print(f"Error processing row {index}: {e}")
        ph_values[index] = None
        conductivity_values[index] = None
# WebDriver 닫기
driver.quit()

# 결과를 DataFrame에 추가
df['토양pH'] = ph_values
df['전기전도도'] = conductivity_values

# 결과 파일 저장
output_file = 'soilData.csv'
df.to_csv(output_file, index=False)
