import pyscreenshot

L_dis = 25
U_dis = 247
R_dis = 2067
D_dis = 1050
pic_region = pyscreenshot.grab(bbox=(L_dis, U_dis, R_dis, D_dis))
pic_region.save('pic.jpg')