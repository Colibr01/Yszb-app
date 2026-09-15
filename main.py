import os
import random
from datetime import datetime
from kivy.core.text import LabelBase
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

# 中文字体
font_path = None
font_candidates = [
    '/system/fonts/NotoSansCJK-Regular.ttc',
    '/system/fonts/DroidSansFallbackFull.ttf',
    '/system/fonts/DroidSansFallback.ttf',
    '/system/fonts/NotoSansSC-Regular.otf'
]
for f in font_candidates:
    if os.path.exists(f):
        font_path = f
        break

if font_path:
    LabelBase.register(name='Roboto', fn_regular=font_path)

# 细爻（六爻占卜左侧用）
THIN_YANG  = "━━━━━"
THIN_YIN   = "━━　━━"

# 粗爻（2元随地占 + 六爻占卜右侧用）
THICK_YANG = "█████"
THICK_YIN  = "██　██"


def get_yao_thin():
    return THIN_YANG if random.random() < 0.5 else THIN_YIN


def get_yao_thick():
    return THICK_YANG if random.random() < 0.5 else THICK_YIN


def get_gua_name(yaos):
    yang_count = sum(1 for y in yaos if y == THIN_YANG)
    if yang_count == 3:
        return "老阳"
    elif yang_count == 0:
        return "老阴"
    elif yang_count == 1:
        return "少阴"
    else:
        return "少阳"


def get_gua_parts(name):
    if name == "老阳":
        return THICK_YANG, "○"
    elif name == "老阴":
        return THICK_YIN, "×"
    elif name == "少阳":
        return THICK_YANG, "　"
    else:
        return THICK_YIN, "　"


def make_button(text, size=48):
    b = Button(text=text, font_size=size)
    b.background_color = (0.54, 0.71, 0.98, 1)
    b.color = (0, 0, 0, 1)
    return b


def toast(msg):
    content = BoxLayout(orientation='vertical', padding=10, spacing=10)
    lbl = Label(text=msg, font_size=24)
    content.add_widget(lbl)
    ok = Button(text="好的", size_hint=(1, 0.5), font_size=36)
    content.add_widget(ok)
    popup = Popup(title="提示", content=content,
                  size_hint=(0.8, 0.4), title_size=30)
    ok.bind(on_press=popup.dismiss)
    popup.open()


def show_help_popup():
    content = BoxLayout(orientation='vertical', padding=20, spacing=12)
    help_text = (
        "0. 生成六次保存发给雨神\n\n"
        "1. 唯独雨神占卜有效\n\n"
        "2. 占卜时心诚则灵\n\n"
        "3. 建议占卜间隔不低于两月\n\n"
        "4. 应用只简化起卦，分析仍需要雨神亲为"
    )
    lbl = Label(text=help_text, font_size=32,
                halign='left', valign='top')
    lbl.bind(size=lambda s, v: setattr(s, 'text_size', (v[0], None)))
    content.add_widget(lbl)
    close_btn = Button(text="关闭", size_hint=(1, 0.25), font_size=40)
    content.add_widget(close_btn)
    popup = Popup(title="使用说明", content=content,
                  size_hint=(0.9, 0.8), title_size=44)
    close_btn.bind(on_press=popup.dismiss)
    popup.open()


def save_widget_to_png(widget, prefix="yinyang"):
    try:
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
        except Exception:
            pass
        save_dir = "/sdcard/Pictures"
        try:
            os.makedirs(save_dir, exist_ok=True)
        except Exception:
            save_dir = os.path.expanduser("~")
        filename = os.path.join(
            save_dir,
            f"{prefix}_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
        )
        widget.export_to_png(filename)
        toast("已保存到：\n" + filename)
    except Exception as e:
        toast("保存失败：\n" + str(e))
