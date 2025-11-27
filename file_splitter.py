#!/usr/bin/env python3
"""
Text File Splitter GUI - Modern Golden Theme Edition
Efficiently split large text files (100M+ lines) into smaller chunks
"""

import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import queue
import time


class GoldenTheme:
    """Golden color palette for modern UI"""
    # Primary colors
    GOLD_PRIMARY = "#D4AF37"      # Classic gold
    GOLD_LIGHT = "#F4E4BA"        # Light gold
    GOLD_DARK = "#B8960C"         # Dark gold
    GOLD_ACCENT = "#FFD700"       # Bright gold
    
    # Background colors
    BG_DARK = "#1A1A2E"           # Dark navy background
    BG_MEDIUM = "#16213E"         # Medium dark background
    BG_LIGHT = "#0F3460"          # Lighter accent background
    BG_CARD = "#1F2940"           # Card background
    
    # Text colors
    TEXT_PRIMARY = "#FFFFFF"       # White text
    TEXT_SECONDARY = "#B8B8B8"     # Gray text
    TEXT_GOLD = "#D4AF37"          # Gold text
    
    # Status colors
    SUCCESS = "#4CAF50"            # Green
    ERROR = "#F44336"              # Red
    WARNING = "#FF9800"            # Orange
    
    # Button states
    BTN_HOVER = "#E5C158"          # Lighter gold for hover
    BTN_PRESSED = "#A38829"        # Darker gold for pressed


