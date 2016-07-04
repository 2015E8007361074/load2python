# coding=utf-8"""Create on June 25,2016kNN:k Nearest Neighbors@author:Wayne<。)#)))≦"""from numpy import *import operator  # 运算符模块from os import listdirdef create_data_set():    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])    labels = ['A', 'A', 'B', 'B']    return group, labelsdef classify0(inx, data_set, labels, k):    data_set_size = data_set.shape[0]    diff_mat = tile(inx, (data_set_size, 1)) - data_set  # tile实现重复AB次    sq_diff_mat = diff_mat ** 2    # print sq_diff_mat    sq_distance = sq_diff_mat.sum(axis=1)  # sum(axis =1)讲矩阵的每一行相加    # print sq_distance    distances = sq_distance ** 0.5    # print distances    sorted_dist_indicies = distances.argsort()  # argsort()函数返回数组从小到大的索引值    # print sorted_dist_indicies    class_count = {}    for i in range(k):        vote_i_label = labels[sorted_dist_indicies[i]]        class_count[vote_i_label] = class_count.get(vote_i_label, 0) + 1    # print class_count    sorted_class_count = sorted(class_count.iteritems(), key=operator.itemgetter(1), reverse=True)    return sorted_class_count[0][0]def file_to_matrix(filename):    fr = open(filename)    arrayOLines = fr.readlines()    numberOfLines = len(arrayOLines)  # 得到文件的行数    returnMat = zeros((numberOfLines, 3))  # 创建返回的NumPy矩阵    classLabelVector = []    index = 0    for line in arrayOLines:        line = line.strip()        listFromLine = line.split('\t')        returnMat[index, :] = listFromLine[0: 3]        classLabelVector.append(int(listFromLine[-1]))        index += 1    return returnMat, classLabelVectordef autoNorm(dataSet):    minVals = dataSet.min(0)    maxVals = dataSet.max(0)    ranges = maxVals - minVals    normDataSet = zeros(shape(dataSet))    m = dataSet.shape[0]  # 获得矩阵的行数    normDataSet = dataSet - tile(minVals, (m, 1))  # oldValue - min    normDataSet = normDataSet/tile(ranges, (m, 1))    return normDataSet, ranges, minValsdef datingClassTest():    hoRatio = 0.10    datingDataMat, datingLabels = file_to_matrix('datingTestSet2.txt')    normMat, ranges, minVals = autoNorm(datingDataMat)    m = normMat.shape[0]    numTestVecs = int(m*hoRatio)    errorCount = 0    for i in range(numTestVecs):        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3 )        print "分类器分类结果是：%d，真实类别是：%d" % (classifierResult, datingLabels[i])        if(classifierResult != datingLabels[i]): errorCount += 1.0    print "分类错误率是：%f" %(errorCount /float(numTestVecs))def img_to_vector(filename):    return_vector = zeros((1, 1024))    fr = open(filename)    for i in range(32):        line_str = fr.readline()        for j in range(32):            return_vector[0, 32*i + j] = int(line_str[j])    return return_vectordef hand_writing_class_test():    hw_labels = []    training_file_list = listdir('digits/trainingDigits')    m = len(training_file_list)    training_matrix = zeros((m, 1024))    for i in range(m):        file_name_str = training_file_list[i]        file_str = file_name_str.split('.')[0]        class_num_str = int(file_str.split('_')[0])        hw_labels.append(class_num_str)        training_matrix[i, :] = img_to_vector('digits/trainingDigits/%s' % file_name_str)    test_file_list = listdir('digits/testDigits')    error_count = 0.0    mtest = len(test_file_list)    for i in range(mtest):        file_name_str = test_file_list[i]        file_str = file_name_str.split('.')[0]        class_num_str = int(file_str.split('_')[0])        vector_under_test = img_to_vector('digits/testDigits/%s' % file_name_str)        classifier_result = classify0(vector_under_test, training_matrix, hw_labels, 3)        print "分类器识别手写样本为：%d， 样本真实数字为：%d" % (classifier_result, class_num_str)        if classifier_result != class_num_str:            error_count += 1.0    print "总的分类错误数目：%d" % error_count    print "分类错误率为：%f" % (error_count / float(mtest))