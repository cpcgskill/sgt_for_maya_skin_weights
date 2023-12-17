# -*-coding:utf-8 -*-
"""
:创建时间: 2023/11/26 19:33
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
except ImportError:
    try:
        from PySide2.QtGui import *
        from PySide2.QtCore import *
        from PySide2.QtWidgets import *
    except ImportError:
        from PySide.QtGui import *
        from PySide.QtCore import *
import sys

app = QApplication(sys.argv)
import cpmel.cmds as cc
import sgt_gui.index
import sgt_skin_weights.app_api as sgtone_for_skin_weights
import sgt_mesh_refine.app_api as sgtone_for_mesh_refine
sgt_gui.index.app_list.append(sgtone_for_skin_weights.app)
sgt_gui.index.app_list.append(sgtone_for_mesh_refine.app)

if __name__ == '__main__':
    from maya_test_tools import open_file, question_open_maya_gui

    # open_file(r'C:\\Users\\PC\\Desktop\\卡内奇Rig集(内含 Vegta,Sebastian,Zoey,Monarudo,Lindsey\\Zoey_Rig_V002.ma')
    open_file(r'C:/Users/PC/Desktop/backup_to_cloud/dev/pytorch_for_maya/sgt/sgt_for_maya_skin_weights/test/mesh_refine.ma')

    sgt_gui.index.create_main_window()

    app.exec_()

    # question_open_maya_gui()
