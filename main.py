# -*- coding: utf-8 -*-
"""
ガンマ補正チャート表示アプリケーション

このアプリケーションは、Tkinterを使用してガンマ補正の視覚的な比較を行うGUIツールです。

主な機能:
- 異なるガンマ値（2.2, 2.0, 1.8, 1.0）の補正チャートをタブ形式で表示
- RGB各色（赤、緑、青）およびグレースケールでのガンマ補正効果を比較
- 交互配置（市松模様）と単色配置の2種類のパターンで補正結果を表示
- 異なる輝度レベル（0%, 25%, 50%, 75%, 100%）での補正効果を視覚化

使用方法:
1. アプリケーションを起動すると、4つのタブが表示されます
2. 各タブには対応するガンマ値の補正チャートが表示されます
3. チャートはRGB各色とグレースケールの組み合わせで構成されています
4. 交互配置と単色配置の違いを比較することで、ガンマ補正の効果を理解できます

技術仕様:
- XPM（X PixMap）形式を使用してピクセルデータを表現
- 16x16ピクセルの基本パターンを12x12グリッドで配置
- ガンマ補正には標準的な指数関数を使用: output = input^gamma
"""

import tkinter as tk
from tkinter import ttk


class Xpm:
    """
    XPM（X PixMap）データ表現の基底クラス。

    XPMはX Window Systemで使用されるピクセルマップ形式で、
    テキストベースで画像データを表現します。このクラスは
    XPMデータの生成とPhotoImageへの変換機能を提供します。

    Attributes:
        _data (list): XPM形式のデータ行リスト
        size (int): 基本パターンのサイズ（16ピクセル）
    """

    _data = []
    size = 16  # 基本パターンのサイズ（16x16ピクセル）

    @property
    def data(self):
        """XPMデータリストを返すプロパティ。"""
        return self._data

    @staticmethod
    def create_photo_image(parent, xpm_data):
        """
        XPMデータを解析し、tkinter.PhotoImageオブジェクトを生成します。

        Args:
            parent: PhotoImageの親ウィジェット。
            xpm_data: XPM形式のデータリスト。

        Returns:
            生成されたtkinter.PhotoImageオブジェクト。
        """
        # XPMデータの解析
        # ヘッダー行から基本情報を読み取る
        # XPMヘッダー形式: "width height num_colors chars_per_pixel"
        header = xpm_data[0].strip().split()
        width, height, num_colors, chars_per_pixel = map(int, header)

        # カラーマップを作成する
        color_map = {}
        for i in range(num_colors):
            line = xpm_data[i + 1]
            char = line[0]  # 行の先頭から文字シンボルを取得
            parts = line.strip().split()
            color = parts[-1]  # 行の末尾から色定義を取得
            color_map[char] = color

        # PhotoImageオブジェクトを作成し、ピクセルデータを設定する
        image = tk.PhotoImage(master=parent, width=width, height=height)
        for y in range(height):
            row_str = ""
            pixel_row = xpm_data[y + 1 + num_colors]
            for x in range(width):
                char = pixel_row[x * chars_per_pixel : (x + 1) * chars_per_pixel]
                row_str += color_map[char] + " "
            # 1行分のピクセルデータをPhotoImageに設定
            image.put("{" + row_str.strip() + "}", to=(0, y))
        return image


class SingleColorXpm(Xpm):
    """
    単色のXPMデータを生成するクラス。

    指定されたRGB値で塗りつぶされた単色のパターンを生成します。
    ガンマチャートで単色領域の補正効果を表示するために使用されます。

    Args:
        red (str): 赤成分の16進数文字列（2桁）
        green (str): 緑成分の16進数文字列（2桁）
        blue (str): 青成分の16進数文字列（2桁）
    """

    def __init__(self, red, green, blue):
        """
        指定されたRGB値で単色のXPMデータを初期化します。
        """
        self._data = [
            f"{Xpm.size * 2} {Xpm.size * 2} 1 1",  # XPMヘッダー: 幅、高さ、色数、1ピクセルあたりの文字数
            f"  c #{red}{green}{blue}",  # 色定義: 空白文字をキーとしてRGB値を定義
        ]
        for _ in range(Xpm.size * 2):
            self._data.append(" " * (Xpm.size * 2))


