import pandas as pd

data = {
    'Name': ['An', 'Như', 'Chi', 'Dũng', 'Hà', 'Huy', 'Lan', 'Minh', 'Ngọc', 'Tuấn'],
    'Age': [20, 21, 22, 20, 23, 21, 22, 20, 24, 22],
    'Gender': ['Male', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male'],
    'Score': [6.5, 7.0, 8.0, 4.5, 5.0, 9.0, 6.0, 3.5, 8.5, 5.5]
}

df_students = pd.DataFrame(data)

print("Toàn bộ dữ liệu:")
print(df_students)

print("\n3 dòng đầu tiên:")
print(df_students.head(3))

print("\nGiá trị tại index=2, cột Name:")
print(df_students.loc[2, 'Name'])

print("\nThử truy cập index=10, cột Age:")
if 10 in df_students.index:
    print(df_students.loc[10, 'Age'])
else:
    print("Index 10 không tồn tại trong DataFrame.")

print("\nCác cột Name và Score:")
print(df_students[['Name', 'Score']])

df_students['Pass'] = df_students['Score'] >= 5
print("\nThêm cột Pass:")
print(df_students)

df_sorted = df_students.sort_values(by='Score', ascending=False)
print("\nDataFrame sau khi sắp xếp theo điểm giảm dần:")
print(df_sorted)
