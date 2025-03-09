from fcsparser import parse
import flowio
import numpy as np
from datetime import datetime

# 读取原始FCS文件
file_path = 'test-0-100W.fcs'
meta, data = parse(file_path)

# 打印原始文件信息
total_cells = len(data)
print(f"原始文件总细胞数: {total_cells}")

# 设置参数
start_cell = 100000  # 从第10万个细胞开始
end_cell = 400000   # 到第40万个细胞
step = 3            # 每3个取1个

# 先截取指定范围的数据
range_data = data.iloc[start_cell:end_cell]

# 然后在这个范围内每3个取1个
new_data = range_data.iloc[::step]

# 获取实际导出的细胞数量
n_cells = len(new_data)
last_cell_position = start_cell + (len(range_data) - 1)  # 范围内最后一个细胞的位置
expected_cells = len(range_data) // step  # 预期导出的细胞数

print(f"\n导出细胞详细信息:")
print(f"起始位置: {start_cell}")
print(f"结束位置: {end_cell}")
print(f"步长: {step}")
print(f"范围内总细胞数: {len(range_data)}")
print(f"实际导出细胞数: {n_cells}")
print(f"预期导出细胞数: {expected_cells}")

# 验证数据
print(f"\n数据验证:")
print(f"前5个选择的细胞位置: {[start_cell + i*step for i in range(5)]}")
print(f"是否符合预期数量: {'是' if n_cells == expected_cells else '否'}")

# 获取通道名称和参数数量
num_params = meta['$PAR']
channels = [meta[f'$P{i}N'] for i in range(1, num_params + 1)]

# 打印形状信息进行调试
print(f"\n数据形状信息:")
print(f"数据形状: {new_data.values.shape}")
print(f"通道数量: {len(channels)}")

# 确保数据是正确的形状
event_data = new_data.values.flatten()  # 将数据展平为一维数组
print(f"展平后的数据长度: {len(event_data)}")
print(f"是否为通道数的整数倍: {len(event_data) % len(channels) == 0}")

# 确定数据类型并转换数据
data_dtype = event_data.dtype
if not np.issubdtype(data_dtype, np.floating):
    event_data = event_data.astype(np.float32)

# 创建新的元数据
new_meta = meta.copy()
new_meta['$TOT'] = n_cells

# 生成输出文件名（包含范围和步长信息）
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
output_path = f'output_{start_cell}-{end_cell}_step{step}_{current_time}.fcs'

# 写入新的FCS文件
with open(output_path, 'wb') as f:
    flow_data = flowio.create_fcs(
        f,                      # 文件句柄
        event_data=event_data,  # 展平的事件数据
        channel_names=channels  # 通道名称
    )

print(f"\n导出结果:")
print(f"成功导出从第{start_cell}到第{end_cell}个细胞中，每{step}个取1个，共{n_cells}个细胞到{output_path}")