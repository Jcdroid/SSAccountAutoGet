# coding: utf-8
__author__ = 'caojing'

from pywinauto import application

def test():
    app = application.Application()
    app.start_('notepad.exe')

if __name__ == '__main__':
    test()