# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :yzm_xueqiu.py
@Author     :wooght
@Date       :2024/6/3 23:01
@Content    :雪球验证码
"""
import numpy
from PIL import Image, ImageFilter

# box_size = (183, 32, 567, 267)  # 300*400 分辨率
box_size = (996, 406, 1384, 644) # 1600 * 900

def move_pixel(num):
    im = Image.open('common/pic/xueqiu/{}.png'.format(str(num)))
    l_im = im.convert('L')  # 黑白
    box_im = l_im.crop(box_size)  # 窃取
    c_im = box_im.filter(ImageFilter.FIND_EDGES)  # 滤波器,边缘轮廓
    # c_im.show()
    img_arr = numpy.array(c_im)            # numpy 加载图像
    y_sum = img_arr[::, 7:80].sum(axis=1)  # 每行求和->根据前80列的值,筛选动图上,下边界
    row_line = []
    start_x1 = 7                 # 默认动图左边界
    left_block = 74              # 标记未再左边界74, 否则80
    start_x2 = 0                 # 动图右边界
    start_x3 = 0
    end_x1 = 0                   # 目标左边界
    end_x2 = 0                   # 目标右边界
    end_x3 = 0
    min_rgb = 6000               # 满足行和的最小值6000(灰度100*60个)
    # 筛选满足的行,不包括上下边界
    for i in range(1, img_arr.shape[0]-1):
        if y_sum[i] > min_rgb:
            row_line.append(i)
    if len(row_line) < 2: return False

    # 列和,起始位置为满足行往下
    x_sum = img_arr[row_line[0]:row_line[0] + 60, ::].sum(axis=0)
    column_line = []
    # 筛选满足的列, 不包括左右边界
    for i in range(1, img_arr.shape[1] - 1):
        if x_sum[i] > min_rgb:
            column_line.append(i)
    if len(x_sum) <= 2: return False
    print(row_line, column_line)
    # 动图起始位置有两种可能 7或者17(标记在左边界)
    # 遍历列   start_x1    start_x2 start_x3       end_x1   end_x2 end_x3
    for i in range(len(column_line)):
        current_l = column_line[i]
        if current_l < 50:
            if current_l == 7: continue
            if current_l > 10:
                left_block = 80
                start_x1 = current_l
        elif current_l < left_block:
            if not start_x2:
                start_x2 = current_l
            else:
                if current_l - start_x2 == 1:
                    start_x3 = current_l
        elif current_l < 300:
            if not end_x1:
                end_x1 = current_l
            elif not end_x2:
                if current_l - end_x1 == 1:
                    end_x2 = end_x1
                    end_x1 = 0
                    end_x3 = current_l
                else:
                    end_x2 = current_l
        else:
            if end_x2 and end_x3:break
            if not end_x1:
                end_x1 = current_l
            if not end_x2:
                end_x2 = current_l
            if not end_x3:
                if current_l - end_x2 == 1:
                    end_x3 = current_l
    print(start_x1, start_x2, start_x3, end_x1, end_x2, end_x3)
    # 最准确是右边界都有两个
    if start_x3 and end_x3:
        return end_x3 - start_x3
    elif start_x2 and end_x3:
        return end_x3 - start_x2
    elif start_x2 and end_x2:
        return end_x2 - start_x2
    elif end_x1:
        return end_x1 - start_x1
    else:
        return False

if __name__ == '__main__':
    print(move_pixel(15162))

"""
数据收集:
    7,66    75, 138
    7       171
    7,65    107,168
    7,69    281
    17,78   144,208
    7,69        281:282
    7,66    211,274
    7,66        263:264
    7,68    
    7,66:67     263:264
    7       171,234
"""