"""
该脚本的功能是下载MNIST数据集，
统计每个数字类别的样本数量，
并使用柱状图和饼图对统计结果进行可视化。
"""
from torchvision import datasets
import matplotlib.pyplot as plt

# 下载 MNIST 数据集
mnist_data = datasets.MNIST(root='../data', train=True, download=True)

# 初始化一个字典来统计每个数字的样本数量
digit_counts = {i: 0 for i in range(10)}

# 遍历数据集
for _, label in mnist_data:
    digit_counts[label] += 1

# 打印每个类别的数量
total_count = sum(digit_counts.values())
print("Digit Counts:")
for digit, count in digit_counts.items():
    print(f"Digit {digit}: {count} samples")

print(f"Total Samples: {total_count}")

# 准备数据
digits = list(digit_counts.keys())
counts = list(digit_counts.values())

# 绘制柱状图
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.bar(digits, counts, color='skyblue')
plt.title('MNIST Digit Count (Bar Chart)')
plt.xlabel('Digits')
plt.ylabel('Number of Samples')
plt.xticks(digits)

# 绘制饼图
plt.subplot(1, 2, 2)
plt.pie(counts, labels=digits, autopct='%1.1f%%', startangle=140)
plt.title('MNIST Digit Count (Pie Chart)')

plt.tight_layout()
plt.show()
