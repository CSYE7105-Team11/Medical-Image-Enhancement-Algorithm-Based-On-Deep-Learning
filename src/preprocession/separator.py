# separate a .nii file into a series of .png images

import nibabel as nib
import os
import matplotlib.pyplot as plt


def read_niifile(niifile):  # 读取niifile文件
    img = nib.load(niifile)  # 下载niifile文件（其实是提取文件）
    img_fdata = img.get_fdata()  # 获取niifile数据
    return img_fdata


def save_fig(file):  # 保存为图片
    fdata = read_niifile(file)  # 调用上面的函数，获得数据
    print(fdata.shape)
    # (x, y, z, p) = fdata.shape  # 获得数据shape信息：（长，宽，维度-切片数量）
    (x, y, z) = fdata.shape
    if os.path.exists(savepicdir + '/x') == 0:
        os.makedirs(savepicdir + '/x')  # 创建文件夹
    if os.path.exists(savepicdir + '/y') == 0:
        os.makedirs(savepicdir + '/y')  # 创建文件夹
    if os.path.exists(savepicdir + '/z') == 0:
        os.makedirs(savepicdir + '/z')  # 创建文件夹

    for k in range(x):
        slice = fdata[k, :, :]  # 三个位置表示三个不同角度的切片
        plt.imsave(os.path.join(savepicdir + '/x', '{}.jpeg'.format(k)), slice, cmap='gray')

    for k in range(y):
        slice = fdata[:, k, :]  # 三个位置表示三个不同角度的切片
        plt.imsave(os.path.join(savepicdir + '/y', '{}.jpeg'.format(k)), slice, cmap='gray')

    for k in range(z):
        slice = fdata[:, :, k]  # 三个位置表示三个不同角度的切片
        plt.imsave(os.path.join(savepicdir + '/z', '{}.jpeg'.format(k)), slice, cmap='gray')
        # imageio.imwrite(os.path.join(savepicdir, '{}.png'.format(k)), slice)
        # cv2.imwrite(os.path.join(savepicdir, '{}.jpeg'.format(k)), slice)
        # 将切片信息保存为png格式


dir = './data/sub-440735_acq-standard_T1w.nii'  # nii的路径
savepicdir = './data/slices/standard'  # 保存png的路径
if os.path.exists(savepicdir) == 0:
    os.makedirs(savepicdir)  # 创建文件夹
save_fig(dir)  # 运行程序，保存为图像


# index  = 0
# while index <= 143:
#     dir = '/home/quindex/Downloads/niis/' + str(index).zfill(3) + '.nii'  # nii的路径
#     savepicdir = '/home/quindex/Downloads/slices/' + str(index).zfill(3)  # 保存png的路径
#     if (os.path.exists(savepicdir) == 0):
#         os.mkdir(savepicdir)  # 创建文件夹
#     save_fig(dir)  # 运行程序，保存为图像
#     index += 1
