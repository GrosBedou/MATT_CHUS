import scipy.io

mat_file = 'seebit-10_2022_06_06_16_16_15_1.mat'

mat_contents = scipy.io.loadmat(mat_file)
print(mat_contents)