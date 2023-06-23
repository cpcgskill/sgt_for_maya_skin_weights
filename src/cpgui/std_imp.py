#!/usr/bin/python
# -*-coding:utf-8 -*-
u"""
:创建时间: 2021/9/20 12:54
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function
try:
    ui_lib_str = "PySide2"
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    from PySide2.QtSvg import *
except ImportError:
    try:
        ui_lib_str = "PySide"
        from PySide.QtGui import *
        from PySide.QtCore import *
        from PySide.QtSvg import *
    except ImportError:
        ui_lib_str = "PyQt5"
        from PyQt5.QtWidgets import *
        from PyQt5.QtCore import *
        from PyQt5.QtGui import *
        from PyQt5.QtSvg import *
try:
    from shiboken2 import *
except ImportError:
    from shiboken import *

import sys
import maya.OpenMayaUI as OpenMayaUI
import maya.cmds as mc

deleteWidget = delete
try:
    if hasattr(mc, "about"):
        ptr_t = int if sys.version_info.major > 2 else long
        mui = wrapInstance(ptr_t(OpenMayaUI.MQtUtil.mainWindow()), QWidget)
    else:
        mui = None
except:
    mui = None