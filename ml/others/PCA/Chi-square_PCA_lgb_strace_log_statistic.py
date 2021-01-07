# 使用卡方过滤对lgb算法来实现features_file_ml7_generate数据集的分类
# 使用matplotlib绘制验证曲线（n_neighbors）

import datetime

import lightgbm as lgb
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.model_selection import validation_curve
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
    x_train, x_test, y_train, y_test = train_test_split(X, Y, train_size=0.75, random_state=4)
    # 使用xgb
    ss = StandardScaler()
    x_train = ss.fit_transform(x_train)
    x_test = ss.transform(x_test)
    print("==========start============")
    # gbm = lgb.LGBMClassifier(num_leaves=50, learning_rate=0.02, n_estimators=50)
    # gbm = lgb.LGBMClassifier(feature_fraction=0.4,min_sum_hessian_in_leaf=1,lambda_l1=0.1,
    #                          min_data_in_leaf=1,max_depth=1,num_iteration=300,num_leaves=100, learning_rate=0.2, n_estimators=300)
    gbm = lgb.LGBMClassifier(feature_fraction=0.4,min_sum_hessian_in_leaf=1,lambda_l1=0.1,
                             min_data_in_leaf=1,max_depth=1,num_iterations=300,num_leaves=100, learning_rate=0.2, n_estimators=300)
    # PCA
    estimator = PCA(n_components=19)
    x_train = estimator.fit_transform(x_train)
    x_test = estimator.transform(x_test)

    gbm.fit(x_train, y_train)
    y_predict = gbm.predict(x_test)
    y_proba = gbm.predict_proba(x_test)
    print(classification_report(y_predict, y_test,digits=5))
    # print(gbm.score(x_test,y_test))
    print("==========end============")
    endtime = datetime.datetime.now()
    print(endtime - starttime)
    return
    for index in range(1,20):
        # if index<103:
        #     index+=1
        #     continue
        # select features using threshold
        estimator = PCA(n_components=index)
        select_X_train = estimator.fit_transform(x_train)
        # train model
        selection_model = lgb.LGBMClassifier(feature_fraction=0.4,min_sum_hessian_in_leaf=1,lambda_l1=0.1,
                             min_data_in_leaf=1,max_depth=1,num_iterations=300,
                            num_leaves=100, learning_rate=0.2, n_estimators=300)
        selection_model.fit(select_X_train, y_train)
        # eval model
        select_X_test = estimator.transform(x_test)
        y_pred = selection_model.predict(select_X_test)
        # predictions = [round(value) for value in y_pred]
        accuracy = accuracy_score(y_test, y_pred)
        print("n=%d, Accuracy: %.4f%%" % (index, accuracy * 100.0))
    return
    # 绘制PR曲线
    precision, recall, thresholds = precision_recall_curve(
        y_test, y_proba[:, 1])
    plt.figure("P-R Curve")
    plt.title('Precision/Recall Curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.plot(recall, precision)
    plt.show()
    ##绘制roc曲线
    plt.figure("ROC Curve")
    fpr, tpr, threshold = roc_curve(y_test, y_proba[:, 1])
    plt.plot(fpr, tpr, color='darkorange')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    roc_auc = auc(fpr, tpr)
    print(roc_auc)
    plt.show()
    # 绘制图像
    return
    param_range = np.arange(0, 100, 10)
    train_scores, test_scores = validation_curve(gbm, X, Y,param_name='lambda_l1', param_range=param_range, cv=10)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.title("Validation Curve with LGBM")
    plt.xlabel("$\gamma$")
    plt.ylabel("Score")
    plt.xlabel("lambda_l1")
    plt.ylim(0.0, 1.1)
    plt.xticks(param_range)
    lw = 2
    # 半对数坐标函数：只有一个坐标轴是对数坐标，另一个是普通算术坐标
    # plt.semilogx(param_range, train_scores_mean, label="Training score",
    #              color="darkorange", lw=lw)
    plt.plot(param_range, train_scores_mean, label="Training score",
             color="darkorange", lw=lw)
    # 在区域内绘制函数包围的区域
    plt.fill_between(param_range, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.2,
                     color="darkorange", lw=lw)
    # plt.semilogx(param_range, test_scores_mean, label="Cross-validation score",
    #              color="navy", lw=lw)
    plt.plot(param_range, test_scores_mean, label="Cross-validation score",
             color="navy", lw=lw)
    plt.fill_between(param_range, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.2,
                     color="navy", lw=lw)
    plt.legend(loc="best")
    plt.show()

if __name__ == "__main__":
    ml()
