# separate a .nii file into a series of .png images

import nibabel as nib
import os
import matplotlib.pyplot as plt
import gzip
import shutil


def read_niifile(niifile):  # 读取niifile文件
    img = nib.load(niifile)  # 下载niifile文件（其实是提取文件）
    img_fdata = img.get_fdata()  # 获取niifile数据
    return img_fdata


def save_fig(file, save_dir):  # 保存为图片
    fdata = read_niifile(file)  # 调用上面的函数，获得数据
    print(fdata.shape)
    # (x, y, z, p) = fdata.shape  # 获得数据shape信息：（长，宽，维度-切片数量）
    (x, y, z) = fdata.shape
    if os.path.exists(save_dir + '/x') == 0:
        os.makedirs(save_dir + '/x')  # 创建文件夹
    if os.path.exists(save_dir + '/y') == 0:
        os.makedirs(save_dir + '/y')  # 创建文件夹
    if os.path.exists(save_dir + '/z') == 0:
        os.makedirs(save_dir + '/z')  # 创建文件夹

    for k in range(x):
        if 30 <= k <= 160 and k % 10 == 0:
            slice = fdata[k, :, :]  # 三个位置表示三个不同角度的切片
            plt.imsave(os.path.join(save_dir + '/x', '{}.png'.format(k)), slice, cmap='gray')

    for k in range(y):
        if 40 <= k <= 190 and k % 10 == 0:
            slice = fdata[:, k, :]  # 三个位置表示三个不同角度的切片
            plt.imsave(os.path.join(save_dir + '/y', '{}.png'.format(k)), slice, cmap='gray')

    for k in range(z):
        if 110 <= k <= 190 and k % 5 == 0:
            slice = fdata[:, :, k]  # 三个位置表示三个不同角度的切片
            plt.imsave(os.path.join(save_dir + '/z', '{}.png'.format(k)), slice, cmap='gray')
        # imageio.imwrite(os.path.join(savepicdir, '{}.png'.format(k)), slice)
        # cv2.imwrite(os.path.join(savepicdir, '{}.jpeg'.format(k)), slice)
        # 将切片信息保存为png格式


dataset_path = './data/ds004173-download/'
folders = [f for f in os.listdir(dataset_path) if 'sub' in f]
ls_of_gz = []
for f in folders:
    f = dataset_path + f + '/anat/'
    for d in os.listdir(f):
        if '.gz' in d:
            ls_of_gz.append(f + d)
ls_of_motion = []
ls_of_std = []
for gz in ls_of_gz:
    if 'standard' in gz:
        ls_of_std.append(gz)
    else:
        ls_of_motion.append(gz)

dir_motion_corrupted = './data/motion-corrupted'
if os.path.exists(dir_motion_corrupted) == 0:
    os.makedirs(dir_motion_corrupted)
    for gz in ls_of_motion:
        with gzip.open(gz, 'rb') as f_in:
            with open(dir_motion_corrupted + '/' + gz[45:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

dir_standard = './data/standard'
if os.path.exists(dir_standard) == 0:
    os.makedirs(dir_standard)
    for gz in ls_of_std:
        with gzip.open(gz, 'rb') as f_in:
            with open(dir_standard + '/' + gz[45:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)


nii_dir = './data/motion-corrupted'
slice_dir = './data/slices/motion-corrupted'
if os.path.exists(slice_dir) == 0:
    os.makedirs(slice_dir)
    for nii in os.listdir(nii_dir):
        path = os.path.join(slice_dir, nii[:6])
        if os.path.exists(path) == 1:
            path = path + '_1'
        os.makedirs(path)
        save_fig(os.path.join(nii_dir, nii), path)

nii_dir = './data/standard'
slice_dir = './data/slices/standard'
if os.path.exists(slice_dir) == 0:
    os.makedirs(slice_dir)
    for nii in os.listdir(nii_dir):
        path = os.path.join(slice_dir, nii[:6])
        if os.path.exists(path) == 1:
            path = path + '_1'
        os.makedirs(path)
        save_fig(os.path.join(nii_dir, nii), path)

path = './data/sub-440735_acq-headmotion2_T1w.nii'  # nii的路径
savepicdir = './data/slices/motion'  # 保存png的路径
if os.path.exists(savepicdir) == 0:
    os.makedirs(savepicdir)  # 创建文件夹
    save_fig(path, savepicdir)  # 运行程序，保存为图像


path = './data/sub-440735_acq-standard_T1w.nii'  # nii的路径
savepicdir = './data/slices/standard'  # 保存png的路径
if os.path.exists(savepicdir) == 0:
    os.makedirs(savepicdir)  # 创建文件夹
    save_fig(path, savepicdir)  # 运行程序，保存为图像


