import sys
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPalette
from scipy.spatial import distance

# Forms GUI
########################################################################################################
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(674, 529)
        self.count_clusters = QtWidgets.QSpinBox(Form)
        self.count_clusters.setGeometry(QtCore.QRect(10, 40, 161, 31))
        self.count_clusters.setMinimum(1)
        self.count_clusters.setMaximum(24)
        self.count_clusters.setProperty("value", 2)
        self.count_clusters.setObjectName("count_clusters")
        self.start_btn = QtWidgets.QPushButton(Form)
        self.start_btn.setGeometry(QtCore.QRect(10, 340, 131, 81))
        self.start_btn.setObjectName("start_btn")
        self.plot_btn = QtWidgets.QPushButton(Form)
        self.plot_btn.setGeometry(QtCore.QRect(10, 420, 131, 91))
        self.plot_btn.setObjectName("plot_btn")
        self.logs = QtWidgets.QPlainTextEdit(Form)
        self.logs.setGeometry(QtCore.QRect(180, 40, 481, 471))
        self.logs.setObjectName("logs")
        self.label_all = QtWidgets.QLabel(Form)
        self.label_all.setGeometry(QtCore.QRect(180, 10, 391, 21))
        self.label_all.setObjectName("label_all")
        self.text_for_count_clusters = QtWidgets.QLabel(Form)
        self.text_for_count_clusters.setGeometry(QtCore.QRect(10, 10, 131, 16))
        self.text_for_count_clusters.setObjectName("text_for_count_clusters")
        self.text_distance = QtWidgets.QLabel(Form)
        self.text_distance.setGeometry(QtCore.QRect(10, 320, 121, 16))
        self.text_distance.setObjectName("text_distance")
        self.text_radius = QtWidgets.QLabel(Form)
        self.text_radius.setGeometry(QtCore.QRect(10, 200, 121, 16))
        self.text_radius.setObjectName("text_radius")
        self.text_n_sp = QtWidgets.QLabel(Form)
        self.text_n_sp.setGeometry(QtCore.QRect(10, 80, 141, 16))
        self.text_n_sp.setObjectName("text_n_sp")
        self.n_sp = QtWidgets.QDoubleSpinBox(Form)
        self.n_sp.setGeometry(QtCore.QRect(10, 100, 161, 31))
        self.n_sp.setPrefix("")
        self.n_sp.setSuffix("")
        self.n_sp.setDecimals(3)
        self.n_sp.setMinimum(0.001)
        self.n_sp.setMaximum(0.7)
        self.n_sp.setSingleStep(0.001)
        self.n_sp.setProperty("value", 0.7)
        self.n_sp.setObjectName("n_sp")
        self.radius = QtWidgets.QDoubleSpinBox(Form)
        self.radius.setGeometry(QtCore.QRect(10, 220, 161, 31))
        self.radius.setPrefix("")
        self.radius.setSuffix("")
        self.radius.setDecimals(1)
        self.radius.setMinimum(0.0)
        self.radius.setMaximum(5.0)
        self.radius.setSingleStep(0.1)
        self.radius.setProperty("value", 0.0)
        self.radius.setObjectName("radius")
        self.n_sp_2 = QtWidgets.QDoubleSpinBox(Form)
        self.n_sp_2.setGeometry(QtCore.QRect(10, 160, 161, 31))
        self.n_sp_2.setPrefix("")
        self.n_sp_2.setSuffix("")
        self.n_sp_2.setDecimals(3)
        self.n_sp_2.setMinimum(0.001)
        self.n_sp_2.setMaximum(0.1)
        self.n_sp_2.setSingleStep(0.001)
        self.n_sp_2.setProperty("value", 0.1)
        self.n_sp_2.setObjectName("n_sp_2")
        self.text_n_sp_2 = QtWidgets.QLabel(Form)
        self.text_n_sp_2.setGeometry(QtCore.QRect(10, 140, 161, 16))
        self.text_n_sp_2.setObjectName("text_n_sp_2")
        self.text_radius_2 = QtWidgets.QLabel(Form)
        self.text_radius_2.setGeometry(QtCore.QRect(10, 260, 161, 16))
        self.text_radius_2.setObjectName("text_radius_2")
        self.radius_2 = QtWidgets.QDoubleSpinBox(Form)
        self.radius_2.setGeometry(QtCore.QRect(10, 280, 161, 31))
        self.radius_2.setPrefix("")
        self.radius_2.setSuffix("")
        self.radius_2.setDecimals(3)
        self.radius_2.setMinimum(0.001)
        self.radius_2.setMaximum(0.1)
        self.radius_2.setSingleStep(0.001)
        self.radius_2.setProperty("value", 0.1)
        self.radius_2.setObjectName("radius_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Clustering with a Cohen output layer"))
        self.start_btn.setText(_translate("Form", "To clustering"))
        self.plot_btn.setText(_translate("Form", "Make a graph\n"
"after making clusters"))
        self.label_all.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">Clustering of multiple patterns(vectors) with a Cohen output layer</span></p></body></html>"))
        self.text_for_count_clusters.setText(_translate("Form", "Cluster_Neuron amt 1-24"))
        self.text_distance.setText(_translate("Form", "distance: Euclidean"))
        self.text_radius.setText(_translate("Form", "radius 0 - 5"))
        self.text_n_sp.setText(_translate("Form", "n:learning speed 0.001-0.7"))
        self.text_n_sp_2.setText(_translate("Form", "n_step:change speed 0.1-0.001"))
        self.text_radius_2.setText(_translate("Form", "r_step:change radius 0.1-0.001"))
