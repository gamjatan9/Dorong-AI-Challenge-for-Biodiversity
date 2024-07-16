"""
도롱뇽 분포 데이터 수집: gbif.org_Hynobius leechii Boulenger, 1887
https://www.gbif.org/occurrence/map?taxon_key=2431142
"""

import csv
import pandas as pd

# 파일 불러오기
file_path = 'dorong.csv'
with open(file_path, 'r', encoding='cp949') as file:
    lines = file.readlines()[1:]
    

# 필요한 데이터 위도, 경도 추출
extracted_data = []
for line in lines:
    split_line = line.split('\t')  # 탭을 기준으로 분리
    if len(split_line) > 22:
        latitude = split_line[21]
        longitude = split_line[22]
        extracted_data.append([latitude, longitude])

# 데이터프레임 생성
df_extracted = pd.DataFrame(extracted_data, columns=['Latitude', 'Longitude'])

# 결과 파일 저장
output_file_path = 'dorongWithLocation.csv'
df_extracted.to_csv(output_file_path, index=False)


'''
위도, 경도 좌표를 주소로 변환
카카오 API 사용
'''

import requests
from dotenv import load_dotenv
import json
import pandas as pd
import time


# kakao API 주소 요청
def get_address_from_kakao(lat, lon, kakao_api_key):
    url = f"https://dapi.kakao.com/v2/local/geo/coord2address.json?x={lon}&y={lat}&input_coord=WGS84"
    headers = {"Authorization": f"KakaoAK {kakao_api_key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            address_info = response.json()['documents'][0]['address']
            address = f"{address_info['region_1depth_name']} {address_info['region_2depth_name']} {address_info['region_3depth_name']}"
            return address
        except (IndexError, KeyError):
            return "주소를 찾을 수 없습니다."
    else:
        return "API 요청 오류"
    
# API 키 설정 (kakao developers_REST API key)
load_dotenv()
kakao_api_key = os.getenv('KAKAO_API_KEY')

# 주소 조회 및 결과 저장
df = pd.read_csv('dorongWithLocation.csv')
addresses = []
for index, row in df.iterrows():
    address = get_address_from_kakao(row['위도'], row['경도'], api_key)
    addresses.append(address)

df['주소'] = addresses

# 결과 파일 저장
df.to_csv('주소추가.csv', index=False, encoding='utf-8-sig')


'''
# 구글 API - 영문 주소

def get_address_from_coordinates(latitude, longitude, google_api_key):
    # Google Maps Geocoding API의 URL
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}"

    # API 요청
    response = requests.get(url)
    if response.status_code == 200:
        # 응답에서 주소 추출
        results = response.json()['results']
        if results:
            address = results[0]['formatted_address']
            return address
        else:
            return "주소를 찾을 수 없습니다."
    else:
        return "API 요청 오류"

# API 키 설정
google_api_key = os.getenv('GOOGLE_API_KEY')
'''
