## 성능 지표

- 정확도 (Accuracy): **68.3%** <br>
모델이 전체적으로 얼마나 정확한지를 측정하는 지표. 서식이 적절한지 여부를 예측.

- 정밀도 (Precision): **70.6%** <br>
모델이 긍정으로 예측한 관측치 중에서 실제 긍정인 비율. 서식이 적절하다고 예측할 때, 그 예측이 약 70.6% 정확함.

- 재현율 (Recall): **92.96%** <br>
실제 긍정 중에서 정확하게 예측한 비율. 서식이 적절한 환경을 효과적으로 찾아내는데, 실제로 약 92.96%를 정확하게 식별함.

- F1 점수 (F1 Score): **80.24%** <br>
정밀도와 재현율의 가중 평균. 이는 거짓 긍정과 거짓 부정을 모두 고려한다. 이 지표는 정밀도와 재현율 사이의 균형을 제공.


- 혼돈 행렬 (Confusion Matrix): <br>

<div style="display: flex; align-items: center;">
  <div style="margin: 0px 10px;">
    <table border="2">
      <tr>
        <td></td>
        <td>Negative</td>
        <td>Positive</td>
      </tr>
      <tr>
      <td>Negative</td>
        <td>(TN) 8</td>
        <td>(FP) 55</td>
      </tr>
      <tr>
      <td>Positive</td>
        <td>(FN) 10</td>
        <td>(TP) 32</td>
      </tr>
    </table>
  </div>
  <div>
    <ul>
      <li>
      True Negatives: "서식하기 힘든 환경"을 8번 예측
      </li>
      <li>
      False Positives: "서식 가능한 환경"이라고 예측했지만 실제로는 아니었던 경우 55번
      </li>
      <li>
      False Negatives: "서식하기 힘든 환경"이라고 예측했지만 실제로는 서식 가능한 경우 10번
      </li>
      <li>
      True Positives: "서식 가능한 환경"을 132번 예측
      </li>
    </ul>
  </div>
</div>

#### 요약 : 모델은 꽤 정확도가 높으며 특히 재현율 면에서 우수한 성과를 보이고 있습니다. 그러나 정밀도 면에서는 개선의 여지가 있으며, 거짓 긍정을 줄이는 방향으로 발전할 수 있을 것입니다.

<br> 

## 회귀 모델
![image](https://github.com/user-attachments/assets/b83267af-98ee-4ed9-8546-6d951be4fb38)


학습한 모델의 회귀 계수는 위와 같으며 지형 유형이 0.83으로 가장 높은 영향력을 가지고 토양 pH가 -0.32로 그 다음으로 높은 영향력을 가졌다.

<br>

## 결론

 모델 성능이 accuracy 68.3%로 아쉽게 나오지만 훈련에 사용된 환경 변수 데이터가 지형, 토양 pH, 토양 전기전도도, 위험 요인까지의 거리 뿐이었으므로 좀 더 다양한 환경 변수 데이터 수집이 가능해진다면 모델 성능 개선 또한 이루어질 것으로 예측된다.