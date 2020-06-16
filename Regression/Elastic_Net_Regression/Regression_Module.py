"""
Regression_program

- train_data = 21대 총선 자료, 788개
- test_data = 21대 총선 자료, 788개 나머지
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from pandas import Series
from sklearn.linear_model import Lasso, Ridge, ElasticNet

# Make graph font English to Korean
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

# Training & Test Data Load
train_data = pd.read_csv('C:/Users/khw08/Desktop/OSBAD_Project/Regression/KoNLPY_M&D_train_CSV_2.csv')

x_train = []
y_train = []
predictors = []

# Test List
x = train_data.drop(['d'], axis=1)
x_2 = x.drop(['m'], axis=1)
x_test = x_2.loc[800:6364, :]
y_pred = []

# 더불어 민주당 train_data 생성
d_x = train_data.drop(['d'], axis=1)
d_x_2 = d_x.drop(['m'], axis=1)
d_y = train_data.loc[:, ['d']]

d_x_train = d_x_2.loc[:788, :]
d_y_train = d_y.loc[:788, :]

d_predictors = d_x_train.columns

# 미래통합당 train_data 셍성
m_x = train_data.drop(['d'], axis=1)
m_x_2 = d_x.drop(['m'], axis=1)
m_y = train_data.loc[:, ['m']]

m_x_train = m_x_2.loc[:788, :]
m_y_train = m_y.loc[:788, :]

m_predictors = m_x_train.columns

# Coefficient List
coef_list = []
coef_result = []

# Approval
d_real_approval = 0.60
m_real_approval = 0.34

"""
Regression
____Reg   = Coefficient List
predictors = Attributes List
coef       = DataFrame with Attributes & Coefficient
pre_coef   = Except Zero Coefficient Value List
"""


def Reg_coef(var, a):
    global y_pred

    if var == 0:
        lassoReg = Lasso(alpha=a)
        lassoReg.fit(x_train, y_train)

        coef = Series(lassoReg.coef_, predictors).sort_values()  # Save Coefficient
        coef_pre = coef[coef != 0.0][coef != -0.0]  # Except Zero Coefficient
        print(np.sum(lassoReg.coef_ != 0))  # Check the number of valid Coefficient
        y_pred = lassoReg.predict(x_test)

    elif var == 1:
        ridgeReg = Ridge(alpha=a)  # Call Ridge Regression Function
        ridgeReg.fit(x_train, y_train)  # Fit Data in Ridge function

        ridgeData = np.array(ridgeReg.coef_).flatten().tolist()  # Data Preprocessed 2D List to 1D List

        coef = Series(ridgeData, predictors).sort_values()  # Save Coefficient
        coef_pre = coef[coef != 0.0][coef != -0.0]  # Except Zero Coefficient
        print(np.sum(ridgeReg.coef_ != 0))  # Check the number of valid Coefficient
        y_pred = ridgeReg.predict(x_test)

    elif var == 2:
        elasticReg = ElasticNet(alpha=a)  # Call Elastic_Net Regression Function
        elasticReg.fit(x_train, y_train)  # Fit Data in Lasso function

        elasticData = np.array(elasticReg.coef_).flatten().tolist()  # Data Preprocessed 2D List to 1D List

        coef = Series(elasticData, predictors).sort_values()  # Save Coefficient
        coef_pre = coef[coef != 0.0][coef != -0.0]  # Except Zero Coefficient
        print(np.sum(elasticReg.coef_ != 0))  # Check the number of valid Coefficient
        y_pred = elasticReg.predict(x_test)

    else:
        print('Wrong Input!')
        exit()

    print('상위 5 단어')
    print(coef_pre.head())
    print('하위 5 단어')
    print(coef_pre.tail())
    coef_pre.plot(kind='bar')  # Show Graph Coefficient formed by Bar
    plt.show()


def Approval_Rate(party, var):
    p_count = 0
    n_count = 0
    global y_pred

    for idx, val in enumerate(y_pred):
        if val >= 0.5:
            val = 1
            coef_result.append(val)
        elif val < 0.5:
            val = 0
            coef_result.append(val)
    print(coef_result)

    for idx, pn in enumerate(y_train):
        if pn == 1:
            p_count = p_count + 1
        elif pn == 0:
            n_count = n_count + 1

    for pn in coef_result:
        if pn == 1:
            p_count = p_count + 1
        elif pn == 0:
            n_count = n_count + 1

    p_approval = p_count / (p_count + n_count)
    # n_approval = n_count / (p_count + n_count)

    print(p_approval)
    # print(n_approval)

    if party == 0:
        plt.bar('실제 지지율', d_real_approval, width=0.35, label='실제 지지율')
        plt.bar('예측 지지율', p_approval, width=0.35, label='예측 지지율')
        plt.xlabel('더불어 민주당')
    elif party == 1:
        plt.bar('실제 지지율', m_real_approval, width=0.35, label='실제 지지율')
        plt.bar('예측 지지율', p_approval, width=0.35, label='예측 지지율')
        plt.xlabel('미래 통합당')

    plt.ylabel('지지율')
    plt.show()


def Model_Accuacy():
    alpha_set = [0.00001, 0.0001, 0.001, 0.01, 0.1, 1]
    max_inter_set = [100000000, 10000000, 1000000, 100000, 10000, 1000]

    la_train_score = []
    ri_train_score = []
    el_train_score = []
    used_feature = []

    for a, m in zip(alpha_set, max_inter_set):
        lasso = Lasso(alpha=a, max_iter=m).fit(x_train, y_train)
        ridge = Ridge(alpha=a, max_iter=m).fit(x_train, y_train)
        elastic = ElasticNet(alpha=a, max_iter=m).fit(x_train, y_train)

        la_tr_score = round(lasso.score(x_train, y_train), 3)
        ri_tr_score = round(ridge.score(x_train, y_train), 3)
        el_tr_score = round(elastic.score(x_train, y_train), 3)

        la_number_used = np.sum(lasso.coef_ != 0)
        ri_number_used = np.sum(ridge.coef_ != 0)
        el_number_used = np.sum(elastic.coef_ != 0)

        la_train_score.append(la_tr_score)
        ri_train_score.append(ri_tr_score)
        el_train_score.append(el_tr_score)

        used_feature.append(la_number_used)
        used_feature.append(ri_number_used)
        used_feature.append(el_number_used)

    index = np.arange(len(alpha_set))

    bar_width = 0.25

    plt.bar(index, la_train_score, width=bar_width, label='Lasso train')
    plt.bar(index + bar_width, ri_train_score, width=bar_width, label='Ridge train')
    plt.bar(index + (bar_width * 2), el_train_score, width=bar_width, label='Elastic Net train')

    plt.xticks(index + bar_width / 2, alpha_set)  # bar그래프 dodge를 하기 위해 기준값에 보정치를 더해줍니다.

    for i, (lt, rt, et) in enumerate(zip(la_train_score, ri_train_score, el_train_score)):
        plt.text(i, lt + 0.01, str(lt), horizontalalignment='center')
        plt.text(i + bar_width, rt + 0.01, str(rt), horizontalalignment='center')
        plt.text(i + (bar_width * 2), et + 0.01, str(et), horizontalalignment='center')

    plt.legend(loc=1)
    plt.xlabel('alpha')
    plt.ylabel('score')
    plt.show()


if __name__ == '__main__':


    # 데이터 선택
    print("Party")
    party = int(input('더불어 민주당 : 0, 미래통합당 : 1 = '))

    if party == 0:
        x_train = d_x_train
        y_train = d_y_train
        predictors = d_predictors
    elif party == 1:
        x_train = m_x_train
        y_train = m_y_train
        predictors = m_predictors

    #정확도 확인
    Model_Accuacy()

    print('Coefficient')
    var = int(input('Lasso: 0, Ridge : 1, Elastic Net : 2 = '))
    a = float(input('alpha = '))

    Reg_coef(var, a)

    print('Approval')
    Approval_Rate(party, var)
