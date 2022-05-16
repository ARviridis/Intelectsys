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
        Form.resize(604, 329)
        self.count_clusters = QtWidgets.QSpinBox(Form)
        self.count_clusters.setGeometry(QtCore.QRect(10, 40, 131, 31))
        self.count_clusters.setMinimum(1)
        self.count_clusters.setMaximum(30)
        self.count_clusters.setProperty("value", 2)
        self.count_clusters.setObjectName("count_clusters")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(10, 80, 131, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.start_btn = QtWidgets.QPushButton(Form)
        self.start_btn.setGeometry(QtCore.QRect(10, 130, 131, 81))
        self.start_btn.setObjectName("start_btn")
        self.plot_btn = QtWidgets.QPushButton(Form)
        self.plot_btn.setGeometry(QtCore.QRect(10, 220, 131, 91))
        self.plot_btn.setObjectName("plot_btn")
        self.logs = QtWidgets.QPlainTextEdit(Form)
        self.logs.setGeometry(QtCore.QRect(150, 40, 431, 271))
        self.logs.setObjectName("logs")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(220, 0, 301, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.label_2.setObjectName("label_2")
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setEnabled(True)
        self.checkBox.setGeometry(QtCore.QRect(10, 100, 141, 21))
        self.checkBox.setMouseTracking(True)
        self.checkBox.setAcceptDrops(False)
        self.checkBox.setAutoFillBackground(True)
        self.checkBox.setInputMethodHints(QtCore.Qt.ImhNone)
        self.checkBox.setChecked(False)
        self.checkBox.setAutoRepeat(False)
        self.checkBox.setAutoExclusive(False)
        self.checkBox.setTristate(False)
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(Form)
        self.comboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "K_sred_clustering"))
        self.comboBox.setCurrentText(_translate("Form", "Euclidean"))
        self.comboBox.setItemText(0, _translate("Form", "Euclidean"))
        self.comboBox.setItemText(1, _translate("Form", "Dominirovanie"))
        self.start_btn.setText(_translate("Form", "To clustering"))
        self.plot_btn.setText(_translate("Form", "Make a graph\n"
"after making clusters"))
        self.label.setText(_translate("Form", "Clustering of multiple patterns (vectors)"))
        self.label_2.setText(_translate("Form", "Cluster kol-vo 1-30"))
        self.checkBox.setText(_translate("Form", "Нормирование образов"))


########################################################################################################
########################################################################################################
#obrazi
class obrazcl_podhod:
    def __init__(
            self,
            mnojestov_obraz,
            rast_dist,
            count_clusters,
            ves_ed=np.array([1, 1, 1]),
    ):
        self.vectors = mnojestov_obraz
        self.clusters = []
        self.rast_dist = rast_dist
        self.ves_ed = ves_ed
        self.count_clusters = count_clusters

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

# clustering po k srednim
    def clustering(self):
        count_clusters = self.count_clusters

        proizv_centr = []  # произвольные центры для начала
        for i in range(count_clusters):
            proizv_centr.append(self.vectors[i])
            new_cluster = Cluster()
            self.clusters.append(new_cluster)

        ki = 0
        centr_for_ravn = []
        ogr_flag = 1
        while (ogr_flag != 0):  # ki<2
            print('ki=', ki)

            print('proizv_centr', proizv_centr)
            print('centr_for_ravn', centr_for_ravn)

            if ki != 0:
                # удаляем старую выборку относительно прошлой середины образы
                proizv_centr = []
                # заносим новые центры
                for clusters_i in range(len(self.clusters)):
                    proizv_centr.append(self.clusters[clusters_i].center)
                    self.clusters[clusters_i].vectors = []
            else:
                print('Первый_прогон')

            for vector in self.vectors:  # вычисляем расстояние от векторов(образов) к каждой середине кластера
                dist_beetwen_centr_And_obraz = []  # массив с расстояниями одного образа к цестрам кластера

                # вычисляем расстояния новые между центрои и образами
                for proizv_centr_i in range(len(proizv_centr)):  # для каждой середины вычисляем расстояние
                    dist = self.rast_dist(
                        vector,
                        proizv_centr[proizv_centr_i],
                        self.ves_ed,  # (едининицы) задаются для scypi
                    )
                    dist_beetwen_centr_And_obraz.append(dist)  # дистанции

                min_rast = min(dist_beetwen_centr_And_obraz)
                # смотрим к какому кластеру принадлежит минимум
                for i in range(len(dist_beetwen_centr_And_obraz)):
                    if dist_beetwen_centr_And_obraz[i] == min_rast:
                        # причисляем этот образ к этому кластеру
                        self.clusters[i].add_vector(vector)

            ki = ki + 1

            # пересчитанные центры выносим для сравнения, чтобы выйти из цикла(стабилизация кластера)
            centr_for_ravn = []

            ogr_flag = 0
            for clusters_i in range(len(self.clusters)):
                for i in range(len(self.clusters[clusters_i].center)):
                    if proizv_centr[clusters_i][i] != self.clusters[clusters_i].center[i]:
                        print("не равный цетр")
                        ogr_flag = 1
                        break
                centr_for_ravn.append(self.clusters[clusters_i].center)
            if ogr_flag == 0:
                print('конец')

            print('proizv_centr2', proizv_centr)
            print('centr_for_ravn2', centr_for_ravn)

        return self.clusters

    def get_clusters(self):
        return self.clusters


