#!/usr/bin/python
# -*-coding:utf-8 -*-
u"""
:创建时间: 2021/5/24 13:44
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function

import hashlib
import binascii
import os
import time
import sqlite3
import json
import contextlib


class SimpleDbException(Exception): pass


def ket_hash(d):
    return hashlib.sha256(d).hexdigest()

KEY_VALUE_PAIR = os.path.dirname(os.path.abspath(__file__))
KEY_VALUE_PAIR = os.sep.join([KEY_VALUE_PAIR, 'sgt.sqlite'])


class Table(object):
    def __init__(self, name):
        self._name = name
        self._cache = dict()
        self._new_table(self._name)

    @contextlib.contextmanager
    def _execute(self):
        with sqlite3.connect(KEY_VALUE_PAIR) as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except Exception as ex:
                conn.rollback()
                raise SimpleDbException(u"数据库错误")
            finally:
                cursor.close()

    def _new_table(self, name):
        with sqlite3.connect(KEY_VALUE_PAIR) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("select * from sqlite_master where type = 'table' and name = '{}'".format(self._name))
                v = cursor.fetchall()
                if len(v) < 1:
                    for i in range(10):
                        try:
                            cursor.execute("""\
                            create table `{}`(
                            `key` varchar(4096) not null unique ,
                            `value` varchar(4096) not null
                            )
                            """.format(self._name))
                            conn.commit()
                        except Exception as ex:
                            print(">>", ex)
                            conn.rollback()
                            time.sleep(1)
                        else:
                            break
            finally:
                cursor.close()

    def _get(self, key, _default=None):
        key = ket_hash(json.dumps(key).encode("utf-8"))
        with self._execute() as cursor:
            cursor.execute("select `value` from `{}` where `key` = ?".format(self._name),
                           [key])
            v = cursor.fetchone()
            if v is None:
                v = _default
            else:
                v = json.loads(binascii.a2b_hex(v[0]))
            return v

    def _set(self, key, val):
        key = ket_hash(json.dumps(key).encode("utf-8"))
        val = binascii.b2a_hex(json.dumps(val).encode('utf-8'))
        with self._execute() as cursor:
            cursor.execute("select count(*) from `{}` where `key` = ?".format(self._name),
                           [key])
            if cursor.fetchone()[0] > 0:
                cursor.execute("update `{}` set `value`=? where `key` = ?".format(self._name),
                               [val, key])
            else:
                cursor.execute("insert into `{}` (`key`, `value`) values (?, ?)".format(self._name),
                               [key, val])

    def __iter__(self):
        with self._execute() as cursor:
            cursor.execute("select `key`, `value` from `{}`".format(self._name))
            v = cursor.fetchall()
            return ((i[0], json.loads(binascii.a2b_hex(i[1]))) for i in v)

    def get(self, key, _default=None):
        if key in self._cache:
            return self._cache[key]
        else:
            val = self._get(key, _default)
            self._cache[key] = val
            return val

    def set(self, key, val):
        self._set(key, val)
        self._cache[key] = val


def new(name):
    """
    :type name: str
    :rtype: Table
    """
    return Table(name)
