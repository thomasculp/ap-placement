import numpy as np

# uniform distribution - ideal where noise is not an issue
x = np.ones((5, 10))
# print(x)

# random clusters - brain break
L = list()
for i in range(5):
    y = np.random.randint(8, size=(5, 10)).astype('uint8')
    y = y.tolist()
    L.append(y)

# print(L)

# future VR/AR - 5 times the bandwidth https://venturebeat.com/2017/05/06/the-bandwidth-problem-5-issues-the-vr-industry-must-resolve/
L2 = list()
for i in range(5):
    z = np.random.randint(8, 45, size=(5, 10)).astype('uint8')
    z = z.tolist()
    L2.append(z)
# print(L2)

# one strip of high usage - office hours
L3 = list()
for i in range(5):
    a = np.random.randint(5, size=(5, 10)).astype('uint8')
    a[i] =  8
    a = a.tolist()
    L3.append(a)
# print(L3)

# high uniform distribution - meal times
L4 = list()
for i in range(4, 9):
    b = np.zeros((5, 10))
    b.fill(i)
    b = b.tolist()
    L4.append(b)
# print(L4)
