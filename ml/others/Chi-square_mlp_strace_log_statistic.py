# 使用卡方过滤对knn算法来实现features_file_ml7_generate数据集的分类
# 使用matplotlib绘制验证曲线（n_neighbors）

import datetime

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.model_selection import validation_curve
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler


def ml():
    starttime = datetime.datetime.now()
    df = pd.read_csv('H:\\A数据集\\others\\ring - 副本.csv')
    list = df.values
    # print(df)
    X = list[:, 0:19]  # 取数据集的特征向量
    Y = list[:, 20]  # 取数据集的标签（类型）
    # 使用卡方过滤
    # model1 = SelectKBest(chi2, k=2000)  # 60结果还不错
    # X = model1.fit_transform(X, Y)
    x_train, x_test, y_train, y_test = train_test_split(X, Y, train_size=0.75, random_state=0)
    # 使用xgb
    ss = StandardScaler()
    x_train = ss.fit_transform(x_train)
    x_test = ss.transform(x_test)
    print("==========start============")
    mlp = MLPClassifier(solver='sgd',max_iter=1000,learning_rate='constant')
    # mlp = MLPClassifier(solver='lbfgs', alpha=1e-5, random_state=1, max_iter=1000)
    mlp.fit(x_train, y_train)
    y_predict = mlp.predict(x_test)
    print(classification_report(y_predict, y_test,digits=5))
    # print(gbm.score(x_test,y_test))
    print("==========end============")
    endtime = datetime.datetime.now()
    print(endtime - starttime)
    # 绘制图像
    param_range = np.arange(0.1, 0.99, 0.1)
    train_scores, test_scores = validation_curve(mlp, X, Y,param_name='beta_2', param_range=param_range, cv=10)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.title("Validation Curve with MLP")
    plt.xlabel("$\gamma$")
    plt.ylabel("Score")
    plt.xlabel("beta_2")
    plt.ylim(0.0, 1.1)
    plt.xticks(param_range)
    lw = 2
    # 半对数坐标函数：只有一个坐标轴是对数坐标，另一个是普通算术坐标
    # plt.semilogx(param_range, train_scores_mean, label="Training score",
    #              color="darkorange", lw=lw)
    plt.plot(param_range, train_scores_mean, label="Training score",
             color="darkorange", lw=lw)
    # 在区域内绘制函数包围的区域
    # plt.fill_between(param_range, train_scores_mean - train_scores_std,
    #                  train_scores_mean + train_scores_std, alpha=0.2,
    #                  color="darkorange", lw=lw)
    # plt.semilogx(param_range, test_scores_mean, label="Cross-validation score",
    #              color="navy", lw=lw)
    plt.plot(param_range, test_scores_mean, label="Cross-validation score",
             color="navy", lw=lw)
    # plt.fill_between(param_range, test_scores_mean - test_scores_std,
    #                  test_scores_mean + test_scores_std, alpha=0.2,
    #                  color="navy", lw=lw)
    plt.legend(loc="best")
    plt.show()


if __name__ == "__main__":
    ml()