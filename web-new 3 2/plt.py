import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, zero_one_loss
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn import preprocessing
 
# 加载数据
raw_data_filename = "totall_extend.csv"
print("Loading raw data...")
raw_data = pd.read_csv(raw_data_filename, header=None,low_memory=False)
 
# 随机抽取比例，当数据集比较大的时候，可以采用这个，可选项
raw_data=raw_data.sample(frac=0.03)
 
# 查看标签数据情况
last_column_index = raw_data.shape[1] - 1
print("print data labels:")
print(raw_data[last_column_index].value_counts())
 
# 将非数值型的数据转换为数值型数据
# print("Transforming data...")
raw_data[last_column_index], attacks = pd.factorize(raw_data[last_column_index], sort=True)
 
# 对原始数据进行切片，分离出特征和标签，第1~78列是特征，第79列是标签
features = raw_data.iloc[:, :raw_data.shape[1] - 1]  # pandas中的iloc切片是完全基于位置的索引
labels = raw_data.iloc[:, raw_data.shape[1] - 1:]
 
# 特征数据标准化，这一步是可选项
features = preprocessing.scale(features)
features = pd.DataFrame(features)
 
# 将多维的标签转为一维的数组
labels = labels.values.ravel()
 
# 将数据分为训练集和测试集,并打印维数
df = pd.DataFrame(features)
X_train, X_test, y_train, y_test = train_test_split(df, labels, train_size=0.8, test_size=0.2, stratify=labels)
 
# print("X_train,y_train:", X_train.shape, y_train.shape)
# print("X_test,y_test:", X_test.shape, y_test.shape)
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, zero_one_loss
 
# 训练模型
print("Training model...")
clf = DecisionTreeClassifier(criterion='entropy', max_depth=12, min_samples_leaf=1, splitter="best")
trained_model = clf.fit(X_train, y_train)
print("Score:", trained_model.score(X_train, y_train))
 
# 预测
print("Predicting...")
y_pred = clf.predict(X_test)
print("Computing performance metrics...")
results = confusion_matrix(y_test, y_pred)
error = zero_one_loss(y_test, y_pred)
 
# 根据混淆矩阵求预测精度
list_diag = np.diag(results)
list_raw_sum = np.sum(results, axis=1)
print("Predict accuracy of the decisionTree: ", np.mean(list_diag) / np.mean(list_raw_sum))
class PlotConfusionMatrix:
    def plot_confusion_matrix(self,labels,cm, title='Confusion Matrix', cmap=plt.cm.binary):
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        xlocations = np.array(range(len(labels)))
        plt.xticks(xlocations, labels, rotation=90)
        plt.yticks(xlocations, labels)
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
 
    def prepareWork(self,labels, y_true, y_pred):
        tick_marks = np.array(range(len(labels))) + 0.5
        cm = confusion_matrix(y_true, y_pred)
        np.set_printoptions(precision=2)
        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        plt.figure(figsize=(12, 8), dpi=120)
 
        ind_array = np.arange(len(labels))
        x, y = np.meshgrid(ind_array, ind_array)
 
        for x_val, y_val in zip(x.flatten(), y.flatten()):
            c = cm_normalized[y_val][x_val]
            if c > 0.01:
                plt.text(x_val, y_val, "%0.2f" % (c,), color='red', fontsize=7, va='center', ha='center')
        # offset the tick
        plt.gca().set_xticks(tick_marks, minor=True)
        plt.gca().set_yticks(tick_marks, minor=True)
        plt.gca().xaxis.set_ticks_position('none')
        plt.gca().yaxis.set_ticks_position('none')
        plt.grid(True, which='minor', linestyle='-')
        plt.gcf().subplots_adjust(bottom=0.15)
 
        self.plot_confusion_matrix(labels,cm_normalized, title='Normalized confusion matrix')
        # show confusion matrix
        plt.savefig('confusion_matrix.png', format='png')
        plt.show()
        # 绘制混淆矩阵
def plotMatrix(attacks, y_test, y_pred):
    # attacks是整个数据集的标签集合，但是切分测试集的时候，某些标签数量很少，可能会被去掉，这里要剔除掉这些标签
    y_test_set = set(y_test)
    y_test_list = list(y_test_set)
    attacks_test = []
    for i in range(0, len(y_test_set)):
        attacks_test.append(attacks[y_test_list[i]])
    p = PlotConfusionMatrix()
    p.prepareWork(attacks_test, y_test, y_pred)
 
# 绘制混淆矩阵图形，attacks是标签列表，y_test是测试结果，y_pred是预测结果
plotMatrix(attacks,y_test,y_pred)