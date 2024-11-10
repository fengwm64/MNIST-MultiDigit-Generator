"""
MNIST单位数字图像生成脚本
"""

from torchvision import datasets
from PIL import Image
import os
import random
import csv

# 下载并加载MNIST数据集
mnist_data = datasets.MNIST(root='../', train=True, download=True)

# 创建输出文件夹
output_dir = '../single'
os.makedirs(output_dir, exist_ok=True)

# 创建 CSV 文件路径
csv_file_path = os.path.join(output_dir, 'labels.csv')

# 设置背景和数字的尺寸
target_size = (100, 50)
digit_size = (40, 40)  # 放大MNIST数字图像的尺寸
margin = 2  # 设置安全边距，防止数字切边

# 打开 CSV 文件并写入标签
with open(csv_file_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['filename', 'label'])  # 写入CSV文件的表头
    
    # 遍历数据集并保存图片
    for idx, (img, label) in enumerate(mnist_data):
        # 将28x28的数字图像放大到40x40，并使用LANCZOS算法抗锯齿
        resized_digit = img.resize(digit_size, Image.LANCZOS)
        
        # 创建一个100x50的黑色背景
        background = Image.new('L', target_size, color=0)
        
        # 生成随机的粘贴位置，确保数字完整
        max_x = target_size[0] - digit_size[0] - margin
        max_y = target_size[1] - digit_size[1] - margin
        paste_x = random.randint(margin, max_x)
        paste_y = random.randint(margin, max_y)
        
        # 将放大的数字图像粘贴到随机位置
        background.paste(resized_digit, (paste_x, paste_y))
        
        # 创建文件名，例如 '5_1234.png'，表示标签为5，序号为1234
        filename = f'{label}_{idx}.png'
        
        # 保存图像到输出目录
        background.save(os.path.join(output_dir, filename))
        
        # 将文件名和标签写入 CSV 文件
        csv_writer.writerow([filename, label])

print(f"导出完成，所有图像已保存到 '{output_dir}' 文件夹中，标签信息保存到 '{csv_file_path}'。")
