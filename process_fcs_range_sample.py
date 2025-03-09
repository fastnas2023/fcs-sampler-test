from fcsparser import parse
import flowio
import numpy as np
from datetime import datetime

def sample_cells(raw_data, range_start, range_end, target_count, mode='continuous'):
    """
    细胞采样函数
    mode: 采样模式 - 'continuous'（连续）, 'interval'（间隔）, 'random'（随机）
    """
    cells_in_range = raw_data.iloc[range_start:range_end]
    range_count = len(cells_in_range)
    
    if mode == 'continuous':
        # 连续采样：直接取前target_count个细胞
        sampled_cells = cells_in_range.iloc[:target_count]
        sample_desc = f"连续采样前{target_count}个细胞"
        
    elif mode == 'interval':
        # 间隔采样：计算所需间隔
        interval = range_count // target_count
        sampled_cells = cells_in_range.iloc[::interval]
        sample_desc = f"每{interval}个细胞采样1个"
        
    elif mode == 'random':
        # 随机采样：随机选择target_count个细胞
        random_indices = np.random.choice(range_count, target_count, replace=False)
        random_indices.sort()  # 排序以保持细胞顺序
        sampled_cells = cells_in_range.iloc[random_indices]
        sample_desc = f"随机采样{target_count}个细胞"
        
    else:
        raise ValueError("不支持的采样模式")
        
    return sampled_cells, sample_desc

# 读取FCS文件
source_file = 'test-0-100W.fcs'
metadata, raw_data = parse(source_file)

# 显示源文件信息
cell_count = len(raw_data)
print(f"源文件细胞总数: {cell_count}")

# 采样参数设置
range_start = 100000    # 起始位置：第10万个细胞
range_end = 400000     # 结束位置：第40万个细胞
target_count = 100000  # 目标采样数量：10万个细胞
sample_mode = 'interval'  # 采样模式：'continuous', 'interval', 'random'

# 执行采样
sampled_cells, sample_desc = sample_cells(
    raw_data, 
    range_start, 
    range_end, 
    target_count, 
    sample_mode
)

# 显示采样结果
print(f"\n采样结果:")
print(f"采样范围: {range_start}-{range_end}")
print(f"采样模式: {sample_mode}")
print(f"采样方式: {sample_desc}")
print(f"采样后细胞数: {len(sampled_cells)}")

# 获取参数信息
param_count = metadata['$PAR']
param_names = [metadata[f'$P{i}N'] for i in range(1, param_count + 1)]

# 数据验证
print(f"\n数据验证:")
print(f"参数数量: {param_count}")
print(f"采样数据形状: {sampled_cells.values.shape}")
first_five = [range_start + i*sample_interval for i in range(5)]
print(f"前5个采样位置: {first_five}")

# 准备输出数据
cell_data = sampled_cells.values.flatten()
if not np.issubdtype(cell_data.dtype, np.floating):
    cell_data = cell_data.astype(np.float32)

# 更新元数据
output_metadata = metadata.copy()
output_metadata['$TOT'] = len(sampled_cells)

# 生成输出文件名
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f'sampled_{range_start}-{range_end}_mode{sample_mode}_{timestamp}.fcs'

# 写入新文件
with open(output_file, 'wb') as f:
    flow_data = flowio.create_fcs(
        f,
        event_data=cell_data,
        channel_names=param_names
    )

print(f"\n文件导出:")
print(f"已将{range_start}-{range_end}范围内每{sample_interval}个细胞采样1个")
print(f"共导出{len(sampled_cells)}个细胞到文件: {output_file}") 