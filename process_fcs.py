from fcsparser import parse
import flowio
import numpy as np
from datetime import datetime

# 读取原始FCS文件
file_path = 'test-0-100W.fcs'
meta, data = parse(file_path)

# 设置参数
start_cell = 100000  # 从第10万个细胞开始
step = 3  # 每3个取1个

# 使用切片操作选择数据，格式为 [start:end:step]
new_data = data.iloc[start_cell::step]

# 获取实际导出的细胞数量
n_cells = len(new_data)
end_cell = start_cell + (n_cells - 1) * step  # 计算最后一个细胞的位置

# 获取通道名称和参数数量
num_params = meta['$PAR']
channels = [meta[f'$P{i}N'] for i in range(1, num_params + 1)]

# 打印形状信息进行调试
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

# 生成输出文件名（包含起始位置和步长信息）
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
output_path = f'output_start{start_cell}_step{step}_{current_time}.fcs'

# 写入新的FCS文件
with open(output_path, 'wb') as f:
    flow_data = flowio.create_fcs(
        f,                      # 文件句柄
        event_data=event_data,  # 展平的事件数据
        channel_names=channels  # 通道名称
    )

print(f"成功导出从第{start_cell}个细胞开始，每{step}个取1个，共{n_cells}个细胞到{output_path}")
print(f"最后一个导出的细胞位置: {end_cell}")