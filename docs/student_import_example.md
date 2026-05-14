# 学生批量导入示例

## 1. CSV 格式

文件名示例：

```text
students.csv
```

表头至少需要包含：

```csv
student_no,name,class_name
```

完整示例见同目录下的 [student_import_example.csv](D:/code/Time_Attendance/docs/student_import_example.csv)。

说明：

- `student_no`：学号，必须唯一
- `name`：学生姓名
- `class_name`：班级名称
- `is_active`：可选，支持 `true/false/1/0/yes/no`

## 2. ZIP 照片格式

文件名示例：

```text
photos.zip
```

压缩包内照片请直接使用学号命名，扩展名支持：

```text
.jpg .jpeg .png .bmp .webp
```

示例结构：

```text
photos.zip
├─ 20240001.jpg
├─ 20240002.png
└─ 20240003.jpeg
```

匹配规则：

- `20240001.jpg` 会自动匹配 CSV 中 `student_no=20240001` 的学生
- ZIP 中没有对应照片：学生档案照常导入，`feature_status=pending`
- ZIP 中同一学号有多张照片：该学生会导入成功，但照片处理记为失败
- ZIP 中多出的照片：会在返回结果里列入 `unmatched_photos`

## 3. 一次导入的推荐提交内容

```text
students.csv
photos.zip
```

这样系统会自动完成：

1. 批量创建学生档案
2. 自动生成/绑定学生账号
3. 批量导入照片
4. 自动提取人脸特征

## 4. 返回结果重点字段

- `created_count`：成功创建的学生数
- `photo_bound_count`：成功绑定并提取特征的照片数
- `photo_missing_count`：CSV 中学生缺少照片的数量
- `photo_failed_count`：照片存在但提取失败的数量
- `unmatched_photo_count`：ZIP 中未匹配到学生的照片数量
- `duplicate_photo_count`：ZIP 中重复学号照片数量
