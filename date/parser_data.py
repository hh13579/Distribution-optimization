import gaosi as gs
import os
f_write = open('parser_data.txt', 'w+')
f_write_2 = open('xiaoqu_data_temp.txt', 'w+')
vis = []
id = 1
with open('./xiaoqu_data.txt',encoding='utf-8') as f:
    for line in f:
        if (len(line) < 2):
            continue
        line_vec = line.split(" ")
        # 去重
        if (line_vec[0] not in vis):
            vis.append(line_vec[0])
            f_write_2.write(line)
        else:
            continue

        x = gs.LB_to_xy(float(line_vec[2]), float(line_vec[3]))
        ans = str(id) + "," + line_vec[0]
        num = line_vec[1].replace("户","")
        ans = ans + "," + num
        ans = ans + "," + str(x[0]) + "," + str(x[1]) + "\n"
        f_write.write(ans)
        id = id + 1