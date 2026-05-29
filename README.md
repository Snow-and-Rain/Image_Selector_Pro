# Image-Selector-Pro / 快速图片多选与筛选工具

A lightweight, ultra-fast Python desktop app built with Tkinter and Pillow for rapid manual image filtering and batch directory cleanup. Optimized for workflows with massive subfolders, it allows you to quickly inspect each directory, select the best shots to keep, and instantly purge the rest to save disk space.

这是一个基于 Python + Tkinter 开发的轻量级本地图片手动筛选与清理工具。专为解决“在大文件夹内包含大量子文件夹，需要人工在每个子文件夹中挑选并保留部分照片、同时清空其余废片”的高频工作场景而设计。通过极致优化的交互逻辑与后台算法，大幅提升人工筛选与硬盘清理的效率。

## Core Features / 核心功能

### English

- **Multi-Select Retention:** Keep one or multiple images freely. The app highlights selected items and will safely delete all unselected images upon confirmation.
- **Dual-Folder Async Preloading:** Powered by background multi-threading. While you are reviewing the current folder, the application automatically processes, resizes, and caches images for the next two valid subfolders in memory. This eliminates disk I/O bottlenecks and ensures absolute zero-loading latency when switching folders.
- **Smart Automated Skipping:** Automatically evaluates image counts within subfolders. Directories with fewer than 2 images (empty or containing only 1 photo) are silently bypassed in the background, saving you from redundant inspection tasks.
- **Crisp Grid Layout:** Displays high-resolution 300x300 thumbnails in a stable 5-column grid layout, highly optimized for modern widescreen monitors. It supports fluent mouse-wheel scrolling for quick navigation.
- **Dynamic Full-Size Preview Pane:** Clicking any thumbnail instantly renders a scaled version of the original image onto the right-side preview panel. This allows for detailed inspection of facial expressions, focus accuracy, and image artifacts.
- **Real-Time Progress Tracking:** Includes a native progress bar and index counter at the top of the interface, providing clear visualization of your overall workflow completion rate.

### 中文

- **支持多选保留：** 不再局限于只保留一张。单击缩略图可自由选中或取消选择多张图片，最终确认后会保留所有选中图片，删除未选中的。
- **双文件夹异步预加载：** 基于底层多线程架构。在您审查当前文件夹时，程序会自动在后台提前加载、裁剪并缓存后续两个有效文件夹的图片。彻底消除由于硬盘读取大图带来的卡顿感，实现无缝切换。
- **智能自动跳过：** 自动检测子文件夹内的图片数量，若图片少于 2 张（无文件或仅 1 张），将自动后台跳过，无需人工进行无意义的判断。
- **高清大网格布局：** 单行展示 5 个 300x300 像素的高清缩略图，针对宽屏显示器深度优化，配合鼠标滚轮可实现流畅的瀑布流滚动。
- **动态大图预览：** 单击任意缩略图，右侧预览区域会自动无缝等比例放大显示原图，方便精细观察人物表情、闭眼或画质细节。
- **实时进度追踪：** 顶部工具栏原生集成了进度条与计数器，直观展示当前处理进度与文件夹总量。

## Prerequisites / 环境要求

- Python 3.x
- Pillow (PIL Fork)

## Installation & Setup / 安装与使用

1. **Clone or Download the Repository / 克隆或下载本项目**

   Download the source files to your local machine.
   将本项目的所有源代码下载或克隆到本地电脑。

2. **Install Dependencies / 安装第三方依赖**

   Open your command line interface (CMD, PowerShell, or Terminal) and run the following command to install the required image processing library:
   打开命令行工具（CMD、PowerShell 或终端），运行以下命令安装唯一的第三方图片处理库：
```bash
   pip install Pillow
   ```

3. **Launch the Application / 运行程序**

  Run the main script from your project root directory:
  在项目根目录下执行以下命令启动程序：
```bash
   python main.py
   ```


## User Guide & Controls / 操作指南与快捷键

### English

- **Select Root Directory:** Upon startup, a native Windows folder picker will appear. Select the top-level folder containing your subfolders.
- **Reviewing and Selecting:**
    - Left Click on any thumbnail to select/deselect it. Selected images will be highlighted with a distinctive blue border.
    - The last-clicked image will always expand on the right side for clear inspection.
- **Execution Options:**
    - Press **Enter** or click **Confirm & Next** (Green Button) to preserve your selected pictures and delete the rest.
    - Double-click a single image to select it and instantly move to the next folder.
    - Click **Skip Folder** (Grey Button) to move on without making any modifications.
    - Click **Delete All (Keep None)** (Red Button) to entirely clear out images in the active folder.
- **Safety Interceptions:**
    - If you select 2 or more photos, a confirmation dialog pops up to prevent accidental bulk deletions.
    - If you try to submit without selecting any photos, the top bar will briefly flash red as a warning without throwing annoying modal popups.

### 中文

- **选择主目录：** 启动后，在弹出的系统对话框中选择包含众多子文件夹的大文件夹。
- **预览与选择：**
    - 鼠标单击左侧缩略图：可将其选中（亮蓝色边框样式），再次单击可取消选中。右侧大图区域会同步显示最后一次点击的高清原图。
- **流程执行控制：**
    - **方法 A：** 按下键盘 **回车键 (Enter)** 或点击绿色按钮 **确认保留并下一组**：保留当前所有勾选的照片，瞬间清空其余照片并载入下一组。
    - **方法 B：** 对某张缩略图执行 **双击**：确保该图片被选中并直接触发保存流转。
    - **方法 C：** 点击灰色按钮 **跳过该文件夹**：不执行任何删除，直接流转至下一个子文件夹。
    - **方法 D：** 点击红色按钮 **全部删除(不保留)**：彻底清空当前子文件夹下的所有照片，一张都不保留。
- **安全防护机制：**
    - **多选确认：** 当选择的照片数量大于或等于 2 张时，执行确认会触发二次弹窗，防止手滑误删。
    - **拦截警告：** 若未选择任何照片误触确认，顶部状态栏会变红闪烁提示，不会弹出打断操作的警告框。

## Customization / 开发者自定义

### English

Advanced users can easily adjust interface metrics directly inside the script:

- `img.thumbnail((300, 300))` - Change thumbnail dimensions.
- `columns_count = 5` - Change the number of thumbnails per row.
- `width=1650` - Tweak the default width allotment for the left grid panel.

### 中文

开发者可以根据具体的显示器分辨率，在源码中直接修改以下参数调整界面布局：

- `img.thumbnail((300, 300))` - 修改左侧缩略图的分辨率大小。
- `columns_count = 5` - 修改每行展示的缩略图数量。
- `width=1650` - 调整左侧网格区域的初始像素宽度。


   
