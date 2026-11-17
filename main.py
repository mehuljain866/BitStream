"""BitStream desktop interface."""
import math
import os
import queue
import sys
import threading
import time
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk

try:
    import index as backend
    HAS_BACKEND = True
except ImportError as exc:
    backend = None
    HAS_BACKEND = False
    BACKEND_IMPORT_ERROR = exc

ctk.set_appearance_mode("dark")
BG, CYAN, BLUE, WHITE, DIM, GRAY = "#000000", "#6FFFE9", "#3A86FF", "#EAEAEA", "#666666", "#333333"


class BitStreamApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BitStream")
        self.geometry("480x600")
        self.resizable(False, False)
        self.configure(fg_color=BG)
        self.is_running = False
        self.settings_window = None
        self.events = queue.Queue()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.setup_canvas()
        self.setup_widgets()
        self.after(80, self.poll_events)
        if not HAS_BACKEND:
            self.set_status(f"Backend unavailable: {BACKEND_IMPORT_ERROR}")

    def setup_canvas(self):
        self.canvas = tk.Canvas(self, width=480, height=600, bg=BG, highlightthickness=0, bd=0)
        self.canvas.place(x=0, y=0)
        cx, cy, radius = 240, 230, 118
        self.canvas.create_arc(cx-radius, cy-radius, cx+radius, cy+radius,
                               start=10, extent=160, outline=BLUE, width=2, style="arc")
        self.canvas.create_arc(cx-radius, cy-radius, cx+radius, cy+radius,
                               start=190, extent=160, outline=BLUE, width=2, style="arc")
        self.lbl_files = self.canvas.create_text(cx-radius-14, cy, text="Files", fill=CYAN,
                                                  anchor="e", font=("Inter", 26, "bold"), tags="files_tag")
        self.lbl_video = self.canvas.create_text(cx+radius+14, cy, text="Video", fill=CYAN,
                                                  anchor="w", font=("Inter", 26, "bold"), tags="video_tag")
        self.gear_cx, self.gear_cy, self.gear_r = 30, 30, 12
        self.canvas.create_oval(10, 10, 50, 50, fill=BG, outline="", tags="gear_btn")
        self.draw_gear_icon(DIM)
        self.eta_id = self.canvas.create_text(460, 422, text="Ready", fill=WHITE,
                                               anchor="e", font=("Inter", 11))
        self.canvas.create_rectangle(60, 440, 420, 470, outline=CYAN, width=2, fill=BG)
        self.pb_x, self.pb_y, self.pb_w = 63, 443, 354
        self.fill_bar = self.canvas.create_rectangle(self.pb_x, self.pb_y, self.pb_x,
                                                       467, fill=BLUE, outline="")
        self.pct_id = self.canvas.create_text(240, 488, text="0%", fill=BLUE,
                                               anchor="n", font=("Inter", 13, "bold"))
        self.canvas.tag_bind("files_tag", "<Button-1>", lambda _e: self.action_files())
        self.canvas.tag_bind("files_tag", "<Enter>", lambda _e: self.canvas.itemconfig(self.lbl_files, fill=WHITE))
        self.canvas.tag_bind("files_tag", "<Leave>", lambda _e: self.canvas.itemconfig(self.lbl_files, fill=CYAN))
        self.canvas.tag_bind("video_tag", "<Button-1>", lambda _e: self.action_video())
        self.canvas.tag_bind("gear_btn", "<Button-1>", lambda _e: self.open_settings())
        self.canvas.tag_bind("gear_icon", "<Button-1>", lambda _e: self.open_settings())

    def draw_gear_icon(self, color):
        x, y, r = self.gear_cx, self.gear_cy, self.gear_r
        self.canvas.delete("gear_icon")
        self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=color, width=2, fill=BG, tags="gear_icon")
        self.canvas.create_oval(x-4, y-4, x+4, y+4, outline=color, width=1, fill=BG, tags="gear_icon")
        for angle in range(0, 360, 60):
            a = math.radians(angle)
            self.canvas.create_line(x+(r-2)*math.cos(a), y+(r-2)*math.sin(a),
                                    x+(r+4)*math.cos(a), y+(r+4)*math.sin(a),
                                    fill=color, width=3, tags="gear_icon")

    def setup_widgets(self):
        self.btn_enc = ctk.CTkButton(self, text="convert", command=self.run_encode,
                                     width=104, height=28, fg_color=BG, border_width=2,
                                     border_color=WHITE, text_color=WHITE, hover_color=GRAY)
        self.btn_enc.place(x=188, y=84)
        self.btn_dec = ctk.CTkButton(self, text="convert", command=self.run_decode,
                                     width=104, height=28, fg_color=BG, border_width=2,
                                     border_color=WHITE, text_color=WHITE, hover_color=GRAY)
        self.btn_dec.place(x=188, y=358)
        self.btn_cover = ctk.CTkButton(self, text="Upload Cover Video",
                                       command=lambda: self.do_upload(backend.upload_cover_video),
                                       width=160, height=30, fg_color=BG, border_width=2,
                                       border_color=CYAN, text_color=CYAN, hover_color=GRAY)
        self.update_cover_btn_visibility()

    def set_status(self, message):
        self.canvas.itemconfig(self.eta_id, text=str(message)[:70])

    def set_progress(self, value):
        value = max(0.0, min(1.0, float(value)))
        self.canvas.coords(self.fill_bar, self.pb_x, self.pb_y,
                           self.pb_x + int(value * self.pb_w), 467)
        self.canvas.itemconfig(self.pct_id, text=f"{int(value * 100)}%")

    def update_cover_btn_visibility(self):
        if HAS_BACKEND and backend.is_steg_enabled():
            self.btn_cover.place(x=160, y=525)
        else:
            self.btn_cover.place_forget()

    def action_files(self):
        if not HAS_BACKEND:
            return self.backend_error()
        menu = tk.Menu(self, tearoff=0, bg="#222", fg="white",
                       activebackground=CYAN, activeforeground="black")
        menu.add_command(label="Upload Files", command=lambda: self.do_upload(backend.upload_files))
        menu.add_command(label="Upload Folder", command=lambda: self.do_upload(backend.upload_folder))
        if backend.is_steg_enabled():
            menu.add_command(label="Upload Cover Video", command=lambda: self.do_upload(backend.upload_cover_video))
        try:
            menu.tk_popup(self.winfo_pointerx(), self.winfo_pointery())
        finally:
            menu.grab_release()

    def do_upload(self, func):
        try:
            if func():
                self.set_status("Input loaded")
        except Exception as exc:
            messagebox.showerror("Upload failed", str(exc), parent=self)

    def action_video(self):
        path = backend.OUTPUT_VIDEO if HAS_BACKEND else Path("./output")
        path.mkdir(parents=True, exist_ok=True)
        try:
            if sys.platform == "win32":
                os.startfile(str(path))
            elif sys.platform == "darwin":
                os.spawnlp(os.P_NOWAIT, "open", "open", str(path))
            else:
                os.spawnlp(os.P_NOWAIT, "xdg-open", "xdg-open", str(path))
        except OSError as exc:
            messagebox.showerror("Cannot open folder", str(exc), parent=self)

    def open_settings(self):
        if not HAS_BACKEND:
            return self.backend_error()
        if self.settings_window is not None and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return
        window = self.settings_window = ctk.CTkToplevel(self)
        window.title("Settings")
        window.geometry("360x400")
        window.configure(fg_color=BG)
        window.resizable(False, False)
        current = backend.load_settings()
        ctk.CTkLabel(window, text="Settings", text_color=WHITE,
                     font=("Inter", 22, "bold")).pack(pady=(15, 5))
        ctk.CTkFrame(window, height=1, fg_color=GRAY).pack(fill="x", padx=30, pady=5)
        ctk.CTkLabel(window, text="Resolution", text_color=WHITE).pack(anchor="w", padx=40)
        self.v_res = tk.StringVar(value=current["resolution"])
        ctk.CTkOptionMenu(window, variable=self.v_res,
                          values=["256x256", "512x512", "1024x1024", "1920x1080"]).pack(fill="x", padx=40, pady=5)
        ctk.CTkLabel(window, text="FPS", text_color=WHITE).pack(anchor="w", padx=40)
        self.v_fps = tk.StringVar(value=str(current["fps"]))
        ctk.CTkOptionMenu(window, variable=self.v_fps, values=["15", "24", "30", "60"]).pack(fill="x", padx=40, pady=5)
        self.v_steg = tk.BooleanVar(value=current["steganography"])
        ctk.CTkSwitch(window, text="Steganography Mode", variable=self.v_steg).pack(anchor="w", padx=40, pady=8)
        self.v_sort = tk.BooleanVar(value=current["auto_sort"])
        ctk.CTkSwitch(window, text="Auto-Sort Extracted Files", variable=self.v_sort).pack(anchor="w", padx=40, pady=8)
        ctk.CTkButton(window, text="Save Settings", command=self.save_settings).pack(side="bottom", fill="x", padx=40, pady=25)
        window.protocol("WM_DELETE_WINDOW", self.close_settings)

    def save_settings(self):
        try:
            backend.save_settings({
                "resolution": self.v_res.get(), "fps": int(self.v_fps.get()),
                "steganography": bool(self.v_steg.get()), "auto_sort": bool(self.v_sort.get())
            })
            self.update_cover_btn_visibility()
            self.close_settings()
            self.set_status("Settings saved")
        except Exception as exc:
            messagebox.showerror("Settings error", str(exc), parent=self)

    def close_settings(self):
        if self.settings_window is not None:
            self.settings_window.destroy()
            self.settings_window = None

    def backend_error(self):
        messagebox.showerror("Backend unavailable",
                             f"BitStream's backend could not be loaded.\n{BACKEND_IMPORT_ERROR}", parent=self)

    def run_encode(self):
        if not HAS_BACKEND:
            return self.backend_error()
        if self.is_running:
            return
        self._start_job(lambda callback: backend.encode(callback), "Encoding")

    def run_decode(self):
        if not HAS_BACKEND:
            return self.backend_error()
        if self.is_running:
            return
        selected = filedialog.askopenfilename(
            title="Select BitStream video",
            filetypes=[("Video Files", "*.avi *.mkv *.mp4"), ("All files", "*.*")]
        )
        if selected:
            self._start_job(lambda callback: backend.extract(Path(selected), callback), "Extracting")

    def _start_job(self, job, label):
        self.is_running = True
        self.btn_enc.configure(state="disabled")
        self.btn_dec.configure(state="disabled")
        self.set_progress(0)
        self.set_status(label + "...")
        def report(value, message):
            self.events.put(("progress", value, message))
        def worker():
            try:
                result = job(report)
                self.events.put(("success", result))
            except Exception as exc:
                self.events.put(("error", str(exc)))
        threading.Thread(target=worker, daemon=True).start()

    def poll_events(self):
        try:
            while True:
                event = self.events.get_nowait()
                if event[0] == "progress":
                    self.set_progress(event[1])
                    self.set_status(event[2])
                elif event[0] == "success":
                    self.is_running = False
                    self.btn_enc.configure(state="normal")
                    self.btn_dec.configure(state="normal")
                    self.set_progress(1)
                    self.set_status("Completed successfully")
                    messagebox.showinfo("BitStream", f"Operation completed:\n{event[1]}", parent=self)
                elif event[0] == "error":
                    self.is_running = False
                    self.btn_enc.configure(state="normal")
                    self.btn_dec.configure(state="normal")
                    self.set_status("Operation failed")
                    messagebox.showerror("BitStream operation failed", event[1], parent=self)
        except queue.Empty:
            pass
        if self.winfo_exists():
            self.after(80, self.poll_events)

    def on_close(self):
        if self.is_running and not messagebox.askyesno(
            "Operation running", "An operation is still running. Close the application anyway?"
        ):
            return
        self.destroy()


if __name__ == "__main__":
    app = BitStreamApp()
    app.mainloop()
