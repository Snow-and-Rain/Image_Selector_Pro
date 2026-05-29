import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from PIL import Image, ImageTk


class ImageSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片快速筛选工具 Professional")
        self.root.geometry("1920x1000")

        # 支持的图片格式
        self.image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.JPG', '.JPEG', '.PNG')

        self.main_dir = ""
        self.subfolders = []
        self.current_folder_idx = 0

        # 存储多张被选中照片的路径
        self.selected_image_paths = set()
        self.tk_images_cache = {}  # 缓存当前界面的 ImageTk 对象
        self.current_large_image_tk = None  # 缓存当前显示的大图

        # 预加载缓存字典
        self.preload_cache = {}

        self.setup_ui()
        self.select_main_directory()

    def setup_ui(self):
        # 1. 顶部状态栏与操作按钮区
        self.top_frame = tk.Frame(self.root, bg="#f0f0f0", height=80, bd=1, relief="groove")
        self.top_frame.pack(fill=tk.X, side=tk.TOP)

        # 状态文本框
        self.status_label = tk.Label(
            self.top_frame,
            text="请选择主文件夹开始...",
            font=("Microsoft YaHei", 12, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        self.status_label.pack(side=tk.LEFT, padx=20, pady=(10, 5))

        # 操作按钮容器
        self.btn_frame = tk.Frame(self.top_frame, bg="#f0f0f0")
        self.btn_frame.pack(side=tk.LEFT, padx=20, pady=(10, 5))

        # 确认保留按钮
        self.btn_confirm = tk.Button(
            self.btn_frame,
            text="确认保留并下一组",
            font=("Microsoft YaHei", 10, "bold"),
            bg="#28a745",
            fg="#ffffff",
            relief="flat",
            padx=15,
            pady=5,
            command=self.confirm_and_next
        )
        self.btn_confirm.pack(side=tk.LEFT, padx=5)

        # 跳过当前文件夹按钮
        self.btn_skip = tk.Button(
            self.btn_frame,
            text="跳过该文件夹",
            font=("Microsoft YaHei", 10, "bold"),
            bg="#6c757d",
            fg="#ffffff",
            relief="flat",
            padx=15,
            pady=5,
            command=self.skip_folder
        )
        self.btn_skip.pack(side=tk.LEFT, padx=5)

        # 全部删除按钮
        self.btn_delete_all = tk.Button(
            self.btn_frame,
            text="全部删除(不保留)",
            font=("Microsoft YaHei", 10, "bold"),
            bg="#dc3545",
            fg="#ffffff",
            relief="flat",
            padx=15,
            pady=5,
            command=self.delete_all_images
        )
        self.btn_delete_all.pack(side=tk.LEFT, padx=5)

        # 提示栏
        self.tip_label = tk.Label(
            self.top_frame,
            text="操作提示：[单击]选择/取消多选并预览 | [回车Enter]或[点击确认]保留所选 | [双击]直接确认当前选择",
            font=("Microsoft YaHei", 10),
            fg="#ffffff",
            bg="#337ab7",
            padx=10, pady=5
        )
        self.tip_label.pack(side=tk.RIGHT, padx=20, pady=(10, 5))

        # 新增：进度条组件，放置在顶部区域的最下方
        self.progress_bar = ttk.Progressbar(self.top_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=(5, 10))

        # 2. 中间主体区域（使用 PanedWindow 分割左右）
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=5)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 2.1 左侧：缩略图滚动区域
        self.left_panel = tk.Frame(self.paned_window, bg="#ffffff")

        self.canvas = tk.Canvas(self.left_panel, bg="#ffffff", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.left_panel, orient="vertical", command=self.canvas.yview)
        self.image_grid_frame = tk.Frame(self.canvas, bg="#ffffff")

        self.image_grid_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.image_grid_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.paned_window.add(self.left_panel, minsize=800, width=1650)

        # 2.2 右侧：大图预览区域
        self.right_panel = tk.Frame(self.paned_window, bg="#e8e8e8", bd=1, relief="sunken")

        self.preview_label = tk.Label(
            self.right_panel,
            text="单击左侧图片预览大图",
            font=("Microsoft YaHei", 12),
            fg="#666666",
            bg="#e8e8e8"
        )
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.preview_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.paned_window.add(self.right_panel, minsize=250)

        # 3. 绑定全局事件
        self.root.bind("<Return>", self.confirm_and_next)
        self.canvas.bind_all("<MouseWheel>",
                             lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    def select_main_directory(self):
        self.main_dir = filedialog.askdirectory(title="请选择包含子文件夹的大文件夹")
        if not self.main_dir:
            self.root.destroy()
            return

        all_dirs = [os.path.join(self.main_dir, d) for d in os.listdir(self.main_dir) if
                    os.path.isdir(os.path.join(self.main_dir, d))]
        all_dirs.sort()
        self.subfolders = all_dirs

        if not self.subfolders:
            messagebox.showinfo("提示", "所选文件夹内未找到子文件夹")
            self.root.destroy()
            return

        # 新增：设置进度条的最大值为子文件夹的总数
        self.progress_bar['maximum'] = len(self.subfolders)

        self.current_folder_idx = 0
        self.load_current_folder()

    def get_image_files_in_folder(self, folder_path):
        try:
            return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(self.image_extensions)]
        except Exception as e:
            print(f"读取文件夹出错 {folder_path}: {e}")
            return []

    def load_current_folder(self):
        # 新增：实时更新进度条的当前进度数值
        self.progress_bar['value'] = self.current_folder_idx

        if self.current_folder_idx >= len(self.subfolders):
            messagebox.showinfo("大功告成", "所有符合条件的文件夹已筛选完毕！")
            self.root.destroy()
            return

        current_dir = self.subfolders[self.current_folder_idx]
        folder_name = os.path.basename(current_dir)

        img_files = self.get_image_files_in_folder(current_dir)
        num_images = len(img_files)

        # 自动跳过少于2张图片的文件夹
        if num_images < 2:
            print(f"自动跳过文件夹: '{folder_name}' (图片数量: {num_images}, 不需要筛选)")
            self.current_folder_idx += 1
            self.load_current_folder()
            return

            # 从预加载缓存中取出当前文件夹的数据
        preloaded_data = self.preload_cache.pop(current_dir, None)

        for widget in self.image_grid_frame.winfo_children():
            widget.destroy()
        self.tk_images_cache.clear()

        self.preview_label.config(image='', text="单击左侧图片预览大图")
        self.current_large_image_tk = None

        self.selected_image_paths.clear()

        # 修改状态栏文本，增加数字进度显示
        self.status_label.config(
            text=f"进度: {self.current_folder_idx + 1} / {len(self.subfolders)}  |  正在筛选: {folder_name} ({num_images}张)"
        )

        columns_count = 5

        for index, img_path in enumerate(img_files):
            try:
                if preloaded_data and img_path in preloaded_data:
                    img = preloaded_data[img_path]
                else:
                    img = Image.open(img_path)
                    img.thumbnail((300, 300))

                tk_img = ImageTk.PhotoImage(img)
                self.tk_images_cache[img_path] = tk_img

                img_frame = tk.Frame(self.image_grid_frame, bd=4, relief="flat", bg="#ffffff")
                row = index // columns_count
                col = index % columns_count
                img_frame.grid(row=row, column=col, padx=12, pady=12)

                lbl_img = tk.Label(img_frame, image=tk_img, bg="#ffffff")
                lbl_img.pack()

                short_name = os.path.basename(img_path)
                if len(short_name) > 30:
                    short_name = short_name[:27] + "..."
                lbl_name = tk.Label(img_frame, text=short_name, font=("Microsoft YaHei", 9), bg="#ffffff", fg="#555555")
                lbl_name.pack(pady=2)

                for widget in (img_frame, lbl_img, lbl_name):
                    widget.bind("<Button-1>",
                                lambda e, path=img_path, frame=img_frame: self.on_image_select(path, frame))
                    widget.bind("<Double-Button-1>",
                                lambda e, path=img_path, frame=img_frame: self.on_image_double_click(path, frame))

            except Exception as e:
                print(f"无法解析缩略图 {img_path}: {e}")

        # 当前界面渲染好后，立刻检查并触发下两个有效文件夹的后台预加载
        self.start_preload_next()

    def start_preload_next(self):
        """寻找下两个真正符合条件（图片数>=2）的文件夹，并开启后台多线程并行加载它们"""
        idx = self.current_folder_idx + 1
        valid_found_count = 0  # 记录向后找到的有效文件夹数量

        # 【已修改】通过循环向后检索，最多找出 2 个不需要被自动跳过的有效文件夹
        while idx < len(self.subfolders) and valid_found_count < 2:
            folder_path = self.subfolders[idx]
            img_files = self.get_image_files_in_folder(folder_path)

            if len(img_files) >= 2:
                valid_found_count += 1
                # 如果这个文件夹还没有进入缓存，则立刻启动一个新的后台线程进行异步加载
                if folder_path not in self.preload_cache:
                    t = threading.Thread(
                        target=self._preload_worker,
                        args=(folder_path, img_files),
                        daemon=True
                    )
                    t.start()
            idx += 1

    def _preload_worker(self, folder_path, img_files):
        temp_dict = {}
        for img_path in img_files:
            try:
                img = Image.open(img_path)
                img.thumbnail((300, 300))
                img.load()
                temp_dict[img_path] = img
            except Exception as e:
                print(f"后台预加载图片失败 {img_path}: {e}")

        self.preload_cache[folder_path] = temp_dict
        print(f"[预加载成功] 已提前将文件夹 '{os.path.basename(folder_path)}' 的 {len(temp_dict)} 张图片载入缓存。")

    def on_image_select(self, img_path, frame_widget):
        children = frame_widget.winfo_children()
        lbl_img = children[0]
        lbl_name = children[1]

        if img_path in self.selected_image_paths:
            self.selected_image_paths.remove(img_path)
            frame_widget.config(bg="#ffffff", relief="flat")
            lbl_img.config(bg="#ffffff")
            lbl_name.config(bg="#ffffff", fg="#555555")
        else:
            self.selected_image_paths.add(img_path)
            frame_widget.config(bg="#337ab7", relief="solid")
            lbl_img.config(bg="#337ab7")
            lbl_name.config(bg="#337ab7", fg="#ffffff")

        self.show_large_preview(img_path)

    def show_large_preview(self, img_path):
        try:
            self.preview_label.config(text="正在加载预览...")
            self.right_panel.update_idletasks()

            panel_width = self.right_panel.winfo_width() - 20
            panel_height = self.right_panel.winfo_height() - 20

            if panel_width < 50 or panel_height < 50:
                panel_width = 800
                panel_height = 800

            img = Image.open(img_path)
            img.thumbnail((panel_width, panel_height))

            tk_large_img = ImageTk.PhotoImage(img)
            self.current_large_image_tk = tk_large_img

            self.preview_label.config(image=tk_large_img, text="")

        except Exception as e:
            self.preview_label.config(image='', text=f"预览加载失败: {e}")
            print(f"加载大图失败 {img_path}: {e}")

    def on_image_double_click(self, img_path, frame_widget):
        if img_path not in self.selected_image_paths:
            self.on_image_select(img_path, frame_widget)
        self.confirm_and_next()

    def skip_folder(self):
        if self.current_folder_idx >= len(self.subfolders):
            return
        current_dir = self.subfolders[self.current_folder_idx]
        print(f"用户手动跳过文件夹: '{os.path.basename(current_dir)}'")
        self.current_folder_idx += 1
        self.load_current_folder()

    def delete_all_images(self):
        if self.current_folder_idx >= len(self.subfolders):
            return

        current_dir = self.subfolders[self.current_folder_idx]
        folder_name = os.path.basename(current_dir)

        is_confirmed = messagebox.askyesno(
            "危险操作确认",
            f"您确定要【全部删除】文件夹 '{folder_name}' 中的所有照片吗？\n\n注意：执行后该文件夹下的所有照片将被清空，一张都不保留！"
        )
        if not is_confirmed:
            return

        try:
            img_files = self.get_image_files_in_folder(current_dir)
            deleted_count = 0

            for img_path in img_files:
                os.remove(img_path)
                deleted_count += 1

            print(f"文件夹 '{folder_name}' 已彻底清空：删除了全部 {deleted_count} 张照片。")

            self.current_folder_idx += 1
            self.load_current_folder()

        except Exception as e:
            messagebox.showerror("错误", f"在清空文件夹时发生错误: {e}")

    def confirm_and_next(self, event=None):
        if not self.selected_image_paths:
            self.top_frame.config(bg="#f2dede")
            self.status_label.config(text="【请先单击选择至少一张你想保留的照片！】", fg="#a94442", bg="#f2dede")
            self.root.after(1500, lambda: [self.top_frame.config(bg="#f0f0f0"),
                                           self.status_label.config(fg="#333333", bg="#f0f0f0")])
            return

        if len(self.selected_image_paths) >= 2:
            is_confirmed = messagebox.askyesno(
                "确认保留多张照片",
                f"您当前在该文件夹中选择了 {len(self.selected_image_paths)} 张照片。\n\n"
                f"确定要【保留】这 {len(self.selected_image_paths)} 张照片，并【删除】其余未选中的所有照片吗？"
            )
            if not is_confirmed:
                return

        current_dir = self.subfolders[self.current_folder_idx]
        keep_paths = {os.path.normpath(p) for p in self.selected_image_paths}

        try:
            img_files = self.get_image_files_in_folder(current_dir)
            deleted_count = 0

            for img_path in img_files:
                norm_img_path = os.path.normpath(img_path)
                if norm_img_path not in keep_paths:
                    os.remove(norm_img_path)
                    deleted_count += 1

            print(
                f"文件夹 '{os.path.basename(current_dir)}' 处理完成：保留了 {len(keep_paths)} 张，删除了 {deleted_count} 张。")

            self.current_folder_idx += 1
            self.load_current_folder()

        except Exception as e:
            messagebox.showerror("错误", f"自行删除或跳转时发生错误: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    default_font = ("Microsoft YaHei", 10)
    root.option_add("*Font", default_font)
    app = ImageSelectorApp(root)
    root.mainloop()
