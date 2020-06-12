"""
Lasso_regulation_program

- train_data = 20대 총선 자료,
    d = 더불어 민주당
    s = 새누리당
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from pandas import Series
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso, Ridge, ElasticNet

# Make graph font English to Korean
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)


# Training & Test Data Load
train_data = pd.read_csv('C:/Users/khw08/Desktop/OSBAD_Project/TAG/2016DTM7_lasso.csv')

# Na Data dop
train_data.dropna()

# Arrange Data Set
x = train_data.drop(['d'], axis=1)
X = x.drop(['s'], axis=1)
Y = train_data.loc[:, ['d']]

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)    # Split Data Set
predictors = X.columns                                                # Save tarin_X attributes

"""
Lasso Regression
lassoReg   = Coefficient List
predictors = Attributes List
coef       = DataFrame with Attributes & Coefficient
pre_coef   = Except Zero Coefficient Value List
"""
ridgeReg = ElasticNet(alpha=0.001)                                          # Call Lasso Regression Function
ridgeReg.fit(x_train, y_train)                                              # Fit Data in Lasso function

ridgeData = np.array(ridgeReg.coef_).flatten().tolist()                     # 데어터 전처리

coef = Series(ridgeData, predictors).sort_values()                          # Save Coefficient
print(np.sum(ridgeReg.coef_ != 0))                                          # Check the number of valid Coefficient
coef_pre = coef[coef != 0.0][coef != -0.0]                                  # Except Zero Coefficient


coef_pre.plot(kind='bar')                                                   # Show Graph Coefficient formed by Bar
plt.show()


y_pred = ridgeReg.predict(x_test)                                           # Predict Target value


"""Testing dummy Codes.."""

'''
for idx, val in enumerate(coef):
    print(val)
'''
'''
#print(y_pred)
arr = []
for idx, val in enumerate(y_pred):
    if val >= 0.5:
        val = 1
        arr.append(val)
    elif val < 0.5:
        val = 0
        arr.append(val)

print(arr)
'''
'''
# x_test 값을 Dataframe 형식으로 저장
dataframe_x = pd.DataFrame(x_test)
dataframe_x.to_csv('C:/Users/khw08/Desktop/Lasso_x_test_21.csv', encoding='utf-8-sig')

# y_pred2 값을 Dataframe 형식으로 저장
dataframe_y = pd.DataFrame(y_pred)
dataframe_y.to_csv('C:/Users/khw08/Desktop/Lasso_y_pred_21.csv', encoding='utf-8-sig')
'''

# 계수
# Rcoef = pd.read_csv('C:/Users/khw08/Desktop/Lasso_coef.csv')


#dataframe_x = pd.DataFrame(coef)
#dataframe_x.to_csv('C:/Users/khw08/Desktop/Lasso_coef.csv', encoding='utf-8-sig')


"""arr = []
for idx, val in enumerate(coef):
    if val != 0.0 or -0.0:
        arr.append(val)

print(arr)

a = Series(arr).sort_values()"""