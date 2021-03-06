# -*- coding:utf-8 -*-
# ##################################################
# 函数：LU分解，QR分解， Householde约简，Givens约简
# 作者：余文艳(2015E8007361074)
# 日期：2016.5.17
# 输入：矩阵A
# 输出：所选择矩阵A对应分解或约简后的结果
# 实例：
# > 2 2 2; 4 7 7; 6 18 22               # for LU n*n
# > 0 -20 -14; 3 27 -4                  # for QR(GramSchidt) n*n
# > 1 1 0; 1 0 1                        # for QR(GramSchidt) m*n
# > 0 -20 -14; 3 27 -4; 4 11 -2         # for Householder and Givens
# > 1 19 -34; -2 -5 20; 2 8 37          # for LU QR Householder and Givens
# 支持特性：
# 1.对于LU支持n*n矩阵
# 2.对于QR，Householder,Givens均支持m*n矩阵
# 3.支持浮点型运算
# ###################################################
from numpy import matrix
from math import sqrt


def lu_factor(data):
    A = data
    print "***********下面进行LU分解***********"
    [n,n] = A.shape
    # print A[1, 1]
    # print n
    # Create zero matrices for L and U
    L = matrix([[0.0] * n for i in xrange(n)])
    U = matrix([[0.0] * n for i in xrange(n)])    
    for j in xrange(n):
        # L的所有对角元素都置为1
        L[j, j] = 1.0
        # LaTex: u_{i,j} = a_{i,j} - \sum_{k =1}^{i-1} u_{kj} l_{ik}
        for i in xrange(j + 1):
            s1 = sum(U[k, j] * L[i, k] for k in xrange(i))
            U[i, j] = A[i, j] - s1
        # LaTex: l_{ij} = \frac{1}{u_{jj}} (a_{ij}- \sum_{k=1}^{j-1} u_{kj} l_{ik})
        for i in xrange(j, n):
            s2 = sum(U[k, j] * L[i, k] for k in xrange(j))
            L[i, j] = (A[i, j] - s2) / U[j, j]
    print "分解公式：A = LU "
    print "相应的A矩阵为：\n", A
    print "相应的L矩阵为：\n", L
    print "相应的U矩阵为：\n", U
    print "************************************"
    return (L, U)


def qr_factor(data):
    A = data
    print "***********下面进行QR(GramSchidt)分解***********"
    [m, n] = A.shape
    #print [m, n]
    Q = matrix([[0.0] * n for i in xrange(m)])
    R = matrix([[0.0] * n for i in xrange(n)])
    
    for k in xrange(1, n + 1):
        if k == 1:
            r11 = sqrt(sum(x_i**2 for x_i in A[:,0] )) #求r11的模
            q1 = A[:,0] / r11
            Q[:,0] = q1
            R[0,0] = r11
        else:
            ak = A[:,k-1] # 初始化ak 为A中的第k个列向量
            for l in xrange(k-1):
                R[l, k-1] = ak.T * Q[:, l]
                ak = ak - R[l, k-1] * Q[:, l]
            q = ak
            R[k-1, k-1] = sqrt(sum(x_i**2 for x_i in q)) #求q的模，并放在R矩阵的相应位置
            Q[:, k-1] = q / R[k-1, k-1] # 对矩阵Q的第k个列向量进行归一化操作
    print "分解公式：A = QR "
    print "相应的A矩阵为：\n", A
    print "相应的Q矩阵为：\n", Q
    print "相应的R矩阵为：\n", R
    print "************************************"
    return (Q, R)


