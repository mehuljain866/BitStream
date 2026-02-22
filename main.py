import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import math
import os
import sys
from pathlib import Path

# ─── BACKEND CONNECTION ──────────────────────────────────────────────────────
try:
    import index as backend
    HAS_BACKEND = True
except ImportError:
    HAS_BACKEND = False
    print("!! BACKEND MISSING: Make sure index.py is in the same folder !!")

# ─── VISUAL STYLE CONSTANTS ──────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
BG      = "#000000"      # Pure black background
CYAN    = "#6FFFE9"      # Files side color
BLUE    = "#3A86FF"      # Video side & arrows
WHITE   = "#EAEAEA"      # Text
DIM     = "#666666"      # Dim gray for gear
GRAY    = "#333333"      # Settings separators

# ─── MAIN UI CLASS ───────────────────────────────────────────────────────────
class BitStreamApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("file → video")
        self.geometry("480x600")
        self.resizable(False, False)
        self.configure(fg_color=BG)
        
        self.is_running = False
        self.settings_window = None
        
        # 1. Setup the Canvas (The Visuals)
        self.setup_canvas()
        # 2. Setup the Buttons (The Controls)
        self.setup_widgets()

    def setup_canvas(self):
        """Draw the circular diagram matching your sketch exactly"""
        W, H = 480, 600
        self.canvas = tk.Canvas(self, width=W, height=H, bg=BG, highlightthickness=0, bd=0)
        self.canvas.place(x=0, y=0)
        
        # Circle center and radius
        CX, CY = W // 2, 230
        R = 118
        
        # ─── Upper arc (Files → Video) ───
        self.canvas.create_arc(CX - R, CY - R, CX + R, CY + R,
                               start=10, extent=160,
                               outline=BLUE, width=2, style="arc")
        # Arrow at right end of top arc
        ax, ay = self.arc_point(10, R, CX, CY)
        self.draw_arrow(ax, ay, -80, BLUE)
        
        # ─── Lower arc (Video → Files) ───
        self.canvas.create_arc(CX - R, CY - R, CX + R, CY + R,
                               start=190, extent=160,
                               outline=BLUE, width=2, style="arc")
        # Arrow at left end of bottom arc
        bx, by = self.arc_point(190, R, CX, CY)
        self.draw_arrow(bx, by, 100, BLUE)
        
        # ─── "Files" label (left, cyan) ───
        self.lbl_files = self.canvas.create_text(CX - R - 14, CY,
                                                 text="Files",
                                                 fill=CYAN, anchor="e",
                                                 font=("Inter", 26, "bold"),
                                                 tags="files_tag")
        
        # ─── "Video" label (right, cyan) ───
        self.lbl_video = self.canvas.create_text(CX + R + 14, CY,
                                                 text="Video",
                                                 fill=CYAN, anchor="w",
                                                 font=("Inter", 26, "bold"),
                                                 tags="video_tag")
        
        # ─── Settings gear button (top-left) ───
        self.gear_cx, self.gear_cy = 30, 30
        self.gear_r = 12
        
        # Invisible circle for easier clicking
        self.canvas.create_oval(
            self.gear_cx - 20, self.gear_cy - 20,
            self.gear_cx + 20, self.gear_cy + 20,
            fill=BG, outline="", tags="gear_btn"
        )
        self.draw_gear_icon(self.gear_cx, self.gear_cy, self.gear_r, DIM)
        
        # ─── Progress bar area ───
        PROG_Y = 440
        self.eta_id = self.canvas.create_text(W - 20, PROG_Y - 18,
                                              text="est time: -",
                                              fill=WHITE, anchor="e",
                                              font=("Inter", 11))
        
        PB_X0, PB_X1 = 60, W - 60
        PB_Y0, PB_Y1 = PROG_Y, PROG_Y + 30
        self.canvas.create_rectangle(PB_X0, PB_Y0, PB_X1, PB_Y1,
                                     outline=CYAN, width=2, fill=BG)
        
        self.PB_INNER_X0 = PB_X0 + 3
        self.PB_INNER_Y0 = PB_Y0 + 3
        self.PB_INNER_X1 = self.PB_INNER_X0
        self.PB_INNER_Y1 = PB_Y1 - 3
        self.MAX_PB_W = PB_X1 - PB_X0 - 6
        
        self.fill_bar = self.canvas.create_rectangle(
            self.PB_INNER_X0, self.PB_INNER_Y0,
            self.PB_INNER_X1, self.PB_INNER_Y1,
            fill=BLUE, outline=""
        )
        
        self.pct_id = self.canvas.create_text(W // 2, PB_Y1 + 18,
                                              text="0%",
                                              fill=BLUE, anchor="n",
                                              font=("Inter", 13, "bold"))
        
        # ─── Event bindings ───
        self.canvas.tag_bind("files_tag", "<Button-1>", lambda e: self.action_files())
        self.canvas.tag_bind("files_tag", "<Enter>", self.on_enter_files)
        self.canvas.tag_bind("files_tag", "<Leave>", self.on_leave_files)
        
        self.canvas.tag_bind("video_tag", "<Button-1>", lambda e: self.action_video())
        self.canvas.tag_bind("video_tag", "<Enter>", self.on_enter_video)
        self.canvas.tag_bind("video_tag", "<Leave>", self.on_leave_video)
        
        self.canvas.tag_bind("gear_btn", "<Button-1>", lambda e: self.open_settings())
        self.canvas.tag_bind("gear_btn", "<Enter>", self.on_gear_enter)
        self.canvas.tag_bind("gear_btn", "<Leave>", self.on_gear_leave)
        self.canvas.tag_bind("gear_icon", "<Button-1>", lambda e: self.open_settings())

    def arc_point(self, angle_deg, radius, cx, cy):
        """Get point on circle at given angle"""
        a = math.radians(angle_deg)
        return cx + radius * math.cos(a), cy - radius * math.sin(a)

    def draw_arrow(self, cx, cy, angle_deg, color):
        """Draw triangle arrowhead"""
        a = math.radians(angle_deg)
        size = 11
        tip = (cx + size * math.cos(a), cy - size * math.sin(a))
        left = (cx + size * math.cos(a + 2.4), cy - size * math.sin(a + 2.4))
        right = (cx + size * math.cos(a - 2.4), cy - size * math.sin(a - 2.4))
        self.canvas.create_polygon(tip, left, right, fill=color, outline="")

    def draw_gear_icon(self, cx, cy, r, color):
        """Draw gear icon for settings"""
        # Outer circle
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r,
                               outline=color, width=2, fill=BG, tags="gear_icon")
        # Center hole
        self.canvas.create_oval(cx-r//3, cy-r//3, cx+r//3, cy+r//3,
                               outline=color, width=1, fill=BG, tags="gear_icon")
        # Teeth
        for angle in range(0, 360, 60):
            a = math.radians(angle)
            x1 = cx + (r-2) * math.cos(a)
            y1 = cy + (r-2) * math.sin(a)
            x2 = cx + (r+4) * math.cos(a)
            y2 = cy + (r+4) * math.sin(a)
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=3, tags="gear_icon")

    def setup_widgets(self):
        """Create convert buttons overlaid on canvas"""
        CX, CY = 240, 230
        R = 118
        
        # Top convert button (Files → Video)
        top_btn_y = CY - R - 14
        self.btn_enc = ctk.CTkButton(self, text="convert",
                                     command=self.run_encode,
                                     width=104, height=28,
                                     fg_color=BG,
                                     border_width=2,
                                     border_color=WHITE,
                                     text_color=WHITE,
                                     hover_color=GRAY,
                                     font=("Inter", 12, "bold"))
        self.btn_enc.place(x=CX-52, y=top_btn_y-14)
        
        # Bottom convert button (Video → Files)
        bot_btn_y = CY + R + 14
        self.btn_dec = ctk.CTkButton(self, text="convert",
                                     command=self.run_decode,
                                     width=104, height=28,
                                     fg_color=BG,
                                     border_width=2,
                                     border_color=WHITE,
                                     text_color=WHITE,
                                     hover_color=GRAY,
                                     font=("Inter", 12, "bold"))
        self.btn_dec.place(x=CX-52, y=bot_btn_y-14)
        
        # Cover video button (appears below bottom convert when steg enabled)
        self.cover_btn_y = bot_btn_y + 50
        self.btn_cover = ctk.CTkButton(self, text="🎬 Upload Cover Video",
                                       command=lambda: self.do_upload(backend.upload_cover_video),
                                       width=140, height=32,
                                       fg_color=BG,
                                       border_width=2,
                                       border_color=CYAN,
                                       text_color=CYAN,
                                       hover_color=GRAY,
                                       font=("Inter", 11, "bold"))
        self.update_cover_btn_visibility()

    def update_cover_btn_visibility(self):
        """Show/hide cover button based on steg setting"""
        if HAS_BACKEND and backend.is_steg_enabled():
            self.btn_cover.place(x=240-70, y=self.cover_btn_y-16)
        else:
            self.btn_cover.place_forget()

    # ─── HOVER EFFECTS ───────────────────────────────────────────────────────
    def on_enter_files(self, e):
        self.canvas.itemconfig(self.lbl_files, fill=WHITE)
        self.canvas.configure(cursor="hand2")
    
    def on_leave_files(self, e):
        self.canvas.itemconfig(self.lbl_files, fill=CYAN)
        self.canvas.configure(cursor="")
    
    def on_enter_video(self, e):
        self.canvas.itemconfig(self.lbl_video, fill=WHITE)
        self.canvas.configure(cursor="hand2")
    
    def on_leave_video(self, e):
        self.canvas.itemconfig(self.lbl_video, fill=CYAN)
        self.canvas.configure(cursor="")
    
    def on_gear_enter(self, e):
        self.canvas.delete("gear_icon")
        self.draw_gear_icon(self.gear_cx, self.gear_cy, self.gear_r, WHITE)
        self.canvas.configure(cursor="hand2")
    
    def on_gear_leave(self, e):
        self.canvas.delete("gear_icon")
        self.draw_gear_icon(self.gear_cx, self.gear_cy, self.gear_r, DIM)
        self.canvas.configure(cursor="")

    # ─── ACTIONS (CONNECTED TO BACKEND) ──────────────────────────────────────
    def action_files(self):
        """Show popup menu when clicking 'Files'"""
        menu = tk.Menu(self, tearoff=0, bg="#222", fg="white",
                       activebackground=CYAN, activeforeground="black",
                       font=("Inter", 10))
        menu.add_command(label="📁 Upload Files",
                         command=lambda: self.do_upload(backend.upload_files))
        menu.add_command(label="📂 Upload Folder",
                         command=lambda: self.do_upload(backend.upload_folder))
        
        if HAS_BACKEND and backend.is_steg_enabled():
            menu.add_separator()
            menu.add_command(label="🎬 Upload Cover Video",
                             command=lambda: self.do_upload(backend.upload_cover_video))
        
        menu.tk_popup(self.winfo_pointerx(), self.winfo_pointery())

    def do_upload(self, func):
        if func():
            self.canvas.itemconfig(self.eta_id, text="Input Loaded")
            self.flash_text(self.lbl_files, CYAN)
        return True

    def action_video(self):
        """Open output folder when clicking 'Video'"""
        # FIX: Changed OUTPUT_VIDEO_DIR to OUTPUT_VIDEO to match index.py
        path = backend.OUTPUT_VIDEO if HAS_BACKEND else Path("./output")
        path.mkdir(parents=True, exist_ok=True)
        
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            os.system(f'open "{path}"')
        else:
            os.system(f'xdg-open "{path}"')
        
        self.flash_text(self.lbl_video, CYAN)

    def flash_text(self, tag, color):
        self.canvas.itemconfig(tag, fill=WHITE)
        self.after(150, lambda: self.canvas.itemconfig(tag, fill=color))

    # ─── SETTINGS WINDOW (FIXED LAYOUT) ─────────────────────────────────────
    def open_settings(self):
        if self.settings_window is not None:
            self.settings_window.lift()
            return
        
        self.settings_window = ctk.CTkToplevel(self)
        self.settings_window.title("Settings")
        self.settings_window.geometry("360x400") # Optimized height
        self.settings_window.configure(fg_color=BG)
        self.settings_window.resizable(False, False)
        
        curr = backend.load_settings() if HAS_BACKEND else {}
        
        # Title
        ctk.CTkLabel(self.settings_window, text="Settings",
                             text_color=WHITE, font=("Inter", 22, "bold")).pack(pady=(15, 5))
        
        # Separator
        ctk.CTkFrame(self.settings_window, height=1, fg_color=GRAY).pack(fill="x", padx=30, pady=5)
        
        # Resolution
        ctk.CTkLabel(self.settings_window, text="Resolution",
                     text_color=WHITE, font=("Inter", 14)).pack(anchor="w", padx=40, pady=(5, 0))
        
        self.v_res = tk.StringVar(value=curr.get("resolution", "256x256"))
        ctk.CTkOptionMenu(self.settings_window, variable=self.v_res,
                          values=["256x256", "512x512", "1024x1024", "1920x1080"],
                          fg_color=GRAY, button_color=BLUE, button_hover_color=CYAN,
                          text_color=WHITE, dropdown_fg_color=GRAY, dropdown_text_color=WHITE).pack(padx=40, pady=(2, 10), fill="x")
        
        # FPS
        ctk.CTkLabel(self.settings_window, text="FPS",
                     text_color=WHITE, font=("Inter", 14)).pack(anchor="w", padx=40, pady=(5, 0))
        
        self.v_fps = tk.StringVar(value=str(curr.get("fps", 24)))
        ctk.CTkOptionMenu(self.settings_window, variable=self.v_fps,
                          values=["15", "24", "30", "60"],
                          fg_color=GRAY, button_color=BLUE, button_hover_color=CYAN,
                          text_color=WHITE, dropdown_fg_color=GRAY, dropdown_text_color=WHITE).pack(padx=40, pady=(2, 10), fill="x")
        
        # Separator
        ctk.CTkFrame(self.settings_window, height=1, fg_color=GRAY).pack(fill="x", padx=30, pady=10)
        
        # Steganography
        steg_frame = ctk.CTkFrame(self.settings_window, fg_color=BG)
        steg_frame.pack(fill="x", padx=40, pady=5)
        ctk.CTkLabel(steg_frame, text="Steganography Mode", text_color=WHITE, font=("Inter", 14)).pack(side="left")
        
        self.v_steg = tk.BooleanVar(value=curr.get("steganography", False))
        ctk.CTkSwitch(steg_frame, text="", variable=self.v_steg,
                      progress_color=BLUE, button_color=CYAN, button_hover_color=WHITE, fg_color=GRAY, width=40).pack(side="right")
        
        # Auto-Sort (Tight spacing)
        sort_frame = ctk.CTkFrame(self.settings_window, fg_color=BG)
        sort_frame.pack(fill="x", padx=40, pady=5)
        ctk.CTkLabel(sort_frame, text="Auto-Sort Extracted Files", text_color=WHITE, font=("Inter", 14)).pack(side="left")
        
        self.v_sort = tk.BooleanVar(value=curr.get("auto_sort", False))
        ctk.CTkSwitch(sort_frame, text="", variable=self.v_sort,
                      progress_color=BLUE, button_color=CYAN, button_hover_color=WHITE, fg_color=GRAY, width=40).pack(side="right")
        
        # Save Button
        ctk.CTkButton(self.settings_window, text="Save Settings",
                      fg_color=BLUE, hover_color=CYAN, text_color=WHITE,
                      font=("Inter", 14, "bold"), height=40,
                      command=self.save_settings).pack(side="bottom", pady=25, padx=40, fill="x")
        
        self.settings_window.protocol("WM_DELETE_WINDOW", self.close_settings)

    def save_settings(self):
        if HAS_BACKEND:
            backend.save_settings({
                "resolution": self.v_res.get(),
                "fps": int(self.v_fps.get()),
                "steganography": self.v_steg.get(),
                "auto_sort": self.v_sort.get()
            })
        self.update_cover_btn_visibility()
        self.close_settings()
        self.canvas.itemconfig(self.eta_id, text="Settings Saved")

    def close_settings(self):
        if self.settings_window:
            self.settings_window.destroy()
            self.settings_window = None

    # ─── PROGRESS BAR (CANVAS BASED) ─────────────────────────────────────────
    def set_progress(self, val):
        """Update the custom canvas progress bar"""
        val = max(0.0, min(1.0, val))
        new_x1 = self.PB_INNER_X0 + int(val * self.MAX_PB_W)
        self.canvas.coords(self.fill_bar,
                           self.PB_INNER_X0, self.PB_INNER_Y0,
                           new_x1, self.PB_INNER_Y1)
        self.canvas.itemconfig(self.pct_id, text=f"{int(val * 100)}%")

    # ─── THREADED RUNNERS (REAL FUNCTIONALITY) ───────────────────────────────
    def run_encode(self):
        if self.is_running: return
        self.start_thread(backend.encode if HAS_BACKEND else lambda: time.sleep(2), "encoding...")

    def run_decode(self):
        if self.is_running: return
        vid = filedialog.askopenfilename(
            title="Select encoded video to extract",
            filetypes=[("Video Files", "*.avi *.mp4 *.mkv")]
        )
        if not vid: return
        
        func = (lambda: backend.extract(Path(vid))) if HAS_BACKEND else (lambda: time.sleep(2))
        self.start_thread(func, "extracting...")

    def start_thread(self, func, status_msg):
        self.is_running = True
        self.canvas.itemconfig(self.eta_id, text=f"est time: {status_msg}")
        self.set_progress(0)
        
        def work():
            start = time.time()
            # Fake progress purely for visual feedback (since backend blocks)
            for i in range(1, 95):
                if not self.is_running: break
                time.sleep(0.02)
                self.set_progress(i / 100)
            
            try:
                func()
                elapsed = int(time.time() - start)
                self.after(0, lambda: self.set_progress(1.0))
                self.after(0, lambda: self.canvas.itemconfig(self.eta_id, text=f"done in {elapsed}s"))
            except Exception as e:
                print(f"[Error] {e}")
                self.after(0, lambda: self.canvas.itemconfig(self.eta_id, text="error"))
            finally:
                self.is_running = False
        
        threading.Thread(target=work, daemon=True).start()

# ─── LAUNCH ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = BitStreamApp()
    app.mainloop()