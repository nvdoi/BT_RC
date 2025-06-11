import pandas as pd

data = {
    'Name': ['An', 'Bình', 'Cường', 'Dương', 'Hà', 'Hạnh', 'Khánh', 'Lan', 'Minh', 'Ngọc'],
    'Age': [20, 21, 19, 22, 20, 23, 21, 20, 22, 21],
    'Gender': ['M', 'F', 'M', 'M', 'F', 'F', 'M', 'F', 'M', 'F'],
    'Score': [6.5, 8.0, 4.5, 7.2, 9.0, 3.2, 5.5, 6.8, 4.0, 8.5]
}

df_students = pd.DataFrame(data)

print(df_students)

print(df_students.head(3))

print(df_students.loc[2, 'Name'])

print(df_students.loc[10, 'Age'] if 10 in df_students.index else "Index 10 không tồn tại.")

print(df_students[['Name', 'Score']])

df_students['Pass'] = df_students['Score'] >= 5
print(df_students)

df_sorted = df_students.sort_values(by='Score', ascending=False)
print(df_sorted)