class AlternateXpm(Xpm):
    """
    2色を交互に配置した市松模様のXPMデータを生成するクラス。

    2つのRGB値を交互に配置することで市松模様パターンを生成します。
    ガンマチャートで交互配置領域の補正効果を表示するために使用されます。
    これにより、隣接する異なる輝度値のコントラストがガンマ補正により
    どのように変化するかを視覚的に確認できます。

    Args:
        red1 (str): 1色目の赤成分の16進数文字列（2桁）
        green1 (str): 1色目の緑成分の16進数文字列（2桁）
        blue1 (str): 1色目の青成分の16進数文字列（2桁）
        red2 (str): 2色目の赤成分の16進数文字列（2桁）
        green2 (str): 2色目の緑成分の16進数文字列（2桁）
        blue2 (str): 2色目の青成分の16進数文字列（2桁）
    """

    def __init__(self, red1, green1, blue1, red2, green2, blue2):
        """
        指定された2つのRGB値で市松模様のXPMデータを初期化します。
        """
        self._data = [
            f"{Xpm.size * 2} {Xpm.size * 2} 2 1",  # XPMヘッダー: 幅、高さ、色数、1ピクセルあたりの文字数
            f"  c #{red1}{green1}{blue1}",  # 1色目の定義（空白文字をキー）
            f". c #{red2}{green2}{blue2}",  # 2色目の定義（ドット文字をキー）
        ]
        for _ in range(Xpm.size):
            self._data.append(". " * Xpm.size)
            self._data.append(" ." * Xpm.size)