class ModernButton(tk.Canvas):
    """Custom modern button with golden styling"""
    
    def __init__(self, parent, text, command=None, width=200, height=45, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        bg=GoldenTheme.BG_DARK, highlightthickness=0, **kwargs)
        
        self.command = command
        self.text = text
        self.width = width
        self.height = height
        self.enabled = True
        
        self._draw_button(GoldenTheme. GOLD_PRIMARY)
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)
    
    def _draw_button(self, color):
        self.delete("all")
        # Draw rounded rectangle
        self._round_rectangle(5, 5, self.width-5, self.height-5, 
                             radius=10, fill=color, outline="")
        # Draw text
        self. create_text(self.width//2, self.height//2, text=self.text,
                        fill=GoldenTheme.BG_DARK, font=("Segoe UI", 11, "bold"))
    
    def _round_rectangle(self, x1, y1, x2, y2, radius=10, **kwargs):
        points = [
            x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
            x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
            x1, y2, x1, y2-radius, x1, y1+radius, x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _on_enter(self, event):
        if self.enabled:
            self._draw_button(GoldenTheme.BTN_HOVER)
            self.config(cursor="hand2")
    
    def _on_leave(self, event):
        if self.enabled:
            self._draw_button(GoldenTheme. GOLD_PRIMARY)
    
    def _on_click(self, event):
        if self.enabled:
            self._draw_button(GoldenTheme.BTN_PRESSED)
    
    def _on_release(self, event):
        if self.enabled:
            self._draw_button(GoldenTheme.BTN_HOVER)
            if self.command:
                self.command()
    
    def set_enabled(self, enabled):
        self.enabled = enabled
        if enabled:
            self._draw_button(GoldenTheme. GOLD_PRIMARY)
        else:
            self._draw_button(GoldenTheme.TEXT_SECONDARY)


class ProgressCard(tk.Frame):
    """Modern progress display card"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=GoldenTheme.BG_CARD, **kwargs)
        
        # Progress bar container
        self.progress_frame = tk. Frame(self, bg=GoldenTheme.BG_CARD)
        self. progress_frame.pack(fill="x", padx=20, pady=(15, 5))
        
        # Progress bar background
        self.progress_bg = tk. Canvas(self.progress_frame, height=8, 
                                     bg=GoldenTheme.BG_DARK, highlightthickness=0)
        self.progress_bg.pack(fill="x")
        
        # Status labels
        self.status_frame = tk.Frame(self, bg=GoldenTheme.BG_CARD)
        self.status_frame.pack(fill="x", padx=20, pady=(5, 15))
        
        self.status_label = tk.Label(self.status_frame, text="Ready to split", 
                                     bg=GoldenTheme.BG_CARD, fg=GoldenTheme.TEXT_SECONDARY,
                                     font=("Segoe UI", 10))
        self.status_label.pack(side="left")
        
        self.percent_label = tk. Label(self.status_frame, text="0%", 
                                      bg=GoldenTheme.BG_CARD, fg=GoldenTheme. GOLD_PRIMARY,
                                      font=("Segoe UI", 10, "bold"))
        self.percent_label.pack(side="right")
        
        # Stats frame
        self. stats_frame = tk.Frame(self, bg=GoldenTheme.BG_CARD)
        self.stats_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self. lines_label = tk. Label(self.stats_frame, text="Lines: 0", 
                                    bg=GoldenTheme.BG_CARD, fg=GoldenTheme. TEXT_SECONDARY,
                                    font=("Segoe UI", 9))
        self. lines_label.pack(side="left")
        
        self.files_label = tk. Label(self.stats_frame, text="Files: 0", 
                                    bg=GoldenTheme.BG_CARD, fg=GoldenTheme.TEXT_SECONDARY,
                                    font=("Segoe UI", 9))
        self.files_label. pack(side="right")
    
    def update_progress(self, percent, status="", lines=0, files=0):
        # Update progress bar
        self.progress_bg.delete("progress")
        width = self.progress_bg.winfo_width()
        if width > 1:
            fill_width = int(width * percent / 100)
            self.progress_bg.create_rectangle(0, 0, fill_width, 8, 
                                              fill=GoldenTheme.GOLD_PRIMARY, 
                                              outline="", tags="progress")
        
        # Update labels
        self.percent_label.config(text=f"{percent:. 1f}%")
        if status:
            self.status_label. config(text=status)
        self.lines_label. config(text=f"Lines: {lines:,}")
        self.files_label. config(text=f"Files: {files}")
    
    def reset(self):
        self.progress_bg. delete("progress")
        self.percent_label.config(text="0%")
        self.status_label.config(text="Ready to split")
        self. lines_label.config(text="Lines: 0")
        self.files_label.config(text="Files: 0")


class TextSplitterGUI:
    """Main GUI Application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self. root.title("✨ Text File Splitter - Golden Edition")
        self.root.geometry("700x650")
        self.root.minsize(600, 600)
        self.root.configure(bg=GoldenTheme.BG_DARK)
        
        # Set icon if available
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.split_method = tk.StringVar(value="lines")
        self. lines_per_file = tk.StringVar(value="1000000")
        self.size_mb = tk.StringVar(value="100")
        
        # Queue for thread communication
        self.progress_queue = queue. Queue()
        self.is_processing = False
        self.cancel_requested = False
        
        self._create_ui()
        self._start_queue_handler()
    
    def _create_ui(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg=GoldenTheme.BG_DARK)
        main_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Header
        self._create_header(main_container)
        
        # File selection card
        self._create_file_card(main_container)
        
        # Split options card
        self._create_options_card(main_container)
        
        # Progress card
        self._create_progress_card(main_container)
        
        # Action buttons
        self._create_action_buttons(main_container)
        
        # Footer
        self._create_footer(main_container)
    
    def _create_header(self, parent):
        header_frame = tk.Frame(parent, bg=GoldenTheme.BG_DARK)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Title with gold styling
        title_label = tk.Label(header_frame, text="✨ Text File Splitter", 
                              bg=GoldenTheme.BG_DARK, fg=GoldenTheme. GOLD_PRIMARY,
                              font=("Segoe UI", 24, "bold"))
        title_label.pack()
        
        subtitle_label = tk. Label(header_frame, 
                                  text="Handle 100M+ lines with ease • Golden Edition", 
                                  bg=GoldenTheme.BG_DARK, fg=GoldenTheme.TEXT_SECONDARY,
                                  font=("Segoe UI", 10))
        subtitle_label.pack(pady=(5, 0))
    
    def _create_file_card(self, parent):
        # Card frame
        card = tk.Frame(parent, bg=GoldenTheme.BG_CARD)
        card.pack(fill="x", pady=(0, 15))
        
        # Card header
        header = tk.Label(card, text="📁 File Selection", 
                         bg=GoldenTheme.BG_CARD, fg=GoldenTheme. GOLD_PRIMARY,
                         font=("Segoe UI", 12, "bold"))
        header.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Input file row
        input_frame = tk.Frame(card, bg=GoldenTheme. BG_CARD)
        input_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        tk.Label(input_frame, text="Input File:", bg=GoldenTheme.BG_CARD, 
                fg=GoldenTheme. TEXT_PRIMARY, font=("Segoe UI", 10)).pack(anchor="w")
        
        input_row = tk.Frame(input_frame, bg=GoldenTheme.BG_CARD)
        input_row.pack(fill="x", pady=(5, 0))
        
        self. input_entry = tk.Entry(input_row, textvariable=self.input_file,
                                    bg=GoldenTheme.BG_MEDIUM, fg=GoldenTheme.TEXT_PRIMARY,
                                    insertbackground=GoldenTheme. GOLD_PRIMARY,
                                    font=("Segoe UI", 10), relief="flat")
        self.input_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        
        browse_btn = tk. Button(input_row, text="Browse", command=self._browse_input,
                              bg=GoldenTheme. GOLD_PRIMARY, fg=GoldenTheme.BG_DARK,
                              font=("Segoe UI", 9, "bold"), relief="flat",
                              activebackground=GoldenTheme.BTN_HOVER, cursor="hand2")
        browse_btn. pack(side="right", ipadx=15, ipady=5)
        
        # Output directory row
        output_frame = tk.Frame(card, bg=GoldenTheme.BG_CARD)
        output_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        tk.Label(output_frame, text="Output Directory (optional):", bg=GoldenTheme.BG_CARD, 
                fg=GoldenTheme.TEXT_PRIMARY, font=("Segoe UI", 10)).pack(anchor="w")
        
        output_row = tk.Frame(output_frame, bg=GoldenTheme.BG_CARD)
        output_row.pack(fill="x", pady=(5, 0))
        
        self.output_entry = tk.Entry(output_row, textvariable=self.output_dir,
                                     bg=GoldenTheme.BG_MEDIUM, fg=GoldenTheme.TEXT_PRIMARY,
                                     insertbackground=GoldenTheme. GOLD_PRIMARY,
                                     font=("Segoe UI", 10), relief="flat")
        self.output_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        
        browse_out_btn = tk. Button(output_row, text="Browse", command=self._browse_output,
                                   bg=GoldenTheme. GOLD_PRIMARY, fg=GoldenTheme.BG_DARK,
                                   font=("Segoe UI", 9, "bold"), relief="flat",
                                   activebackground=GoldenTheme. BTN_HOVER, cursor="hand2")
        browse_out_btn.pack(side="right", ipadx=15, ipady=5)
        
        # File info label
        self.file_info_label = tk.Label(card, text="", bg=GoldenTheme.BG_CARD, 
                                        fg=GoldenTheme.TEXT_SECONDARY,
                                        font=("Segoe UI", 9))
        self. file_info_label.pack(anchor="w", padx=20, pady=(0, 15))
    
    def _create_options_card(self, parent):
        # Card frame
        card = tk. Frame(parent, bg=GoldenTheme.BG_CARD)
        card.pack(fill="x", pady=(0, 15))
        
        # Card header
        header = tk.Label(card, text="⚙️ Split Options", 
                         bg=GoldenTheme.BG_CARD, fg=GoldenTheme.GOLD_PRIMARY,
                         font=("Segoe UI", 12, "bold"))
        header.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Split method selection
        method_frame = tk. Frame(card, bg=GoldenTheme.BG_CARD)
        method_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Custom styled radio buttons
        style = ttk.Style()
        style.configure("Gold.TRadiobutton", 
                       background=GoldenTheme.BG_CARD,
                       foreground=GoldenTheme.TEXT_PRIMARY,
                       font=("Segoe UI", 10))
        
        lines_radio = tk.Radiobutton(method_frame, text="Split by Lines", 
                                     variable=self.split_method, value="lines",
                                     bg=GoldenTheme. BG_CARD, fg=GoldenTheme.TEXT_PRIMARY,
                                     selectcolor=GoldenTheme.BG_MEDIUM,
                                     activebackground=GoldenTheme.BG_CARD,
                                     activeforeground=GoldenTheme. GOLD_PRIMARY,
                                     font=("Segoe UI", 10), cursor="hand2",
                                     command=self._update_options_visibility)
        lines_radio.pack(side="left", padx=(0, 30))
        
        size_radio = tk. Radiobutton(method_frame, text="Split by Size", 
                                    variable=self.split_method, value="size",
                                    bg=GoldenTheme.BG_CARD, fg=GoldenTheme.TEXT_PRIMARY,
                                    selectcolor=GoldenTheme. BG_MEDIUM,
                                    activebackground=GoldenTheme. BG_CARD,
                                    activeforeground=GoldenTheme. GOLD_PRIMARY,
                                    font=("Segoe UI", 10), cursor="hand2",
                                    command=self._update_options_visibility)
        size_radio. pack(side="left")
        
        # Options container
        options_container = tk.Frame(card, bg=GoldenTheme. BG_CARD)
        options_container.pack(fill="x", padx=20, pady=(10, 15))
        
        # Lines option
        self.lines_frame = tk.Frame(options_container, bg=GoldenTheme.BG_CARD)
        self.lines_frame.pack(fill="x")
        
        tk.Label(self. lines_frame, text="Lines per file:", 
                bg=GoldenTheme. BG_CARD, fg=GoldenTheme.TEXT_PRIMARY,
                font=("Segoe UI", 10)).pack(side="left")
        
        self.lines_entry = tk.Entry(self.lines_frame, textvariable=self.lines_per_file,
                                    bg=GoldenTheme. BG_MEDIUM, fg=GoldenTheme.TEXT_PRIMARY,
                                    insertbackground=GoldenTheme.GOLD_PRIMARY,
                                    font=("Segoe UI", 10), relief="flat", width=15)
        self. lines_entry.pack(side="left", padx=(10, 10), ipady=5)
        
        tk.Label(self. lines_frame, text="(e.g., 1000000 = 1 million)", 
                bg=GoldenTheme.BG_CARD, fg=GoldenTheme.TEXT_SECONDARY,
                font=("Segoe UI", 9)).pack(side="left")
        
        # Size option
        self.size_frame = tk.Frame(options_container, bg=GoldenTheme.BG_CARD)
        
        tk.Label(self.size_frame, text="Size per file (MB):", 
                bg=GoldenTheme.BG_CARD, fg=GoldenTheme.TEXT_PRIMARY,
                font=("Segoe UI", 10)). pack(side="left")
        
        self.size_entry = tk.Entry(self.size_frame, textvariable=self.size_mb,
                                   bg=GoldenTheme.BG_MEDIUM, fg=GoldenTheme.TEXT_PRIMARY,
                                   insertbackground=GoldenTheme.GOLD_PRIMARY,
                                   font=("Segoe UI", 10), relief="flat", width=15)
        self.size_entry.pack(side="left", padx=(10, 10), ipady=5)
        
        tk.Label(self. size_frame, text="(e.g., 100 = 100 MB)", 
                bg=GoldenTheme.BG_CARD, fg=GoldenTheme. TEXT_SECONDARY,
                font=("Segoe UI", 9)).pack(side="left")
        
        # Presets
        presets_frame = tk.Frame(card, bg=GoldenTheme.BG_CARD)
        presets_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        tk.Label(presets_frame, text="Quick presets:", 
                bg=GoldenTheme.BG_CARD, fg=GoldenTheme.TEXT_SECONDARY,
                font=("Segoe UI", 9)).pack(side="left", padx=(0, 10))
        
        presets = [("1M lines", "1000000"), ("5M lines", "5000000"), 
                   ("10M lines", "10000000"), ("50M lines", "50000000")]
        
        for text, value in presets:
            btn = tk.Button(presets_frame, text=text, 
                           command=lambda v=value: self._set_lines_preset(v),
                           bg=GoldenTheme.BG_LIGHT, fg=GoldenTheme. GOLD_PRIMARY,
                           font=("Segoe UI", 8), relief="flat", cursor="hand2",
                           activebackground=GoldenTheme. GOLD_DARK)
            btn.pack(side="left", padx=3, ipadx=8, ipady=2)
    
    def _create_progress_card(self, parent):
        # Card frame
        card = tk. Frame(parent, bg=GoldenTheme.BG_CARD)
        card.pack(fill="x", pady=(0, 15))
        
        # Card header
        header = tk.Label(card, text="📊 Progress", 
                         bg=GoldenTheme.BG_CARD, fg=GoldenTheme. GOLD_PRIMARY,
                         font=("Segoe UI", 12, "bold"))
        header.pack(anchor="w", padx=20, pady=(15, 5))
        
        # Progress component
        self.progress_card = ProgressCard(card)
        self.progress_card.pack(fill="x")
    
    def _create_action_buttons(self, parent):
        buttons_frame = tk. Frame(parent, bg=GoldenTheme.BG_DARK)
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        # Center the buttons
        center_frame = tk. Frame(buttons_frame, bg=GoldenTheme.BG_DARK)
        center_frame.pack()
        
        self.split_button = ModernButton(center_frame, "🚀 Start Splitting", 
                                         command=self._start_split, width=180)
        self.split_button.pack(side="left", padx=10)
        
        self.cancel_button = ModernButton(center_frame, "❌ Cancel", 
                                          command=self._cancel_split, width=120)
        self. cancel_button.pack(side="left", padx=10)
        self.cancel_button. set_enabled(False)
    
    def _create_footer(self, parent):
        footer_frame = tk. Frame(parent, bg=GoldenTheme.BG_DARK)
        footer_frame.pack(fill="x", pady=(20, 0))
        
        footer_text = tk. Label(footer_frame, 
                              text="💡 Tip: For 100M+ lines, use streaming mode for memory efficiency",
                              bg=GoldenTheme.BG_DARK, fg=GoldenTheme.TEXT_SECONDARY,
                              font=("Segoe UI", 9))
        footer_text.pack()
    
    def _update_options_visibility(self):
        if self.split_method.get() == "lines":
            self.size_frame.pack_forget()
            self.lines_frame.pack(fill="x")
        else:
            self.lines_frame.pack_forget()
            self.size_frame. pack(fill="x")
    
    def _set_lines_preset(self, value):
        self. split_method.set("lines")
        self.lines_per_file.set(value)
        self._update_options_visibility()
    
    def _browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self. input_file.set(filename)
            self._update_file_info(filename)
    
    def _browse_output(self):
        dirname = filedialog. askdirectory(title="Select Output Directory")
        if dirname:
            self. output_dir.set(dirname)
    
    def _update_file_info(self, filepath):
        try:
            path = Path(filepath)
            size_bytes = path.stat(). st_size
            size_mb = size_bytes / (1024 * 1024)
            size_gb = size_bytes / (1024 * 1024 * 1024)
            
            if size_gb >= 1:
                size_str = f"{size_gb:.2f} GB"
            else:
                size_str = f"{size_mb:.2f} MB"
            
            # Estimate line count (rough estimate: ~50 bytes per line average)
            est_lines = size_bytes // 50
            if est_lines >= 1_000_000_000:
                lines_str = f"~{est_lines/1_000_000_000:.1f}B lines"
            elif est_lines >= 1_000_000:
                lines_str = f"~{est_lines/1_000_000:.1f}M lines"
            else:
                lines_str = f"~{est_lines:,} lines"
            
            self. file_info_label.config(
                text=f"📄 Size: {size_str} | Estimated: {lines_str}",
                fg=GoldenTheme. GOLD_LIGHT
            )
        except Exception as e:
            self.file_info_label. config(text=f"⚠️ Error reading file info", 
                                        fg=GoldenTheme.ERROR)
    
    def _validate_inputs(self):
        if not self.input_file.get():
            messagebox. showerror("Error", "Please select an input file.")
            return False
        
        if not Path(self.input_file.get()).exists():
            messagebox.showerror("Error", "Input file does not exist.")
            return False
        
        try:
            if self.split_method.get() == "lines":
                lines = int(self. lines_per_file.get(). replace(',', ''). replace('_', ''))
                if lines <= 0:
                    raise ValueError()
            else:
                size = int(self. size_mb.get())
                if size <= 0:
                    raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number.")
            return False
        
        return True
    
    def _start_split(self):
        if not self._validate_inputs():
            return
        
        self.is_processing = True
        self.cancel_requested = False
        self.split_button.set_enabled(False)
        self.cancel_button.set_enabled(True)
        self.progress_card.reset()
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self._split_worker, daemon=True)
        thread.start()
    
    def _cancel_split(self):
        self.cancel_requested = True
        self. progress_queue.put(("status", "Cancelling... "))
    
    def _split_worker(self):
        try:
            input_file = self.input_file. get()
            output_dir = self. output_dir.get() or None
            
            input_path = Path(input_file)
            file_size = input_path. stat().st_size
            
            # Set output directory
            if output_dir is None:
                output_dir = input_path.parent / f"{input_path.stem}_split"
            else:
                output_dir = Path(output_dir)
            
            output_dir.mkdir(exist_ok=True)
            
            file_ext = input_path. suffix
            base_name = input_path.stem
            
            if self.split_method. get() == "lines":
                lines_per_file = int(self.lines_per_file.get().replace(',', '').replace('_', ''))
                self._split_by_lines(input_file, lines_per_file, output_dir, 
                                     base_name, file_ext, file_size)
            else:
                size_mb = int(self.size_mb. get())
                self._split_by_size(input_file, size_mb, output_dir,
                                    base_name, file_ext, file_size)
            
            if not self.cancel_requested:
                self.progress_queue. put(("complete", "Split completed successfully!"))
            else:
                self.progress_queue. put(("cancelled", "Operation cancelled. "))
        
        except Exception as e:
            self. progress_queue.put(("error", str(e)))
    
    def _split_by_lines(self, input_file, lines_per_file, output_dir, 
                        base_name, file_ext, file_size):
        file_number = 1
        line_count = 0
        total_lines = 0
        bytes_read = 0
        output_file = None
        
        # Use buffered reading for better performance with huge files
        buffer_size = 64 * 1024 * 1024  # 64MB buffer
        
        try:
            with open(input_file, 'r', encoding='utf-8', errors='ignore', 
                      buffering=buffer_size) as infile:
                for line in infile:
                    if self.cancel_requested:
                        break
                    
                    bytes_read += len(line.encode('utf-8'))
                    
                    # Open new output file if needed
                    if line_count == 0:
                        if output_file:
                            output_file.close()
                        
                        output_filename = output_dir / f"{base_name}_part_{file_number:04d}{file_ext}"
                        output_file = open(output_filename, 'w', encoding='utf-8', 
                                          buffering=buffer_size)
                        self.progress_queue. put(("status", f"Creating: {output_filename. name}"))
                    
                    output_file.write(line)
                    line_count += 1
                    total_lines += 1
                    
                    # Update progress every 100k lines for responsiveness
                    if total_lines % 100000 == 0:
                        percent = min(99. 9, (bytes_read / file_size) * 100)
                        self.progress_queue. put(("progress", percent, total_lines, file_number))
                    
                    if line_count >= lines_per_file:
                        line_count = 0
                        file_number += 1
            
            if output_file:
                output_file.close()
            
            self.progress_queue.put(("progress", 100, total_lines, file_number))
        
        except Exception as e:
            if output_file:
                output_file. close()
            raise e
    
    def _split_by_size(self, input_file, size_mb, output_dir,
                       base_name, file_ext, file_size):
        max_size_bytes = size_mb * 1024 * 1024
        file_number = 1
        current_size = 0
        total_lines = 0
        bytes_read = 0
        output_file = None
        
        buffer_size = 64 * 1024 * 1024  # 64MB buffer
        
        try:
            with open(input_file, 'r', encoding='utf-8', errors='ignore',
                      buffering=buffer_size) as infile:
                for line in infile:
                    if self.cancel_requested:
                        break
                    
                    line_bytes = len(line.encode('utf-8'))
                    bytes_read += line_bytes
                    
                    # Open new file if needed
                    if current_size == 0 or current_size + line_bytes > max_size_bytes:
                        if output_file:
                            output_file.close()
                        
                        output_filename = output_dir / f"{base_name}_part_{file_number:04d}{file_ext}"
                        output_file = open(output_filename, 'w', encoding='utf-8',
                                          buffering=buffer_size)
                        self.progress_queue.put(("status", f"Creating: {output_filename.name}"))
                        current_size = 0
                        file_number += 1
                    
                    output_file. write(line)
                    current_size += line_bytes
                    total_lines += 1
                    
                    # Update progress every 100k lines
                    if total_lines % 100000 == 0:
                        percent = min(99.9, (bytes_read / file_size) * 100)
                        self.progress_queue.put(("progress", percent, total_lines, file_number - 1))
            
            if output_file:
                output_file.close()
            
            self.progress_queue. put(("progress", 100, total_lines, file_number - 1))
        
        except Exception as e:
            if output_file:
                output_file. close()
            raise e
    
    def _start_queue_handler(self):
        self._process_queue()
    
    def _process_queue(self):
        try:
            while True:
                msg = self.progress_queue.get_nowait()
                
                if msg[0] == "progress":
                    percent, lines, files = msg[1], msg[2], msg[3]
                    self.progress_card.update_progress(percent, "", lines, files)
                
                elif msg[0] == "status":
                    self. progress_card.update_progress(
                        float(self.progress_card. percent_label.cget("text"). rstrip("%")),
                        msg[1],
                        int(self.progress_card.lines_label.cget("text").split(": ")[1]. replace(",", "")),
                        int(self.progress_card.files_label.cget("text").split(": ")[1])
                    )
                
                elif msg[0] == "complete":
                    self._finish_processing(True, msg[1])
                
                elif msg[0] == "cancelled":
                    self._finish_processing(False, msg[1])
                
                elif msg[0] == "error":
                    self._finish_processing(False, f"Error: {msg[1]}")
        
        except queue. Empty:
            pass
        
        # Schedule next check
        self.root.after(50, self._process_queue)
    
    def _finish_processing(self, success, message):
        self. is_processing = False
        self.split_button.set_enabled(True)
        self.cancel_button.set_enabled(False)
        
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showwarning("Stopped", message)
    
    def run(self):
        self.root.mainloop()


def main():
    app = TextSplitterGUI()
    app.run()


if __name__ == "__main__":
    main()
