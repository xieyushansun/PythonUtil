import os
txt_path = r"C:\Users\DF\Desktop\newLabel"
txt_list = os.listdir(txt_path)

classes = [0] * 5


for txt_name in txt_list:
    with open(os.path.join(txt_path, txt_name)) as f:
        for line in f.readlines():
            index = int(line.split(" ")[0]) - 1
            classes[int(line.split(" ")[0]) - 1] += 1

for i in range(0, 5):
    print("第", i+1, "类：", classes[i])