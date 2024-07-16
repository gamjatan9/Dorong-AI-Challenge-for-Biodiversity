# -*- coding: utf-8 -*-
"""logisticregression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lu6gX4-YuOShMVuwB3JvS7zERRlrrFyN
"""

import pandas as pd

data = pd.read_csv('result.csv')
data.head()

data.drop(columns=['Unnamed: 0'], inplace=True)

data.head()

"""one-hot encoding"""

data['지형유형'] = data['지형유형'].apply(lambda x: 1 if x == '산림' else 0)
data.head()

"""model training&evaluation"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

X = data.drop('y', axis=1)
y = data['y']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

conf_matrix = confusion_matrix(y_test, y_pred)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("\nConfusion Matrix:\n", conf_matrix)

def predict_formatting(latitude, longitude, elevation, terrain_type, road_distance, soil_ph, electrical_conductivity):
    input_data = {
        '위도': [latitude],
        '경도': [longitude],
        '고도': [elevation],
        '지형유형': [terrain_type],  # 1 for '산림', 0 for '평지'
        '도로거리': [road_distance],
        '토양 pH': [soil_ph],
        '전기전도도': [electrical_conductivity]
    }
    input_df = pd.DataFrame(input_data)

    input_df['지형유형'] = input_df['지형유형'].apply(lambda x: 1 if x == '산림' else 0)

    prediction = model.predict(input_df)

    return prediction[0]

latitude_input = float(input("위도: "))
longitude_input = float(input("경도: "))
elevation_input = float(input("고도: "))
terrain_type_input = input("지형 유형(산림/평지): ")
road_distance_input = float(input("위험 요인(도로)까지의 거리(m): "))
soil_ph_input = float(input("토양 pH: "))
electrical_conductivity_input = float(input("전기전도도: "))

result = predict_formatting(latitude_input, longitude_input, elevation_input, terrain_type_input, road_distance_input, soil_ph_input, electrical_conductivity_input)

if result == 1:
    print("결과: 도롱뇽이 서식 가능한 환경입니다.")
else:
    print("결과: 도롱뇽이 서식하기 힘든 환경입니다.")

coefficients = model.coef_[0]
intercept = model.intercept_[0]

print("Intercept:", intercept)
for feature, coef in zip(X.columns, coefficients):
    print(f"{feature}: {coef}")

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(X.columns, coefficients)
plt.xlabel("Variables")
plt.ylabel("Coefficients")
plt.title("Logistic Regression Coefficients")
plt.show()