class GammaChart(tk.Canvas):
    """
    ガンマ補正チャートを表示するためのTkinterキャンバスウィジェット。

    指定されたガンマ値に基づいて、RGB各色とグレースケールの組み合わせで
    ガンマ補正効果を視覚的に表現します。チャートは12x12グリッド状に
    16x16ピクセルの基本パターンを配置することで構成されます。

    チャートの構成:
    - 左上: グレースケールパターン（交互配置 + 単色配置）
    - 右上: 赤色パターン（交互配置 + 単色配置）
    - 左下: 緑色パターン（交互配置 + 単色配置）
    - 右下: 青色パターン（交互配置 + 単色配置）

    各色セクション内では、異なる輝度レベル（25%, 50%, 75%）での
    補正効果を交互配置と単色配置で比較表示します。

    Args:
        parent: 親ウィジェット（通常はttk.Notebook）
        gamma (float): ガンマ値（1.0, 1.8, 2.0, 2.2など）
    """

    def __init__(self, parent, gamma):
        """
        ガンマチャートを初期化し、指定されたガンマ値に基づいて描画します。

        Args:
            parent: 親ウィジェット。
            gamma: ガンマ値。
        """
        xpm_side = Xpm.size * 2  # XPMパターンのサイズ（16x2=32ピクセル）
        image_side = xpm_side * 12  # 全体画像サイズ（32x12=384ピクセル）
        super().__init__(parent, width=image_side, height=image_side)

        # ガンマ補正を適用した輝度値を計算
        # ガンマ補正の公式: output = input^gamma
        # ただし、通常のガンマ補正は output = input^(1/gamma) で行われる
        # これはディスプレイの非線形性による色ずれを補正するため
        #
        # 計算ステップ:
        # 1. 入力値を0-1の範囲に正規化 (value / 255.0)
        # 2. ガンマ補正を適用 (normalized_value^(1/gamma))
        # 3. 0-255の範囲に戻す (corrected_value * 255)
        # 4. 整数に丸めて16進数2桁形式に変換
        v000 = f"{int(round(pow(0 / 255.0, 1.0 / gamma) * 255)):02x}"  # 0% (黒)
        v025 = (
            f"{int(round(pow(63 / 255.0, 1.0 / gamma) * 255)):02x}"  # 25% (暗いグレー)
        )
        v050 = (
            f"{int(round(pow(127 / 255.0, 1.0 / gamma) * 255)):02x}"  # 50% (中間グレー)
        )
        v075 = f"{int(round(pow(191 / 255.0, 1.0 / gamma) * 255)):02x}"  # 75% (明るいグレー)
        v100 = f"{int(round(pow(255 / 255.0, 1.0 / gamma) * 255)):02x}"  # 100% (白)

        # XPMデータからPhotoImageオブジェクトを生成
        images = {
            # 全色 (グレー)
            "all_a025": Xpm.create_photo_image(
                self, AlternateXpm(v000, v000, v000, v050, v050, v050).data
            ),
            "all_a050": Xpm.create_photo_image(
                self, AlternateXpm(v000, v000, v000, v100, v100, v100).data
            ),
            "all_a075": Xpm.create_photo_image(
                self, AlternateXpm(v050, v050, v050, v100, v100, v100).data
            ),
            "all_s025": Xpm.create_photo_image(
                self, SingleColorXpm(v025, v025, v025).data
            ),
            "all_s050": Xpm.create_photo_image(
                self, SingleColorXpm(v050, v050, v050).data
            ),
            "all_s075": Xpm.create_photo_image(
                self, SingleColorXpm(v075, v075, v075).data
            ),
            # 赤
            "red_a025": Xpm.create_photo_image(
                self, AlternateXpm(v000, v000, v000, v050, v000, v000).data
            ),
            "red_a050": Xpm.create_photo_image(
                self, AlternateXpm(v000, v000, v000, v100, v000, v000).data
            ),
            "red_a075": Xpm.create_photo_image(
                self, AlternateXpm(v050, v000, v000, v100, v000, v000).data
            ),
            "red_s025": Xpm.create_photo_image(
                self, SingleColorXpm(v025, v000, v000).data
            ),
            "red_s050": Xpm.create_photo_image(
                self, SingleColorXpm(v050, v000, v000).data
            ),
            "red_s075": Xpm.create_photo_image(
                self, SingleColorXpm(v075, v000, v000).data
            ),
            # 緑
            "green_a025": Xpm.create_photo_image(
                self, AlternateXpm(v000, v000, v000, v000, v050, v000).data
            ),
            "green_a050": Xpm.create_photo_image(
                self, AlternateXpm(v000, v000, v000, v000, v100, v000).data
            ),
            "green_a075": Xpm.create_photo_image(
                self, AlternateXpm(v000, v050, v000, v000, v100, v000).data
            ),
            "green_s025": Xpm.create_photo_image(
                self, SingleColorXpm(v000, v025, v000).data
            ),
            "green_s050": Xpm.create_photo_image(
                self, SingleColorXpm(v000, v050, v000).data
            ),
            "green_s075": Xpm.create_photo_image(
                self, SingleColorXpm(v000, v075, v000).data
            ),
            # 青
            "blue_a025": Xpm.create_photo_image(
                self, AlternateXpm(v000, v000, v000, v000, v000, v050).data
            ),
            "blue_a050": Xpm.create_photo_image(
                self, AlternateXpm(v000, v000, v000, v000, v000, v100).data
            ),
            "blue_a075": Xpm.create_photo_image(
                self, AlternateXpm(v000, v000, v050, v000, v000, v100).data
            ),
            "blue_s025": Xpm.create_photo_image(
                self, SingleColorXpm(v000, v000, v025).data
            ),
            "blue_s050": Xpm.create_photo_image(
                self, SingleColorXpm(v000, v000, v050).data
            ),
            "blue_s075": Xpm.create_photo_image(
                self, SingleColorXpm(v000, v000, v075).data
            ),
        }

        # ガベージコレクションを防ぐために画像の参照を保持
        self._images = list(images.values())

        # チャートのパッチのレイアウト定義
        # 各色セクションの開始位置を定義（列インデックス）
        # グリッドは4つの領域に分かれている:
        # - 列0-2: グレースケール（all）
        # - 列3-5: 赤色（red）
        # - 列6-8: 緑色（green）
        # - 列9-11: 青色（blue）
        layout = [("all", 0, 0), ("red", 3, 0), ("green", 6, 0), ("blue", 9, 0)]

        # 各輝度レベルでの交互配置（a）と単色配置（s）の配置パターン
        # 各行は異なる輝度レベルを表す:
        # - 行0: 25%輝度パターン
        # - 行1: 50%輝度パターン
        # - 行2: 75%輝度パターン
        # 各列は交互配置と単色配置の繰り返し
        patterns = [
            ("a025", 0, 0),
            ("s025", 1, 0),
            ("a025", 2, 0),
            ("s025", 3, 0),  # 25%行
            ("a050", 4, 0),
            ("s050", 5, 0),
            ("a050", 6, 0),
            ("s050", 7, 0),  # 50%行
            ("a075", 8, 0),
            ("s075", 9, 0),
            ("a075", 10, 0),
            ("s075", 11, 0),  # 75%行
            ("s025", 0, 1),
            ("a025", 1, 1),
            ("s025", 2, 1),
            ("a025", 3, 1),  # 交互パターン
            ("s050", 4, 1),
            ("a050", 5, 1),
            ("s050", 6, 1),
            ("a050", 7, 1),
            ("s075", 8, 1),
            ("a075", 9, 1),
            ("s075", 10, 1),
            ("a075", 11, 1),
            ("a025", 0, 2),
            ("s025", 1, 2),
            ("a025", 2, 2),
            ("s025", 3, 2),  # 追加パターン
            ("a050", 4, 2),
            ("s050", 5, 2),
            ("a050", 6, 2),
            ("s050", 7, 2),
            ("a075", 8, 2),
            ("s075", 9, 2),
            ("a075", 10, 2),
            ("s075", 11, 2),
        ]

        # レイアウト定義に従って画像をキャンバスに配置
        # 各色セクション（グレースケール、赤、緑、青）に対して
        # すべてのパターン（交互配置、単色配置）を配置する
        for color_name, row_offset, col_offset in layout:
            for pattern_name, col, row in patterns:
                img_key = f"{color_name}_{pattern_name}"
                if img_key in images:
                    # 座標計算:
                    # - x座標: (パターン列 + 色セクション列オフセット) × XPMパターンサイズ
                    # - y座標: (パターン行 + 色セクション行オフセット) × XPMパターンサイズ
                    # これにより、各パターンがグリッド状に整列して配置される
                    x = (col + col_offset) * xpm_side
                    y = (row + row_offset) * xpm_side
                    self.create_image(x, y, image=images[img_key], anchor="nw")


