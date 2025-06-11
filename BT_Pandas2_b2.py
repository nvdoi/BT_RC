import pandas as pd
import numpy as np

df_nv = pd.DataFrame({
    'ID': [101, 102, 103, 104, 105, 106],
    'Name': ['An', 'Bình', 'Cường', 'Dương', np.nan, 'Hạnh'],
    'Age': [25, np.nan, 30, 22, 28, 35],
    'Department': ['HR', 'IT', 'IT', 'Finance', 'HR', np.nan],
    'Salary': [700, 800, 750, np.nan, 710, 770]
})

df_pb = pd.DataFrame({
    'Department': ['HR', 'IT', 'Finance', 'Marketing'],
    'Manager': ['Trang', 'Khoa', 'Minh', 'Lan']
})

print(df_nv.isnull())

df_nv = df_nv[df_nv.isnull().sum(axis=1) <= 2]

df_nv['Name'].fillna('Chưa rõ', inplace=True)
df_nv['Age'].fillna(df_nv['Age'].mean(), inplace=True)
df_nv['Salary'].fillna(method='ffill', inplace=True)
df_nv['Department'].fillna('Unknown', inplace=True)

df_nv['Age'] = df_nv['Age'].astype(int)
df_nv['Salary'] = df_nv['Salary'].astype(int)

df_nv['Salary_after_tax'] = df_nv['Salary'] * 0.9

filtered = df_nv[(df_nv['Department'] == 'IT') & (df_nv['Age'] > 25)]
print(filtered)

sorted_nv = df_nv.sort_values(by='Salary_after_tax', ascending=False)
print(sorted_nv)

grouped = df_nv.groupby('Department')['Salary'].mean()
print(grouped)

merged = pd.merge(df_nv, df_pb, on='Department', how='left')
print(merged)

df_new = pd.DataFrame({
    'ID': [107, 108],
    'Name': ['Nam', 'Thảo'],
    'Age': [27, 29],
    'Department': ['Marketing', 'IT'],
    'Salary': [780, 760]
})

df_new['Salary_after_tax'] = df_new['Salary'] * 0.9

df_all = pd.concat([df_nv, df_new], ignore_index=True)
print(df_all)
