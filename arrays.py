import numpy as np

# defining the size of the kirkland dhall (both in grid size and meters, given
# we're taking those units to be the exact same)
s = (20, 40)

# random clusters - brain break
L1 = list()
for i in range(5):
    y = np.random.randint(8, size=s).astype('uint8')
    L1.append(y)

random_clusters = L1
#print(L)

# future VR/AR - 5 times the bandwidth https://venturebeat.com/2017/05/06/the-bandwidth-problem-5-issues-the-vr-industry-must-resolve/
L2 = list()
for i in range(5):
    z = np.random.randint(8, 45, size=s).astype('uint8')
    L2.append(z)

future = L2
#print(L2)

# one strip of high usage - office hours
L3 = list()
for i in range(5):
    a = np.random.randint(5, size=s).astype('uint8')
    a[i] =  8
    L3.append(a)

office_hours = L3
#print(L3)

# high uniform distribution - meal times
L4 = list()
for i in range(4, 9):
    b = np.zeros(s)
    b.fill(i)
    L4.append(b)

uniform = L4
#print(L4)

#for l in [L1, L2, L3, L4]:
#    for x in l:
#        print(x)