def householder_reduction(data):
    A = data
    print "**********Householder_reduction***********"
    [m, n] = A.shape
    
    #初始化R矩阵
    R = matrix([[0.0] * n for i in xrange(m)])
    #生成对应size的单位矩阵
    I = matrix([[float( i == j) for i in xrange(n)] for j in xrange(n)])
    R0 = I # R0作为循环的中间变量
    e1 = I[:,0]
    for k in xrange(1, n):
        if k == 1:
            u1 = A[:, 0] - sqrt(sum(x_i**2 for x_i in A[:, 0])) * e1
            R1 = I - 2*u1*u1.T/(u1.T*u1)
            R = R1
            a = R1*A
    #        print "---------k=%d-----------------------------" % k
    #        print "A=\n",A
    #        print "R1=\n",R1
    #        print "R1A=\n",R1*A
        else:
            Ak = a[k-1:m,k-1:n]
            l = len(Ak)
            #生成相应size的单位矩阵
            I_l = matrix([[float( i == j) for i in xrange(l)] for j in xrange(l)])
            uk = Ak[:,0] -sqrt(sum(x_i**2 for x_i in Ak[:,0]))*I_l[:,0]
            rk = I_l - 2 * uk *uk.T/(uk.T*uk)
            Rk = R0
            Rk[k-1:m,k-1:n] = rk
            a = Rk * a
            R = Rk*R
    #        print "---------k=%d----------------------------" % k
    #        print "R%d=\n" % k,Rk
    #        print "R%d*..*R1A=\n" % k,a

    P = R
    T = R * A

    print "约简公式：PA = T "
    print "相应的A矩阵为：\n", A
    print "相应的P矩阵为：\n", P
    print "相应的T矩阵为：\n", T
    print "************************************"
    return (P, T)

def givens_reduction(data):
    A = data
    print "**********Givens_reduction***********"
    [m, n] = A.shape # 获得矩阵的大小
    #初始化Q矩阵
    Q = matrix([[float( i == j) for i in xrange(m)] for j in xrange(m)])
    a = A # 初始化a
    xk = a[:,0] # 初始化xk为a 的第一个列向量
    for k in xrange(1,n):
        Ak = a[k-1:m, k-1:n] #选取相应的子矩阵
        xk = Ak[:, 0] # 更新xk为Ak的第一个列向量
        [n1, n2] = Ak.shape
        Qm = matrix([[float(i==j) for i in xrange(n1)] for j in xrange(n1)])
        for m in xrange(2, n1 + 1):
            q = matrix([[float(i==j) for i in xrange(n1)] for j in xrange(n1)])
            q[0, 0] = xk[0]/sqrt(xk[0]**2 + xk[m-1]**2)
            q[0, m-1] = xk[m-1] / sqrt(xk[0]**2 + xk[m-1]**2)
            q[m-1, 0] = -xk[m-1] /sqrt(xk[0]**2 + xk[m-1]**2)
            q[m-1, m-1] = xk[0]/ sqrt(xk[0]**2 + xk[m-1]**2)
            Ak = q*Ak # 更新a 为R(ij) * a
            xk = Ak[:, 0] #更新xk 为R(ij)*a之后的第一列
            Qm= q * Qm
        a = Ak
        Qk = matrix([[float(i == j) for i in xrange(n)] for j in xrange(n)])
        Qk[k-1:n,k-1:n] = Qm # 对n>=2时的R进行更新操作
        Q = Qk * Q
    T = Q * A
    print "约简公式：QA = T "
    print "相应的A矩阵为：\n", A
    print "相应的Q矩阵为：\n", Q
    print "相应的T矩阵为：\n", T
    print "************************************"
    return (Q, T)

print "温馨提示：1.请保证您正处于英文输入状态 2.请您参照下面给出的说明进行相应操作"
print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
print "请您选择所需要进行的变换：（输入变换前的阿拉伯数字即可1、2、3、4）"
print "【1】LU 分解"
print "【2】QR 分解"
print "【3】Householder 约简"
print "【4】Givens 约简"

inputNum = int(raw_input("请选择："))
print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
# print inputNum

inputMatrix = raw_input("请输入一个矩阵：（同一行元素用空格隔开，不用行用分号隔开，例如：1 2 3; 3 4 5; 6 7 8）>")
if not inputMatrix.strip():
    inputMatrix = raw_input("输入矩阵不能为空,请重新输入> ")

inputMatrix = inputMatrix.split(';')

data = []
for ele in inputMatrix:
    data.append(map(float, ele.strip().split(' ')))

# data = ('2 2 2; 4 7 7; 6 18 22') # for LU n*n
# data = ('0 -20 -14; 3 27 -4')  # for QR(GramSchidt) n*n
# data = ('1 1 0; 1 0 1') for QR(GramSchidt) m*n
# data = ('0 -20 -14; 3 27 -4; 4 11 -2') # for Householder and Givens
# data = ('1 19 -34; -2 -5 20; 2 8 37') # for LU QR Householder and Givens
data = matrix(data)

if inputNum == 1:
    lu_factor(data)
elif inputNum == 2:
    qr_factor(data)
elif inputNum == 3:
    householder_reduction(data)
elif inputNum == 4:
    givens_reduction(data)
