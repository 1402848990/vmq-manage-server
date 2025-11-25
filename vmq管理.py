import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# ----------------------------
# 配置
# ----------------------------
BASE_URL = "http://localhost:5500"  # 请根据实际修改
# BASE_URL = "http://47.243.215.58:5500"  # 请根据实际修改
REFRESH_INTERVAL = 5000  # 5秒，单位毫秒


class AccountManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("账号管理系统")
        self.root.geometry("1400x1000")
        self.root.minsize(800, 800)
        self.root.iconbitmap(default=None)  # 可选：设置图标

        # 全局字体（微软雅黑）
        self.font_normal = ("Microsoft YaHei", 10)
        self.font_bold = ("Microsoft YaHei", 10, "bold")
        self.font_title = ("Microsoft YaHei", 14, "bold")
        self.font_stats = ("Microsoft YaHei", 11)

        # 创建界面
        self.create_widgets()

        # 启动自动刷新
        self.auto_refresh_stats()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        # ===== 统计卡片（最顶部）=====
        stats_card = ttk.Frame(main_frame, bootstyle=LIGHT, padding=15)
        stats_card.pack(fill=X, pady=(0, 20), ipadx=10, ipady=10)

        ttk.Label(stats_card, text="📊 账号统计", font=self.font_title,
                  bootstyle=INFO).pack(anchor=W)

        self.stats_text = ttk.Label(
            stats_card,
            text="加载中...",
            font=self.font_stats,
            justify=LEFT,
            wraplength=600,
            bootstyle=DEFAULT
        )
        self.stats_text.pack(anchor=W, pady=(10, 0))

        # ===== 添加账号区域 =====
        add_frame = ttk.Labelframe(main_frame, text="批量添加账号", padding=15)
        add_frame.pack(fill=X, pady=(0, 20))

        self.account_input = scrolledtext.ScrolledText(
            add_frame,
            height=8,
            font=("Consolas", 10),
            wrap=WORD,
            relief=FLAT,
            padx=8,
            pady=8
        )
        self.account_input.pack(fill=BOTH, expand=YES, pady=(0, 10))

        self.add_btn = ttk.Button(
            add_frame,
            text="添加账号",
            bootstyle=SUCCESS,
            command=self.add_accounts,
            width=12
        )
        self.add_btn.pack(side=RIGHT)

        # ===== 日志区域 =====
        log_frame = ttk.Labelframe(main_frame, text="操作日志", padding=15)
        log_frame.pack(fill=BOTH, expand=YES)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            state=DISABLED,
            font=("Consolas", 9),
            wrap=WORD,
            relief=FLAT,
            padx=8,
            pady=8
        )
        self.log_text.pack(fill=BOTH, expand=YES)

    def log(self, message):
        self.log_text.config(state=NORMAL)
        self.log_text.insert(END, f"{message}\n")
        self.log_text.see(END)
        self.log_text.config(state=DISABLED)

    def clear_log(self):
        self.log_text.config(state=NORMAL)
        self.log_text.delete(1.0, END)
        self.log_text.config(state=DISABLED)

    def add_accounts(self):
        print("【DEBUG】按钮点击，准备处理...")  # ← 看这行是否立即打印
        raw = self.account_input.get("1.0", tk.END).strip()
        if not raw:
            messagebox.showwarning("输入为空", "请输入至少一个账号（每行一个）", parent=self.root)
            return

        accounts = [line.strip() for line in raw.splitlines() if line.strip()]
        if not accounts:
            messagebox.showwarning("无效输入", "没有有效的账号内容", parent=self.root)
            return

        # === 立即更新 UI（关键！）===
        self.clear_log()
        self.add_btn.config(state=DISABLED, text="处理中...")
        self.log(f"📤 正在添加 {len(accounts)} 个账号，请稍候...")

        # 立即刷新界面（强制 Tkinter 更新）
        self.root.update_idletasks()

        # 启动后台线程
        threading.Thread(target=self._add_accounts_thread,
                         args=(accounts,), daemon=True).start()

    def _add_accounts_thread(self, accounts):
        print("【DEBUG】添加账号线程启动...")
        try:
            print('1')
            response = requests.post(
                f"{BASE_URL}/add_accounts", json=accounts, timeout=10)
            print('2')
            if response.status_code == 201:
                data = response.json()
                msg = f"✅ 成功添加 {data['message']}，跳过 {data['skipped_due_to_duplicate_or_exist']} 个重复项。"
                self.log(msg)
            else:
                error = response.json().get("error", "未知错误")
                self.log(f"❌ 添加失败: {error}")
        except Exception as e:
            self.log(f"⚠️ 网络异常: {str(e)}")
        finally:
            # 恢复按钮（必须在主线程）
            self.root.after(0, lambda: self.add_btn.config(
                state=NORMAL, text="添加账号"))

    def fetch_stats(self):
        threading.Thread(target=self._fetch_stats_thread, daemon=True).start()

    def _fetch_stats_thread(self):
        try:
            response = requests.get(f"{BASE_URL}/stats", timeout=5)
            if response.status_code == 200:
                data = response.json()
                stats_msg = (
                    f"总账号数：{data['total']}\n"
                    f"已使用：{data['used']} ｜ 未使用：{data['unused']}"
                )
                self.root.after(
                    0, lambda: self.stats_text.config(text=stats_msg))
            else:
                self.root.after(
                    0, lambda: self.stats_text.config(text="❌ 获取统计失败"))
        except Exception as e:
            self.root.after(0, lambda: self.stats_text.config(text=f"⚠️ 网络错误"))

    def auto_refresh_stats(self):
        """每5秒自动刷新统计"""
        self.fetch_stats()
        self.root.after(REFRESH_INTERVAL, self.auto_refresh_stats)


if __name__ == "__main__":
    # 使用 litera 主题 + 微软雅黑全局字体
    root = ttk.Window(
        title="账号管理系统",
        themename="litera",  # ✅ 使用 litera 主题
        size=(720, 600),
        resizable=(True, True)
    )

    # 设置全局字体（ttkbootstrap 支持）
    style = ttk.Style()
    style.configure(".", font=("Microsoft YaHei", 11))  # 默认字体
    style.configure("TButton", font=("Microsoft YaHei", 11))
    style.configure("TLabel", font=("Microsoft YaHei", 11))
    style.configure("TLabelframe.Label", font=("Microsoft YaHei", 11, "bold"))

    app = AccountManagerGUI(root)
    root.mainloop()
