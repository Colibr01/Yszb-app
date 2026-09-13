import os
import random
from kivy.core.text import LabelBase
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

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

        layout = BoxLayout(orientation='vertical', padding=15, spacing=12)

        self.title_label = Label(
            text="雨　神　占　卜　专　用",
            font_size=80,
            bold=True,
            size_hint=(1, None),
            height=130,
            valign='middle'
        )
        layout.add_widget(self.title_label)

        # 六行爻：左(爻, 字号小) + 中(箭头) + 右(符号+标记)
        self.history_rows = []
        for i in range(6):
            row = BoxLayout(orientation='horizontal', size_hint=(1, 0.12))

            left = Label(text="", font_size=26, size_hint=(0.62, 1),
                         halign='center', valign='middle')
            left.bind(size=lambda s, v: setattr(s, 'text_size', (v[0], None)))

            arrow = Label(text="→", font_size=34, size_hint=(0.06, 1),
                          halign='center', valign='middle')

            right = Label(text="", font_size=42, size_hint=(0.32, 1),
                          halign='center', valign='middle')
            right.bind(size=lambda s, v: setattr(s, 'text_size', (v[0], None)))

            row.add_widget(left)
            row.add_widget(arrow)
            row.add_widget(right)
            layout.add_widget(row)
            self.history_rows.append((left, right))

        # 生成按钮：宽度 60% 居中
        btn_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))
        btn_row.add_widget(Label(text="", size_hint=(0.2, 1)))
        self.btn = Button(text="生成", size_hint=(0.6, 1), font_size=44)
        self.btn.bind(on_press=self.generate)
        btn_row.add_widget(self.btn)
        btn_row.add_widget(Label(text="", size_hint=(0.2, 1)))
        layout.add_widget(btn_row)

        self.count_label = Label(text="已生成次数：0", font_size=45, size_hint=(1, 0.1))
        layout.add_widget(self.count_label)

        self.final_label = Label(
            text="", font_size=45, size_hint=(1, 0.1),
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

        left_text = f"{yaos[0]}        |        {yaos[1]}        |     {yaos[2]}"
        right_text = f"{mid_text}  {mark_text}"

        left_lbl, right_lbl = self.history_rows[5 - self.count]
        left_lbl.text = left_text
        right_lbl.text = right_text

        self.results.append((yaos, name))
        self.count += 1
        self.count_label.text = f"已生成次数：{self.count}"

        if self.count == 6:
            self.btn.disabled = True
            self.btn.text = "已锁止"

            marks = []
            for i, (yaos, name) in enumerate(self.results):
                if name in ("老阴", "老阳"):
                    marks.append(f"第{i+1}爻")

            if marks:
                self.final_label.text = "变爻：" + "　".join(marks)
            else:
                self.final_label.text = "变爻：无"

YinyangApp().run()
