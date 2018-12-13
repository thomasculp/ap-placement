import numpy as np

# defining the size of the kirkland dhall (both in grid size and meters, given
# we're taking those units to be the exact same)
s = (20, 40)

# random clusters - brain break
random_clusters = []
for i in range(5):
    y = np.random.randint(8, size=s).astype('uint8')
    random_clusters.append(y)


# future VR/AR - 5 times the bandwidth https://venturebeat.com/2017/05/06/the-bandwidth-problem-5-issues-the-vr-industry-must-resolve/
future = []
for i in range(5):
    z = np.random.randint(8, 45, size=s).astype('uint8')
    future.append(z)


# one strip of high usage - office hours
office_hours = []
for i in range(5):
    a = np.random.randint(5, size=s).astype('uint8')
    a[i] =  8
    office_hours.append(a)


# high uniform distribution - meal times
uniform = []
for i in range(4, 9):
    b = np.zeros(s)
    b.fill(i)
    uniform.append(b)
