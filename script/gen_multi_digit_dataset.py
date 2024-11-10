"""
MNIST多位数字图像生成脚本

此脚本用于生成包含多个MNIST数字的合成图像，以创建自定义图像数据集。它使用MNIST数据集，随机选择数字图像并组合在一起，
生成2位数或3位数的图像。生成的图像经过调整大小后，保存在指定文件夹中，并生成一个CSV文件记录图像文件名及对应的标签。
"""

from torchvision import datasets
import random
import os
import csv
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

class MNISTDigitGenerator:
    def __init__(self, mnist_data, x_offset_min=-3, x_offset_max=1, y_offset_min=-8, y_offset_max=5):
        self.mnist_data = mnist_data
        self.x_offset_max = x_offset_max
        self.x_offset_min = x_offset_min
        self.y_offset_max = y_offset_max
        self.y_offset_min = y_offset_min

    def crop_digit_image(self, digit_image, padding=2):
        """裁剪数字图像，去掉黑边，并增加一些边距"""
        bbox = digit_image.getbbox()  # 获取图像的边界框
        if bbox is not None:
            left = max(bbox[0] - padding, 0)
            top = max(bbox[1] - padding, 0)
            right = min(bbox[2] + padding, digit_image.width)
            bottom = min(bbox[3] + padding, digit_image.height)
            return digit_image.crop((left, top, right, bottom))  # 裁剪图像
        return digit_image  # 如果没有边界框，则返回原图

    def create_single_image(self, num_digits):
        """创建单个多位数字图像"""
        # 随机生成数字，确保第一位不为 0
        digits = [random.randint(1, 9)] + [random.randint(0, 9) for _ in range(num_digits - 1)]
        number = ''.join(map(str, digits))

        # 创建合成图像
        total_width = 28 * num_digits  # 每个数字宽度为 28
        max_height = 60
        image = Image.new('L', (total_width, max_height), color=0)  # 创建透明背景的图像

        current_x = 0
        for i, digit in enumerate(digits):
            # 获取 MNIST 数据集中对应数字的图像
            index = random.choice([j for j, (_, label) in enumerate(self.mnist_data) if label == digit])
            digit_image, _ = self.mnist_data[index]
            digit_image = self.crop_digit_image(digit_image)  # 裁剪数字图像
            
            # 随机调整 Y 轴的偏移量，范围可以自定义
            y_offset = random.randint(self.y_offset_min, self.y_offset_max)

            # 随机调整数字之间的间隙
            x_offset = 0
            if i != 0:  # 非第一位数字
                x_offset = random.randint(self.x_offset_min, self.x_offset_max)  # 随机空隙

            # 粘贴数字图像，考虑 Y 偏移
            image.paste(digit_image, (current_x, max_height // 2 + y_offset))  # Y 坐标基于中心对齐

            current_x += digit_image.width + x_offset  # 每个数字后增加一个固定间隔

        cropped_image = self.crop_digit_image(image)
        return cropped_image.resize((100, 50), Image.LANCZOS), number  # 返回调整后的图像和标签

    def save_images(self, images, labels, prefix=''):
        """保存生成的图像并另外保存标签"""
        if not os.path.exists('data/genData'):
            os.makedirs('data/genData')  # 创建文件夹以保存图像

        # 保存标签到 CSV 文件
        with open('data/mul/labels.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['filename', 'label'])  # 写入表头

            for idx, (img, label) in enumerate(zip(images, labels)):
                # 使用标签和索引生成唯一的文件名
                filename = f'{label}_{idx}.png'
                img.save(filename)  # 保存图像
                
                # 写入标签到 CSV 文件
                csv_writer.writerow([filename, label])  # 记录文件名和标签

    def create_multi_digit_images(self, num_digits, count):
        """创建多位数字图像数据集并保存"""
        images = []
        labels = []

        with ProcessPoolExecutor(max_workers=5) as executor:  # 设置合适的进程数
            futures = [executor.submit(self.create_single_image, num_digits) for _ in range(count)]
            for future in tqdm(futures, total=count, desc="Generating Images"):  # 使用 tqdm 监控进度
                image, label = future.result()
                images.append(image)
                labels.append(label)

        self.save_images(images, labels)  # 保存生成的图像
        return images, labels


if __name__ == '__main__':
    # 下载 MNIST 数据集
    mnist_data = datasets.MNIST(root='../data', train=True, download=True)

    # 创建生成器实例
    generator = MNISTDigitGenerator(mnist_data)

    generator.create_multi_digit_images(2, 50000)
    generator.create_multi_digit_images(3, 50000)
