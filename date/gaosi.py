# import numpy as np
import math


class Point:
    def __init__(self, type=0):
        self.B = 0
        self.L = 0
        self.H = 0

        ##### 椭球参数
        # CGCS2000
        if type == 1:
            self.a = 6378137
            self.f = 1 / 298.257222101

        ## 西安80
        elif type == 2:
            self.a = 6378140
            self.f = 1 / 298.257

        ## 北京54
        elif type == 3:
            self.a = 6378245
            self.f = 1 / 298.3

        ## WGS-84
        else:
            self.a = 6378137
            self.f = 1 / 298.257223563

        self.b = self.a * (1 - self.f)
        self.e = math.sqrt(self.a * self.a - self.b * self.b) / self.a  ##第一偏心率
        self.e2 = math.sqrt(self.a * self.a - self.b * self.b) / self.b  ##第二偏心率
        self.d2r = math.pi / 180

    def SetBLH_DMS(self, degree_L=0.0, minutes_L=0.0, second_L=0.0, degree_B=0.0, minutes_B=0.0, second_B=0.0, H_=0.0):
        ## 度分秒化为 度.度
        self.L = (degree_L + minutes_L / 60.0 + second_L / 3600.0)
        self.B = (degree_B + minutes_B / 60.0 + second_B / 3600.0)
        self.H = H_

    def SetBLH_D(self, B, L, H=0):
        ## 经纬度格式是 度.度
        self.L = L
        self.B = B
        self.H = H

    def GaussProjection(self):
        L0 = 114  ##中央子午线，这里是3度带的取法，6度带注意修改这里
        rho = 180 / math.pi  # 单位是度.度
        l = (self.L - L0) / rho  ## 公式中的参数 l

        cB = math.cos(self.B * self.d2r)
        sB = math.sin(self.B * self.d2r)
        self.N = self.a / math.sqrt(1 - self.e * self.e * sB * sB)  ## 卯酉圈曲率半径
        self.t = math.tan(self.B * self.d2r)  ##tanB 对应公式中的参数t
        self.eta = self.e2 * cB  ## 对应公式中的参数 eta

        m0 = self.a * (1 - self.e * self.e)
        m2 = 3.0 / 2.0 * self.e * self.e * m0
        m4 = 5.0 / 4.0 * self.e * self.e * m2
        m6 = 7.0 / 6.0 * self.e * self.e * m4
        m8 = 9.0 / 8.0 * self.e * self.e * m6

        a0 = m0 + 1.0 / 2.0 * m2 + 3.0 / 8.0 * m4 + 5.0 / 16.0 * m6 + 35.0 / 128.0 * m8
        a2 = 1.0 / 2.0 * m2 + 1.0 / 2.0 * m4 + 15.0 / 32.0 * m6 + 7.0 / 16.0 * m8
        a4 = 1.0 / 8.0 * m4 + 3.0 / 16.0 * m6 + 7.0 / 32.0 * m8
        a6 = 1.0 / 32.0 * m6 + 1.0 / 16.0 * m8
        a8 = 1.0 / 128.0 * m8

        s2b = math.sin(self.B * self.d2r * 2)
        s4b = math.sin(self.B * self.d2r * 4)
        s6b = math.sin(self.B * self.d2r * 6)
        s8b = math.sin(self.B * self.d2r * 8)

        ## X为自赤道量起的子午线弧长
        self.X = a0 * (
                    self.B * self.d2r) - 1.0 / 2.0 * a2 * s2b + 1.0 / 4.0 * a4 * s4b - 1.0 / 6.0 * a6 * s6b + 1.0 / 8.0 * a8 * s8b

        ## 坐标X
        self.xs = self.X + self.N / 2 * self.t * cB * cB * l * l + self.N / 24 * self.t * (
                    5 - self.t * self.t + 9 * math.pow(self.eta, 2) + 4 * math.pow(self.eta, 4)) * math.pow(cB,
                                                                                                            4) * math.pow(
            l, 4) \
                  + self.N / 720 * self.t * (61 - 58 * self.t * self.t + math.pow(self.t, 4)) * math.pow(cB,
                                                                                                         6) * math.pow(
            l, 6)

        ## 坐标Y
        self.ys = self.N * cB * l + self.N / 6 * (1 - self.t * self.t + self.eta * self.eta) * math.pow(cB,
                                                                                                        3) * math.pow(l,
                                                                                                                      3) \
                  + self.N / 120 * (5 - 18 * self.t * self.t + math.pow(self.t, 4) + 14 * math.pow(self.eta,
                                                                                                   2) - 58 * self.eta * self.eta * self.t * self.t) * math.pow(
            cB, 5) * math.pow(l, 5) + 500000

        self.hs = self.H

        self.xyh_vector = [self.xs,self.ys,self.hs]

def degree_to_dms(x):
    d = int(x)
    f = int((x - d) * 60) / 100
    s = (x - d - (int((x - d) * 60) / 60)) * 3600 / 10000
    return [d, f, s]

def LB_to_xy(L, B):
    L = degree_to_dms(L)
    B = degree_to_dms(B)
    L_degree = float(L[0])
    L_minute = float(L[1])
    L_second = float(L[2])
    B_degree = float(B[0])
    B_minute = float(B[1])
    B_second = float(B[2])
    H = 0
    p = Point(type=1)
    p.SetBLH_DMS(L_degree, L_minute, L_second, B_degree, B_minute, B_second, H)
    p.GaussProjection()

    return [p.xyh_vector[0], p.xyh_vector[1]]