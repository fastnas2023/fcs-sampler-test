from fcsparser import parse
import numpy as np
from datetime import datetime
import fcswrite

# 读取原始FCS文件
file_path = 'test-0-100W.fcs'
meta, data = parse(file_path)

# 设置起始和结束位置
start_cell = 200000  # 第20万个细胞
end_cell = 300000   # 第30万个细胞
n_cells = end_cell - start_cell  # 总共导出10万个细胞

# 检查数据是否足够
if len(data) < end_cell:
    raise ValueError(f"原文件只包含{len(data)}个细胞，少于请求的{end_cell}个细胞")

# 截取指定范围的细胞数据
new_data = data.iloc[start_cell:end_cell]

# 获取通道信息
num_params = meta['$PAR']
channels = []
channel_ranges = []
channel_bits = []
channel_types = []

# 收集每个通道的详细信息
for i in range(1, num_params + 1):
    # 通道名称（确保名称兼容）
    channel_name = meta[f'$P{i}N']
    channel_name = channel_name.replace('/', '_').replace('\\', '_')  # 替换可能的非法字符
    channels.append(channel_name)
    # 通道范围
    channel_ranges.append(float(meta.get(f'$P{i}R', '1024')))
    # 数据位数
    channel_bits.append(int(meta.get(f'$P{i}B', '32')))
    # 数据类型
    pne_value = meta.get(f'$P{i}E', '0,0')
    channel_types.append('i' if ',' not in pne_value else 'f')  # 使用小写的数据类型标识符

# 打印形状信息进行调试
print(f"数据形状: {new_data.values.shape}")
print(f"通道数量: {len(channels)}")

# 确保数据是正确的形状
event_data = new_data.values.copy()  # 保持原始数据格式
print(f"数据类型: {event_data.dtype}")

# 生成输出文件名（包含起始和结束位置）
current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
output_path = f'output_{start_cell}-{end_cell}cells_{current_time}.fcs'

# 准备必要的元数据
text_kw = {
    '$FIL': output_path,
    '$TOT': str(n_cells),
    '$PAR': str(num_params),
    '$BYTEORD': '1,2,3,4',  # 小端字节序
    '$DATATYPE': 'F' if np.issubdtype(event_data.dtype, np.floating) else 'I',
    '$MODE': 'L',
    '$NEXTDATA': '0'
}

# 添加通道相关的元数据
for i, (name, range_val, bits) in enumerate(zip(channels, channel_ranges, channel_bits), 1):
    text_kw[f'$P{i}N'] = name
    text_kw[f'$P{i}R'] = str(range_val)
    text_kw[f'$P{i}B'] = str(bits)

# 写入新的FCS文件
fcswrite.write_fcs(
    filename=output_path,
    chn_names=channels,
    data=event_data,
    text_kw_pr=text_kw  # 使用新构建的元数据
)

print(f"成功导出第{start_cell}到第{end_cell}个细胞到{output_path}")
print("通道信息:")
for i, (name, range_val, bits, dtype) in enumerate(zip(channels, channel_ranges, channel_bits, channel_types), 1):
    print(f"通道 {i}: {name}, 范围: {range_val}, 位数: {bits}, 类型: {dtype}")