class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=30)
        layout.add_widget(Label(text="雨　神　占　卜", font_size=72,
                                bold=True, size_hint=(1, 0.25)))

        row1 = BoxLayout(orientation='horizontal', size_hint=(1, 0.11))
        row1.add_widget(Label(text="", size_hint=(0.25, 1)))
        b1 = make_button("2元随地占", 42)
        b1.size_hint = (0.5, 1)
        b1.bind(on_press=lambda x: setattr(self.manager, 'current', 'coin'))
        row1.add_widget(b1)
        row1.add_widget(Label(text="", size_hint=(0.25, 1)))
        layout.add_widget(row1)

        row2 = BoxLayout(orientation='horizontal', size_hint=(1, 0.11))
        row2.add_widget(Label(text="", size_hint=(0.25, 1)))
        b2 = make_button("六爻占卜", 42)
        b2.size_hint = (0.5, 1)
        b2.bind(on_press=lambda x: setattr(self.manager, 'current', 'liuyao'))
        row2.add_widget(b2)
        row2.add_widget(Label(text="", size_hint=(0.25, 1)))
        layout.add_widget(row2)

        layout.add_widget(Label(text="", size_hint=(1, 0.1)))
        self.add_widget(layout)


class CoinScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.locked = False

        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        top = BoxLayout(orientation='horizontal', size_hint=(1, 0.08))
        back = make_button("返回", 36)
        back.size_hint = (0.3, 1)
        back.bind(on_press=self.go_back)
        top.add_widget(back)
        top.add_widget(Label(text="", size_hint=(0.7, 1)))
        layout.add_widget(top)

        self.title = Label(text="2元随地占", font_size=64, bold=True,
                           size_hint=(1, None), height=110, valign='middle')
        layout.add_widget(self.title)

        self.yao_labels = []
        for i in range(6):
            lbl = Label(text="", font_size=64, size_hint=(1, 0.10),
                        halign='center', valign='middle')
            lbl.bind(size=lambda s, v: setattr(s, 'text_size', (v[0], None)))
            layout.add_widget(lbl)
            self.yao_labels.append(lbl)

        self.btn_row = BoxLayout(orientation='horizontal',
                                 size_hint=(1, 0.10), spacing=10)
        self.btn_generate = make_button("生成", 48)
        self.btn_generate.bind(on_press=self.generate_all)
        self.btn_row.add_widget(self.btn_generate)

        self.btn_help = make_button("使用说明", 48)
        self.btn_help.bind(on_press=lambda x: show_help_popup())
        self.btn_row.add_widget(self.btn_help)

        self.btn_save = make_button("保存", 48)
        self.btn_save.bind(on_press=self.save)

        self.btn_refresh = make_button("刷新", 48)
        self.btn_refresh.bind(on_press=self.refresh)

        layout.add_widget(self.btn_row)

        self.count_label = Label(text="已生成次数：0", font_size=38,
                                 size_hint=(1, 0.07))
        layout.add_widget(self.count_label)

        self.add_widget(layout)

    def go_back(self, *a):
        self.manager.current = 'menu'

    def generate_all(self, *a):
        if self.locked:
            return
        for i in range(6):
            self.yao_labels[i].text = get_yao_thick()
        self.locked = True
        self.count_label.text = "已生成次数：6"
        self.btn_generate.disabled = True
        self.btn_generate.text = "已锁止"
        self.btn_row.remove_widget(self.btn_help)
        self.btn_row.add_widget(self.btn_save)
        self.btn_row.add_widget(self.btn_refresh)

    def save(self, *a):
        save_widget_to_png(self, "coin")

    def refresh(self, *a):
        self.locked = False
        for lbl in self.yao_labels:
            lbl.text = ""
        self.count_label.text = "已生成次数：0"
        self.btn_generate.disabled = False
        self.btn_generate.text = "生成"
        self.btn_row.remove_widget(self.btn_save)
        self.btn_row.remove_widget(self.btn_refresh)
        self.btn_row.add_widget(self.btn_help)
class LiuyaoScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.count = 0
        self.results = []

        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        top = BoxLayout(orientation='horizontal', size_hint=(1, 0.08))
        back = make_button("返回", 36)
        back.size_hint = (0.3, 1)
        back.bind(on_press=self.go_back)
        top.add_widget(back)
        top.add_widget(Label(text="", size_hint=(0.7, 1)))
        layout.add_widget(top)

        self.title = Label(text="六爻占卜", font_size=64, bold=True,
                           size_hint=(1, None), height=110, valign='middle')
        layout.add_widget(self.title)

        self.history_rows = []
        for i in range(6):
            row = BoxLayout(orientation='horizontal', size_hint=(1, 0.10))
            left = Label(text="", font_size=26, size_hint=(0.60, 1),
                         halign='center', valign='middle')
            left.bind(size=lambda s, v: setattr(s, 'text_size', (v[0], None)))
            arrow = Label(text="→", font_size=34, size_hint=(0.06, 1),
                          halign='center', valign='middle')
            right = Label(text="", font_size=40, size_hint=(0.34, 1),
                          halign='center', valign='middle')
            right.bind(size=lambda s, v: setattr(s, 'text_size', (v[0], None)))
            row.add_widget(left)
            row.add_widget(arrow)
            row.add_widget(right)
            layout.add_widget(row)
            self.history_rows.append((left, right))

        self.btn_row = BoxLayout(orientation='horizontal',
                                 size_hint=(1, 0.10), spacing=10)
        self.btn_generate = make_button("生成", 48)
        self.btn_generate.bind(on_press=self.generate)
        self.btn_row.add_widget(self.btn_generate)

        self.btn_help = make_button("使用说明", 48)
        self.btn_help.bind(on_press=lambda x: show_help_popup())
        self.btn_row.add_widget(self.btn_help)

        self.btn_save = make_button("保存", 48)
        self.btn_save.bind(on_press=self.save)

        self.btn_refresh = make_button("刷新", 48)
        self.btn_refresh.bind(on_press=self.refresh)

        layout.add_widget(self.btn_row)

        self.count_label = Label(text="已生成次数：0", font_size=38,
                                 size_hint=(1, 0.07))
        layout.add_widget(self.count_label)

        self.final_label = Label(text="", font_size=38, size_hint=(1, 0.07),
                                 halign='center', valign='top')
        self.final_label.bind(size=lambda s, v: setattr(s, 'text_size', (v[0], v[1])))
        layout.add_widget(self.final_label)

        self.add_widget(layout)

    def go_back(self, *a):
        self.manager.current = 'menu'

    def generate(self, *a):
        if self.count >= 6:
            return
        yaos = [get_yao_thin(), get_yao_thin(), get_yao_thin()]
        name = get_gua_name(yaos)
        mid, mark = get_gua_parts(name)

        left_lbl, right_lbl = self.history_rows[5 - self.count]
        left_lbl.text = f"{yaos[0]} | {yaos[1]} | {yaos[2]}"
        right_lbl.text = f"{mid}  {mark}"

        self.results.append(name)
        self.count += 1
        self.count_label.text = f"已生成次数：{self.count}"

        if self.count == 6:
            self.btn_generate.disabled = True
            self.btn_generate.text = "已锁止"
            self.btn_row.remove_widget(self.btn_help)
            self.btn_row.add_widget(self.btn_save)
            self.btn_row.add_widget(self.btn_refresh)

            marks = []
            for i, n in enumerate(self.results):
                if n in ("老阴", "老阳"):
                    marks.append(f"第{i+1}爻")
            self.final_label.text = ("变爻：" + "　".join(marks)) if marks else "变爻：无"

    def save(self, *a):
        save_widget_to_png(self, "liuyao")

    def refresh(self, *a):
        self.count = 0
        self.results = []
        for l, r in self.history_rows:
            l.text = ""
            r.text = ""
        self.count_label.text = "已生成次数：0"
        self.final_label.text = ""
        self.btn_generate.disabled = False
        self.btn_generate.text = "生成"
        self.btn_row.remove_widget(self.btn_save)
        self.btn_row.remove_widget(self.btn_refresh)
        self.btn_row.add_widget(self.btn_help)
class YinyangApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(CoinScreen(name='coin'))
        sm.add_widget(LiuyaoScreen(name='liuyao'))
        return sm


YinyangApp().run()





