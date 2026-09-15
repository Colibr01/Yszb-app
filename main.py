import os
import random
from datetime import datetime
from kivy.core.text import LabelBase
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

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


def get_yao():
    return "━━━━━" if random.random() < 0.5 else "━━　━━"


def get_gua_name(yaos):
    yang_count = sum(1 for y in yaos if y == "━━━━━")
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
        return "█████", "○"
    elif name == "老阴":
        return "██　██", "×"
    elif name == "少阳":
        return "█████", "　"
    else:
        return "██　██", "　"


class YinyangApp(App):
    def build(self):
        self.count = 0
        self.results = []

        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        self.title_label = Label(
            text="雨　神　占　卜　专　用",
            font_size=72,
            bold=True,
            size_hint=(1, None),
            height=120,
            valign='middle'
        )
        layout.add_widget(self.title_label)

        self.history_rows = []
        for i in range(6):
            row = BoxLayout(orientation='horizontal', size_hint=(1, 0.11))
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

        self.btn_generate = Button(text="生成", font_size=48)
        self.btn_generate.bind(on_press=self.generate)
        self.btn_row.add_widget(self.btn_generate)

        self.btn_help = Button(text="使用说明", font_size=48)
        self.btn_help.bind(on_press=self.show_help)
        self.btn_row.add_widget(self.btn_help)

        self.btn_save = Button(text="保存", font_size=48)
        self.btn_save.bind(on_press=self.save_image)

        self.btn_refresh = Button(text="刷新", font_size=48)
        self.btn_refresh.bind(on_press=self.refresh)

        layout.add_widget(self.btn_row)

        self.count_label = Label(text="已生成次数：0", font_size=38,
                                 size_hint=(1, 0.08))
        layout.add_widget(self.count_label)

        self.final_label = Label(
            text="", font_size=38, size_hint=(1, 0.08),
            halign='center', valign='top'
        )
        self.final_label.bind(size=lambda s, v: setattr(s, 'text_size', (v[0], v[1])))
        layout.add_widget(self.final_label)

        return layout

    def generate(self, instance):
        if self.count >= 6:
            return

        yaos = [get_yao(), get_yao(), get_yao()]
        name = get_gua_name(yaos)
        mid_text, mark_text = get_gua_parts(name)

        left_text = f"{yaos[0]} | {yaos[1]} | {yaos[2]}"
        right_text = f"{mid_text}  {mark_text}"

        left_lbl, right_lbl = self.history_rows[5 - self.count]
        left_lbl.text = left_text
        right_lbl.text = right_text

        self.results.append((yaos, name))
        self.count += 1
        self.count_label.text = f"已生成次数：{self.count}"

        if self.count == 6:
            self.btn_generate.disabled = True
            self.btn_generate.text = "已锁止"

            self.btn_row.remove_widget(self.btn_help)
            self.btn_row.add_widget(self.btn_save)
            self.btn_row.add_widget(self.btn_refresh)

            marks = []
            for i, (yaos, name) in enumerate(self.results):
                if name in ("老阴", "老阳"):
                    marks.append(f"第{i+1}爻")

            if marks:
                self.final_label.text = "变爻：" + "　".join(marks)
            else:
                self.final_label.text = "变爻：无"
    def show_help(self, instance):
        content = BoxLayout(orientation='vertical', padding=20, spacing=12)
        help_text = (
            "0.生成六次保存发给雨神\n\n" 
            "1. 唯独雨神占卜有效\n\n"
            "2. 占卜时心诚则灵\n\n"
            "3. 建议占卜间隔不低于两月\n\n"
            "4. 此占卜较为深度，简易占卜雨神在开发"
        )
        lbl = Label(text=help_text, font_size=36,
                    halign='left', valign='top')
        lbl.bind(size=lambda s, v: setattr(s, 'text_size', (v[0], None)))
        content.add_widget(lbl)

        close_btn = Button(text="关闭", size_hint=(1, 0.3), font_size=40)
        content.add_widget(close_btn)

        popup = Popup(
            title="使用说明",
            content=content,
            size_hint=(0.88, 0.7),
            title_size=40
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def save_image(self, instance):
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
                "yinyang_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
            )
            self.root.export_to_png(filename)
            self._toast("已保存到：\n" + filename)
        except Exception as e:
            self._toast("保存失败：\n" + str(e))

    def _toast(self, msg):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        lbl = Label(text=msg, font_size=24)
        content.add_widget(lbl)
        ok = Button(text="好的", size_hint=(1, 0.5), font_size=36)
        content.add_widget(ok)
        popup = Popup(title="提示", content=content,
                      size_hint=(0.8, 0.4), title_size=30)
        ok.bind(on_press=popup.dismiss)
        popup.open()

    def refresh(self, instance):
        self.count = 0
        self.results = []

        for left_lbl, right_lbl in self.history_rows:
            left_lbl.text = ""
            right_lbl.text = ""

        self.count_label.text = "已生成次数：0"
        self.final_label.text = ""

        self.btn_generate.disabled = False
        self.btn_generate.text = "生成"

        self.btn_row.remove_widget(self.btn_save)
        self.btn_row.remove_widget(self.btn_refresh)
        self.btn_row.add_widget(self.btn_help)


YinyangApp().run()          
