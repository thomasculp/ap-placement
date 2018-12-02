import numpy as np

# uniform distribution - ideal where noise is not an issue
x = np.ones((5, 10))
# print(x)

# random clusters - brain break
y = np.random.randint(8, size=(5,10)).astype('uint8')
# print(y)

# future VR/AR - 5 times the bandwidth https://venturebeat.com/2017/05/06/the-bandwidth-problem-5-issues-the-vr-industry-must-resolve/
z = np.random.randint(8, 45, size=(5,10)).astype('uint8')
# print(z)

# one strip of high usage - office hours
a = np.random.randint(2, size=(5,10)).astype('uint8')
a[0] =  8
# print(a)

# high uniform distribution - meal times
b = np.zeros((5, 10))
b.fill(4)
# print(b)