class Cluster:
    def __init__(self):
        self.vectors = []
    # для автоматического подтягивания середины при добавлении
    def get_center(self):
        try:
            n = len(self.vectors)
            x_vector = sum([vector[0] for vector in self.vectors]) / n
            y_vector = sum([vector[1] for vector in self.vectors]) / n
            z_vector = sum([vector[2] for vector in self.vectors]) / n
        except ValueError:
            return np.array([0, 0, 0])
        return np.array([x_vector, y_vector, z_vector])

    def add_vector(self, vector):
        self.vectors.append(vector)

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
            [(15, 6, 15), (1, 19, 0), (-8, -1, 4), (13, 19, 15), (15, 17, -14), (-3, 9, -35),
             (12, 4, 16), (8, 14, 9), (-6, 0, 5), (11, 17, 10), (12, 17, -10), (-1, 10, -25),
             (18, 17, -11), (-4, 9, -31), (19, 4, 13), (8, 14, 10), (-6, -5, 1), (20, 20, 20),
             (7, 16, -17), (-1, 7, -26), (15, 1, 10), (0, 11, 8), (-8, -1, 5), (10, 10, 10),
             (12, 15, -10), (-4, 5, -27), (-7, -1, 4), (3, 17, 11), (0, 1, 3), (7, 2, 0), ]
        )

        self.show()
        self.start_btn.clicked.connect(self.start)
        self.plot_btn.clicked.connect(self.plot)

    def start(self):
        self.logs.clear()
        count_clusters = int(self.count_clusters.value())
        ves_ed = np.array([1, 1, 1])  # ves edinici for skipy

        rast_dist = distance.euclidean  # Евклидово расстояние
        if self.comboBox.currentIndex() == 0:
            rast_dist = distance.euclidean
        elif self.comboBox.currentIndex() == 1:
            rast_dist = distance.chebyshev  # Доминировние расстояние

        sostav = obrazcl_podhod(
            self.mnojestov_obraz,
            rast_dist,
            count_clusters,
            ves_ed=ves_ed,
        )

        if self.checkBox.checkState() == 2:
            self.logs.insertPlainText(
                f'Normalizaciya_active__!\n\n')
            sostav.normalize_vectors()

        sostav.clustering()

        self.clusters = sostav.get_clusters()

        self.logs.insertPlainText(
            f'Количество полученных класстеров: {str(len(self.clusters))}\n\n')
        for i, cluster in enumerate(self.clusters):
            vectors = [[round(vector[0], 2), round(vector[1], 2), round(vector[2], 2)] for
                       vector in cluster.vectors]
            self.logs.insertPlainText(f'Клустер {i + 1}: {str(vectors[:])}\n')

    def plot(self):
        color = ['red', 'blue', 'green', 'black',
                 'yellow', 'silver', 'pink', 'brown', 'gold']
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        for i, cluster in enumerate(self.clusters):
            x = [x[0] for x in cluster.vectors]
            y = [y[1] for y in cluster.vectors]
            z = [z[2] for z in cluster.vectors]
            # Распределение цветов
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
