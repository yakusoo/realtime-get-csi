# -*- coding: utf-8 -*-
from kivy.config import Config
Config.set('graphics', 'width', '1400')
Config.set('graphics', 'height', '1080')
#Windowの大きさを定義

from kivy.core.text import LabelBase, DEFAULT_FONT
LabelBase.register(DEFAULT_FONT, "ipamjm.ttf")

from random import sample
from string import ascii_lowercase
from kivy.base import runTouchApp
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty
from kivy.event import EventDispatcher
import sys
from show_gui import do_predict

Window.clearcolor = (0, 0.4, 0.9, 1)
#Builder.load_file("./GUI.kv")
Builder.load_string('''
#この部分も#でコメントアウトが可能
<Row@BoxLayout>:
    canvas.before:
        Color:
            rgba: 0.5, 0.5, 0.5, 1
        Rectangle:
            size: self.size
            pos: self.pos
    value: ''
    Button:
        text: root.value
    Image:
        size: self.width + 100, self.height + 100

<LabelWidget>:
    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: 0.2
            size: root.size
            pos: root.pos
            Label:
                id: packet_number
                color: 1, 1, 0, 1
                text: '結果'
                font_size: 80

            Button:
                id: packet
                color: 1, 1, 0, 1
                text: root.numbertext
                font_size: 40

        BoxLayout:
            size_hint_y: 0.2
            pos: root.pos
            size: root.size
            Button:
                id: svm
                text: 'SVM'
                font_size: 80
                color: 1, 1, 0, 1

            Button:
                id: svm_result
                text: root.svmtext
                font_size: 60
                color: 1, 1, 0, 1

        BoxLayout:
            size_hint_y: 0.1
            Button:
                id: retry
                text: '実行'
                font_size: 80
                on_press:root.res()
                on_release:root.restart()
                #on_press: root.res()
                #on_pressでボタンが押された時の動作を決める
            Button:
                id: exit
                text: '終了'
                font_size: 80
                on_press: root.end()



''')




def get_score():
    l = []
    f = open('result.txt', 'r')
    for row in f:
        l.append(int(row.strip()))
    f.close()
    a = l[0]
    b = l[1]
    c = l[2]
    return a, b, c


def Result(self, pred_svm=0, per_svm=0, number=0):
    self.pred_svm = pred_svm
    self.per_svm = per_svm
    self.number = number

    pred_svm, per_svm, number = get_score()

    self.numbertext = 'キャプチャ時間: 2 秒\n キャプチャ数 %d 個' %(number)

    #この部分はサービスによって変わる

    if pred_svm == 0:
        self.svmtext = '未検出\n精度 :%f' %(per_svm)
    elif pred_svm == 1:
        self.svmtext = 'イノシシ 検出\n精度: %f' %(per_svm)
    elif pred_svm == 2:
        self.svmtext = 'カボチャ 検出\n精度: %f' %(per_svm)
    elif pred_svm == 3:
        self.svmtext = 'ペットボトル 検出\n精度: %f' %(per_svm)
    elif pred_svm == 4:
        self.svmtext = 'カボチャ横向き 検出\n精度: %f' %(per_svm)
    elif pred_svm == -100:
        self.svmtext = '失敗'

class LabelWidget(Screen):
    #動的に変わるtextを用意
    svmtext = StringProperty()
    numbertext = StringProperty()


    def __init__(self, **kwargs):
        super(LabelWidget, self).__init__(**kwargs)
        self.svmtext = ''
        self.numbertext ='キャプチャ時間 : 2 秒\n'
        #Result(self)


    def end(self):
        sys.exit()

    def restart(self):
        do_predict()
        Result(self)

    def res(self):
        self.svmtext = '検出中\n'

class CSIResultApp(App):
    #pred = ObjectProperty()
    def __init__(self, **kwargs):
        super(CSIResultApp, self).__init__(**kwargs)
        self.title = 'CSI Identification'
    def build(self):
        return LabelWidget()




if __name__ == '__main__':
    CSIResultApp().run()
