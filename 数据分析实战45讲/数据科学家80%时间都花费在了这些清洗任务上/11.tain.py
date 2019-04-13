#!usr/bin/python3
# -*- coding:utf-8 -*-

import os
import numpy as np
import pandas as pd


path = '/Users/albert.ming.xu/Downloads/11.data.xlsx'
new_path = os.path.splitext(path)[0] + '_new' + os.path.splitext(path)[1]
data_type = {'food': np.str, 'ounces': np.float, 'animal': np.str}

df = pd.read_excel(path, sheet_name=0, header=0, dtype=data_type)

# 统一food名称为小写字母
df['food'] = df['food'].str.lower()
# 单位取绝对值
df['ounces'] = df['ounces'].abs()
# 将ounces列的空行填充为平均值
df['ounces'].fillna(df['ounces'].mean(), inplace=True)
# 删除任意字段包含空值的数据
df.dropna(how='any', axis=0, inplace=True)
# 删除food字段出现重复的行，但bacon最后会存在三行数据，ounces分别是4.0、5.31、8.0，最后保留哪个数据更好是个问题
df.drop_duplicates('food', inplace=True)

df.to_excel(new_path, float_format="%.2f")