class MainWindow(tk.Tk):
    """
    ガンマチャートアプリケーションのメインウィンドウ。

    アプリケーションのメインコンテナとして機能し、以下のコンポーネントを管理します:
    - メニューバー（ファイルメニュー、終了機能）
    - タブ付きインターフェース（異なるガンマ値のチャート表示）
    - ウィンドウのサイズと位置の自動調整

    キーボードショートカット:
    - Ctrl+Q: アプリケーション終了

    Attributes:
        自動的に生成されるGUIコンポーネントを内部に保持
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Gamma chart")
        self.protocol(
            "WM_DELETE_WINDOW", self.quit
        )  # ウィンドウを閉じるボタンの動作を設定

        # メニューバーの作成
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Quit", command=self.quit, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=file_menu, underline=0)
        self.config(menu=menubar)
        self.bind_all(
            "<Control-q>", lambda event: self.quit()
        )  # ショートカットキーの設定

        # タブ付きインターフェース（Notebook）の作成
        notebook = ttk.Notebook(self)

        # 各ガンマ値に対応するタブとガンマチャートを追加
        notebook.add(GammaChart(notebook, gamma=2.2), text="Gamma=2.2", underline=6)
        notebook.add(GammaChart(notebook, gamma=2.0), text="Gamma=2.0", underline=6)
        notebook.add(GammaChart(notebook, gamma=1.8), text="Gamma=1.8", underline=6)
        notebook.add(GammaChart(notebook, gamma=1.0), text="Gamma=1.0", underline=6)

        notebook.pack(expand=True, fill="both", padx=5, pady=5)

        # ウィンドウを画面中央に表示
        self.update_idletasks()  # ウィンドウのサイズが確定するのを待つ
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


def main():
    """
    アプリケーションのメイン関数。
    """
    win = MainWindow()
    win.mainloop()


# スクリプトが直接実行された場合にmain関数を呼び出す
if __name__ == "__main__":
    main()