########################################################################################################
########################################################################################################
#obrazi
class obrazcl_podhod:
    def __init__(
            self,
            mnojestov_obraz,
            rast_dist,
            count_clusters,
            n_speed, r,
            shag_n, shag_r,
            ves_ed=np.array([1, 1, 1]),
    ):
        self.vectors = mnojestov_obraz
        self.clusters = []
        self.rast_dist = rast_dist
        self.ves_ed = ves_ed
        self.count_clusters = count_clusters
        self.n_speed = n_speed
        self.r = r
        self.cicl = 0
        self.shag_n = shag_n
        self.shag_r = shag_r

# normalizaciz po max min
    def normalize_vectors(self):
        x_vector = [vector[0] for vector in self.vectors]  # max min по иксу
        x_max, x_min = max(x_vector), min(x_vector)
        y_vector = [vector[1] for vector in self.vectors]  # max min по y
        y_max, y_min = max(y_vector), min(y_vector)
        z_vector = [vector[2] for vector in self.vectors]  # max min по z
        z_max, z_min = max(z_vector), min(z_vector)
        new_vectors = []

        for vector in self.vectors:
            new_vectors.append(
                np.array(
                    [
                        ((vector[0] - x_min) / (x_max - x_min)),
                        ((vector[1] - y_min) / (y_max - y_min)),
                        ((vector[2] - z_min) / (z_max - z_min)),
                    ]
                )
            )
        self.vectors = new_vectors

    def wes(self):
        new_neitr = neitr()
        self.clusters.append(new_neitr)


        centrall = []
        centr1 = self.vectors[0]

        self.clusters[0].add_w(centr1)

        dist_w_n = []
        dist_w_n1 = []


        for centrall_i in range(self.count_clusters):
            for vector in range(len(self.vectors)):

                dist = self.rast_dist(
                    self.vectors[vector],
                    self.clusters[centrall_i].centr1,
                    self.ves_ed,
                    )
                if dist != 0:
                        dist_w_n.append([dist, centrall_i])
                        dist_w_n1.append(self.vectors[vector])
            i = 0
            min1 = []
            max_ot_min = []
            while i < len(self.vectors)-1:

                fl = 0
                vrem = []
                for j in range(len(dist_w_n1)):
                    if dist_w_n1[i].all == dist_w_n1[j].all:
                        for k in range(len(centrall)):
                            if dist_w_n1[j].all == centrall[k].all:
                                fl = 1
                                break
                        if fl != 1:
                            vrem.append([dist_w_n[j][0], j])

                if fl != 1:
                    min1.append(vrem[np.argmin(vrem, axis=0)[0]])
                i = i + 1

            max_ot_min.append(min1[np.argmax(min1, axis=0)[0]])


            if len(self.clusters) < self.count_clusters:
                centrall.append(dist_w_n1[min1[np.argmax(min1, axis=0)[0]][1]])

                new_neitr = neitr()
                self.clusters.append(new_neitr)
                self.clusters[-1].add_w(dist_w_n1[min1[np.argmax(min1, axis=0)[0]][1]])

        for ip in range(len(self.clusters)):
            self.clusters[ip].add_w_start(self.clusters[ip].centr1[0])
        del centrall
        return self.clusters

    def cor_wes(self):
        whileend = 0
        while whileend != 1:
            vrem_old=[]
            vrem_new = []
            for centrall_i in range(len(self.clusters)):
                self.clusters[centrall_i].vectors = []
                vrem_old.append(self.clusters[centrall_i].centr1)
            for vector in range(len(self.vectors)):
                vrem = []
                for centrall_i in range(len(self.clusters)):

                    dist = self.rast_dist(
                        self.vectors[vector],
                        self.clusters[centrall_i].centr1,
                        self.ves_ed,
                            )
                    if dist != 0:
                        vrem.append([dist,centrall_i])

                if vrem == []:
                    vrem =[[0,0]]

                for dd in range(len(self.clusters)):
                    dist = self.rast_dist(
                        self.clusters[(vrem[np.argmin(vrem, axis=0)[0]][1])].centr1[0],
                        self.clusters[dd].centr1,
                        self.ves_ed,
                    )
                    if dist <= self.r:

                        xv = self.clusters[dd].centr1[0][0] \
                             + self.n_speed*(self.vectors[vector][0] \
                             - self.clusters[dd].centr1[0][0])
                        yv = self.clusters[dd].centr1[0][1] \
                             + self.n_speed * (self.vectors[vector][1] \
                             - self.clusters[dd].centr1[0][1])
                        zv = self.clusters[dd].centr1[0][2] \
                             + self.n_speed * (self.vectors[vector][2] \
                             - self.clusters[dd].centr1[0][2])
                        self.clusters[dd].centr1.pop(-1)
                        self.clusters[dd].add_w([xv,yv,zv])


                        self.clusters[dd].add_vector(self.vectors[vector])

            for centrall_i in range(len(self.clusters)):
                vrem_new.append(self.clusters[centrall_i].centr1)


            whileend = 1
            for ik in range(len(vrem_new)):
                for ii in range(2):
                    if vrem_new[ik][0][ii] != vrem_old[ik][0][ii]:
                        whileend = 0
                        break
            for centrall_i in range(len(self.clusters)):
                for ii in range(2):
                    if round(self.clusters[centrall_i].centr1[0][ii],3) != round(self.clusters[centrall_i].center[ii],3):
                        whileend = 0
                        if self.n_speed <= self.shag_n and self.r < self.shag_r:
                            whileend = 1
                            print ("спуск не дал конечного результат, последнее приближение далее")
                            break
                        if self.n_speed > self.shag_n:
                            self.n_speed=self.n_speed-self.shag_n
                            print("уменьшение скорости",self.n_speed)
                        if self.r >= self.shag_r:
                            self.r = self.r - self.shag_r
                            print("уменьшение радиуса",self.r)
                        break
            if whileend == 1:
                print("конечный результат, последнее приближение далее")
            self.cicl = self.cicl+1
        for ip in range(len(self.clusters)):
            print(self.clusters[ip].vectors)
        return self.clusters,self.cicl



    def get_clusters(self):
        return self.clusters





