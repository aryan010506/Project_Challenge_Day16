import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import tkinter as tk
from tkinter import filedialog
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -------------------- Functions --------------------
def load_data():
    file_path = filedialog.askopenfilename(
        title="Select Netflix Dataset CSV",
        filetypes=[("CSV files", "*.csv")]
    )
    if file_path:
        df = pd.read_csv(file_path)
        df.dropna(subset=['rating', 'listed_in', 'release_year', 'description'], inplace=True)
        show_analysis(df)

def show_analysis(df):
    # Clear existing tabs content
    for tab in [tab1, tab2, tab3, tab4]:
        for widget in tab.winfo_children():
            widget.destroy()

    # ---------------- Tab 1 – Genres ----------------
    plt1 = plt.figure(figsize=(6, 4))
    genre_counts = df['listed_in'].str.split(',').explode().str.strip().value_counts().head(10)
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='viridis')
    plt.title('Top 10 Genres on Netflix')
    plt.xlabel('Count')
    plt.tight_layout()
    canvas1 = FigureCanvasTkAgg(plt1, master=tab1)
    canvas1.draw()
    canvas1.get_tk_widget().pack(padx=10, pady=10)

    # ---------------- Tab 2 – Ratings ----------------
    plt2 = plt.figure(figsize=(6, 4))
    rating_counts = df['rating'].value_counts().head(10)
    sns.barplot(x=rating_counts.values, y=rating_counts.index, palette='coolwarm')
    plt.title('Top Ratings')
    plt.xlabel('Count')
    plt.tight_layout()
    canvas2 = FigureCanvasTkAgg(plt2, master=tab2)
    canvas2.draw()
    canvas2.get_tk_widget().pack(padx=10, pady=10)

    # ---------------- Tab 3 – Trends ----------------
    plt3 = plt.figure(figsize=(6, 4))
    year_counts = df['release_year'].value_counts().sort_index()
    sns.lineplot(x=year_counts.index, y=year_counts.values, marker='o', color='green')
    plt.title('Content Release Trend Over Years')
    plt.xlabel('Year')
    plt.ylabel('Number of Titles')
    plt.tight_layout()
    canvas3 = FigureCanvasTkAgg(plt3, master=tab3)
    canvas3.draw()
    canvas3.get_tk_widget().pack(padx=10, pady=10)

    # ---------------- Tab 4 – WordCloud ----------------
    text = " ".join(desc for desc in df['description'])
    wc = WordCloud(width=800, height=400, background_color='black', colormap='plasma').generate(text)
    plt4 = plt.figure(figsize=(6, 4))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title('WordCloud of Descriptions')
    plt.tight_layout()
    canvas4 = FigureCanvasTkAgg(plt4, master=tab4)
    canvas4.draw()
    canvas4.get_tk_widget().pack(padx=10, pady=10)

# -------------------- GUI --------------------
style = Style(theme="cyborg")  # themes: darkly, flatly, cyborg, solar, morph
root = style.master
root.title("🎬 Netflix Data Analysis Dashboard")
root.geometry("1200x700")

# Title
title_label = ttk.Label(root, text="📊 Netflix Data Analysis Dashboard", font=("Helvetica", 20, "bold"), bootstyle=SUCCESS)
title_label.pack(pady=10)

# Load Button
btn_load = ttk.Button(root, text="Load Netflix CSV", bootstyle=PRIMARY, command=load_data)
btn_load.pack(pady=10)

# Notebook (Tabbed Interface)
notebook = ttk.Notebook(root, bootstyle=INFO)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)

notebook.add(tab1, text="📚 Genres")
notebook.add(tab2, text="🎯 Ratings")
notebook.add(tab3, text="📈 Year Trends")
notebook.add(tab4, text="☁ WordCloud")

root.mainloop()
