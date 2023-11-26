# -*-coding:utf-8 -*-
"""
:创建时间: 2022/9/7 5:24
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

if __name__ == '__main__':
    import sgt_gui.index
    import sgt_skin_weights.app_api as sgtone_for_skin_weights
    import sgt_mesh_refine.app_api as sgtone_for_mesh_refine

    sgt_gui.index.app_list.append(sgtone_for_skin_weights.app)
    sgt_gui.index.app_list.append(sgtone_for_mesh_refine.app)

    sgt_gui.index.create_main_window()