class neitr:
    def __init__(self):
        self.vectors = []
        self.centr1 = []
        self.centr_start = []

    def get_center(self):
        try:
            n = len(self.vectors)
            x_vector = sum([vector[0] for vector in self.vectors]) / n
            y_vector = sum([vector[1] for vector in self.vectors]) / n
            z_vector = sum([vector[2] for vector in self.vectors]) / n
        except ValueError:
            return np.array([0, 0, 0])
        except ZeroDivisionError:
            return np.array([0, 0, 0])
        return np.array([x_vector, y_vector, z_vector])

    def add_vector(self, vector):
        self.vectors.append(vector)

    def add_w(self, w):
        self.centr1.append(w)

    def add_w_start(self, w_s):
        self.centr_start.append(w_s)

    @property
    def center(self):
        return self.get_center()


########################################################################################################
########################################################################################################


class MainWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.clusters = None
        self.mnojestov_obraz = np.array(
            [(18, 5, 7), (22, 3, 9), (18, 23, 22), (26, 7, 6), (22,7, 8),
             (20, 23, 16), (20, 5, 5), (22, 24, 8), (18, 19, 7), (21, 20, 2),
             (23, 3, 20), (20, 2, 19), (21, 6, 23), (21, 7, 17), (24, 4, 17),
             (21, 25, 21), (21, 22, 6), (22, 19, 17), (16, 7, 4), (23, 27, 3),
             (18, 3, 2), (24, 16, 19), (25, 3, 23), (19, 20, 6), (20, 19, 21), ]
        )

        self.show()
        self.start_btn.clicked.connect(self.start)
        self.plot_btn.clicked.connect(self.plot)

    def start(self):
        self.logs.clear()
        count_clusters = int(self.count_clusters.value()) # кластеры нейроны
        n_speed = self.n_sp.value()
        r = self.radius.value()
        shag_n = self.n_sp_2.value()
        shag_r = self.radius_2.value()

        ves_ed = np.array([1, 1, 1])

        rast_dist = distance.euclidean


        sostav = obrazcl_podhod(
            self.mnojestov_obraz,
            rast_dist,
            count_clusters,
            n_speed, r,
            shag_n, shag_r,
            ves_ed=ves_ed,
        )


        self.logs.insertPlainText(
            f'Normalizaciya_active__!\n\n')
        sostav.normalize_vectors()

        sostav.wes()

        sostav.cor_wes()

        self.clusters = sostav.get_clusters()
        self.logs.insertPlainText(
            f'Количество нейронов/класстеров: {str(len(self.clusters))}\n\n')
        self.logs.insertPlainText(
            f'Количество итерация до точности: {sostav.cicl}\n\n')

        for i, cluster in enumerate(self.clusters):
            self.logs.insertPlainText(f'Начальный вес/центр нейрона: {i + 1}: '
                f' {[round(self.clusters[i].centr_start[0][0],2), round(self.clusters[i].centr_start[0][1],2), round(self.clusters[i].centr_start[0][2],2)]}'
                                      f'\n\n')
            self.logs.insertPlainText(f'Конечный вес/центр нейрона: {i + 1}: '
                f' {[round(self.clusters[i].centr1[0][0],2), round(self.clusters[i].centr1[0][1],2), round(self.clusters[i].centr1[0][2],2)]}'
                                      f'\n\n')
            self.logs.insertPlainText(f'центр нейрона_по векторам: {i + 1}: '
                f' {[round(self.clusters[i].center[0],2), round(self.clusters[i].center[1],2), round(self.clusters[i].center[2],2)]}'
                                      f'\n\n')
            vectors = [[round(vector[0], 2), round(vector[1], 2), round(vector[2], 2)] for
                       vector in cluster.vectors]
            self.logs.insertPlainText(f'Клустер {i + 1}: {str(vectors[:])}'
                                      f'\n\n')
            print(f'Клустер {i + 1}: {str(vectors[:])}\n')


    def plot(self):
        color = ['red', 'blue', 'green', 'black',
                 'yellow', 'silver', 'pink', 'brown', 'gold']
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        for i, cluster in enumerate(self.clusters):
            x = [x[0] for x in cluster.vectors]
            y = [y[1] for y in cluster.vectors]
            z = [z[2] for z in cluster.vectors]
            if i < len(color):
                ax.scatter(x, y, z, label=f'{i} cluster', color=color[i])
            else:
                ax.scatter(x, y, z, label=f'{i} cluster', color='black')
        ax.legend()
        plt.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = MainWindow()
    widget.setBackgroundRole(QPalette.Shadow)
    widget.setStyleSheet(
        "QWidget {border: 0.1px solid DarkCyan ;text-align: center;"
        "color:rgba(255,255,250,255);"
        "border-radius: 2px;"
        "border-width: 2px;"
        "border-image: 9,2,5,2; "
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(70, 70, 70, 255)\,\
         stop:1 rgba(10, 0, 0, 200));"
        "}"
        "QHeaderView::section:horizontal {color: #fff;border-style: solid;background-color: qlineargradient( x1: 0,\
         y1: 0, x2: 0, y2: 1,stop: 0 #20B2AA, stop: 1 #356ccc);}"

        "QTableView {border: 2px solid #3873d9;border-top-color: #808000;border-radius: 4px;background-color:\
         #696969;gridline-color: #777;selection-background-color: #808000;color:#000000;font-size:12px;}"
    )
    sys.exit(app.exec_())