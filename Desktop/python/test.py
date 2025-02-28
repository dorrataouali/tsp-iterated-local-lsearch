import tkinter as tk
import tkinter.ttk as ttk
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =====================================================
# CLASSES ET FONCTIONS POUR LA VISUALISATION DES TRIS
# =====================================================

class SortingVisualizer:
    """
    Classe permettant d'afficher la partie théorique et pratique (animation) d'un algorithme de tri,
    et d'afficher les métriques (temps, nombre de comparaisons et d'échanges) obtenues lors du tri.
    """
    def __init__(self, master, algorithm_name, sort_func, theory_text):
        self.master = master
        self.algorithm_name = algorithm_name
        self.sort_func = sort_func
        self.theory_text = theory_text
        
        self.frame = tk.Frame(master, bg="#f0f0f0")
        self.frame.pack(fill="both", expand=True)
        
        self.top_frame = tk.Frame(self.frame, bg="#f0f0f0")
        self.top_frame.pack(side=tk.TOP, fill="x")
        
        self.theory_label = tk.Label(self.top_frame, text=self.theory_text, justify=tk.LEFT, wraplength=500, bg="#f0f0f0")
        self.theory_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.style = ttk.Style()
        self.style.configure("Rounded.TButton",
                             font=("Arial", 10, "bold"),
                             foreground="#003366",
                             background="#f0f0f0",  
                             borderwidth=2,
                             relief="flat",
                             padding=10)
        self.style.map("Rounded.TButton", background=[("active", "#f0f0f0")])
        
        self.control_frame = tk.Frame(self.top_frame, bg="#f0f0f0")
        self.control_frame.pack(side=tk.RIGHT, padx=10)
        
        self.generate_button = ttk.Button(self.control_frame, text="Générer un tableau", command=self.generate_array, style="Rounded.TButton")
        self.generate_button.pack(pady=5)
        
        self.run_button = ttk.Button(self.control_frame, text="Lancer le tri", command=self.run_sort, style="Rounded.TButton")
        self.run_button.pack(pady=5)
        
        self.canvas = tk.Canvas(self.frame, width=800, height=400, bg="white", highlightbackground="#707070")
        self.canvas.pack(padx=10, pady=10)
        
        self.metrics_label = tk.Label(self.frame, text="", font=("Arial", 10), bg="#f0f0f0")
        self.metrics_label.pack(pady=5)
        
        self.array = []
        self.delay = 50  # délai en millisecondes pour l'animation
        
        self.generate_array()
    
    def generate_array(self):
        """Génère un tableau aléatoire et l'affiche."""
        self.array = [random.randint(10, 300) for _ in range(50)]
        self.metrics_label.config(text="")  # Réinitialise les métriques
        self.draw_array()
    
    def draw_array(self, highlight_indices=None, swap_indices=None, sorted_index=None, benchmark_value=None):

        self.canvas.delete("all")
        c_width = 800
        c_height = 400
        n = len(self.array)
        bar_width = c_width / n

        for i, val in enumerate(self.array):
            x0 = i * bar_width
            x1 = (i + 1) * bar_width
            y1 = c_height
            if benchmark_value is not None:
                adjusted_val = min(val, benchmark_value)
                y0 = c_height - (benchmark_value - adjusted_val)
            else:
                y0 = c_height - val

            color = "#E0E0E0"       # Couleur par défaut des barres
            border_color = "#004D99"  # Bordure par défaut
            
            if highlight_indices and i in highlight_indices:
                color = "#CA6C0F"   # Orange foncé pour comparaison
                border_color = "#732E00"
            if swap_indices and i in swap_indices:
                color = "red"       # Rouge pour échange
            if sorted_index is not None and i <= sorted_index:
                color = "#004D99"   # Bleu foncé pour éléments triés
                border_color = "#ffffff"
            
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=border_color, width=2)
        self.master.update_idletasks()
    
    def run_sort(self):
        """Mesure le temps d'exécution, lance le tri et affiche les métriques (temps, comparaisons et échanges)."""
        self.run_button.config(state="disabled")
        self.generate_button.config(state="disabled")
        start_time = time.time()
        counters = self.sort_func(self.array, self.draw_array, self.delay)
        elapsed_time = time.time() - start_time
        self.metrics_label.config(text=f"Temps consommé : {elapsed_time:.6f} sec | Comparaisons : {counters.get('comparisons', 0)} | Échanges : {counters.get('swaps', 0)}")
        self.run_button.config(state="normal")
        self.generate_button.config(state="normal")

# ------------------------------
# Fonctions de tri avec comptage
# ------------------------------

def selection_sort(arr, draw_callback, delay, counters=None):
    if counters is None:
        counters = {"comparisons": 0, "swaps": 0}
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            counters["comparisons"] += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
            draw_callback(highlight_indices=[i, j, min_idx], sorted_index=i-1)
            time.sleep(delay / 1000.0)
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            counters["swaps"] += 1
            draw_callback(highlight_indices=[i, min_idx], sorted_index=i-1)
            time.sleep(delay / 1000.0)
        draw_callback(sorted_index=i)
    draw_callback(sorted_index=n-1)
    return counters

def insertion_sort(arr, draw_callback, delay, counters=None):
    if counters is None:
        counters = {"comparisons": 0, "swaps": 0}
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            counters["comparisons"] += 1
            arr[j + 1] = arr[j]
            counters["swaps"] += 1
            draw_callback(highlight_indices=[j, j+1], sorted_index=i-1)
            time.sleep(delay / 1000.0)
            j -= 1
        if j >= 0:
            counters["comparisons"] += 1
        arr[j + 1] = key
        draw_callback(highlight_indices=[j+1], sorted_index=i)
        time.sleep(delay / 1000.0)
    return counters

def bubble_sort(arr, draw_callback, delay, counters=None):
    if counters is None:
        counters = {"comparisons": 0, "swaps": 0}
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            counters["comparisons"] += 1
            draw_callback(highlight_indices=[j, j+1])
            time.sleep(delay / 1000.0)
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                counters["swaps"] += 1
                draw_callback(swap_indices=[j, j+1])
                time.sleep(delay / 1000.0)
        draw_callback(sorted_index=n-i-1)
    return counters

def quick_sort(arr, draw_callback, delay, low=0, high=None, counters=None):
    if counters is None:
        counters = {"comparisons": 0, "swaps": 0}
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi = partition(arr, draw_callback, delay, low, high, counters)
        quick_sort(arr, draw_callback, delay, low, pi - 1, counters)
        quick_sort(arr, draw_callback, delay, pi + 1, high, counters)
    return counters

def partition(arr, draw_callback, delay, low, high, counters):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        counters["comparisons"] += 1
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            counters["swaps"] += 1
            draw_callback(highlight_indices=[i, j])
            time.sleep(delay / 1000.0)
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    counters["swaps"] += 1
    draw_callback(highlight_indices=[i+1, high])
    time.sleep(delay / 1000.0)
    return i + 1

def merge_sort(arr, draw_callback, delay, left=0, right=None, counters=None):
    if counters is None:
        counters = {"comparisons": 0, "swaps": 0}
    if right is None:
        right = len(arr) - 1
    if left < right:
        mid = (left + right) // 2
        merge_sort(arr, draw_callback, delay, left, mid, counters)
        merge_sort(arr, draw_callback, delay, mid + 1, right, counters)
        merge(arr, draw_callback, delay, left, mid, right, counters)
    return counters

def merge(arr, draw_callback, delay, left, mid, right, counters):
    L = arr[left:mid+1]
    R = arr[mid+1:right+1]
    i = j = 0
    k = left
    while i < len(L) and j < len(R):
        counters["comparisons"] += 1
        if L[i] < R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        counters["swaps"] += 1  # Considère l'affectation comme un échange
        draw_callback(highlight_indices=[k])
        time.sleep(delay / 1000.0)
        k += 1
    while i < len(L):
        arr[k] = L[i]
        i += 1
        counters["swaps"] += 1
        draw_callback(highlight_indices=[k])
        time.sleep(delay / 1000.0)
        k += 1
    while j < len(R):
        arr[k] = R[j]
        j += 1
        counters["swaps"] += 1
        draw_callback(highlight_indices=[k])
        time.sleep(delay / 1000.0)
        k += 1

def tim_sort(arr, draw_callback, delay, counters=None):
    if counters is None:
        counters = {"comparisons": 0, "swaps": 0}
    arr.sort()  # Utilise la méthode de tri intégrée (Tim Sort)
    draw_callback(sorted_index=len(arr)-1)
    time.sleep(delay / 1000.0)
    return counters

theory_texts = {
    "Selection Sort": "Selection Sort :\n\nPrincipe : Parcourir le tableau pour trouver l'élément minimum et le placer en première position, puis répéter pour le reste du tableau.\nComplexité théorique : O(n²).",
    "Insertion Sort": "Insertion Sort :\n\nPrincipe : Construire progressivement une sous-liste triée en insérant chaque nouvel élément à sa position correcte.\nComplexité théorique : O(n²) dans le pire cas.",
    "Bubble Sort": "Bubble Sort :\n\nPrincipe : Comparer et échanger les éléments adjacents jusqu'à ce que le tableau soit trié.\nComplexité théorique : O(n²).",
    "Quick Sort": "Quick Sort :\n\nPrincipe : Diviser le tableau autour d'un pivot et trier récursivement les sous-tableaux.\nComplexité théorique : En moyenne O(n log n), mais O(n²) dans le pire cas.",
    "Merge Sort": "Merge Sort :\n\nPrincipe : Diviser le tableau en deux, trier récursivement les deux moitiés et fusionner les deux sous-tableaux triés.\nComplexité théorique : O(n log n).",
    "Tim Sort": "Tim Sort :\n\nPrincipe : Algorithme de tri hybride utilisé par Python, basé sur l'insertion et la fusion.\nComplexité théorique : O(n log n) dans le pire cas."
}

def benchmark_algorithms():
    """
    Effectue un benchmark sur plusieurs tailles de tableaux et retourne une figure matplotlib.
    Affiche également, sous le graphique, les métriques (comparaisons et échanges) pour la taille maximale.
    """
    sizes = [100, 500, 1000, 2000, 5000, 10000]
    algorithms = {
        "Selection Sort": lambda arr, draw, delay: selection_sort(arr, lambda *args, **kwargs: None, 0),
        "Insertion Sort": lambda arr, draw, delay: insertion_sort(arr, lambda *args, **kwargs: None, 0),
        "Bubble Sort": lambda arr, draw, delay: bubble_sort(arr, lambda *args, **kwargs: None, 0),
        "Quick Sort": lambda arr, draw, delay: quick_sort(arr, lambda *args, **kwargs: None, 0),
        "Merge Sort": lambda arr, draw, delay: merge_sort(arr, lambda *args, **kwargs: None, 0),
        "Tim Sort": lambda arr, draw, delay: tim_sort(arr, lambda *args, **kwargs: None, 0)
    }
    results = {name: [] for name in algorithms}
    counters_results = {}
    for size in sizes:
        for name, func in algorithms.items():
            arr = [random.randint(1, size) for _ in range(size)]
            start = time.time()
            counters = func(arr, lambda *args, **kwargs: None, 0)
            end = time.time()
            results[name].append(end - start)
            if size == sizes[-1]:
                counters_results[name] = counters
    fig, ax = plt.subplots(figsize=(8, 6))
    for name, times in results.items():
        ax.plot(sizes, times, marker='o', label=name)
    ax.set_xlabel("Taille du tableau")
    ax.set_ylabel("Temps d'exécution (s)")
    ax.set_title("Comparaison des Algorithmes de Tri")
    ax.legend()
    text_info = f"Métriques pour taille = {sizes[-1]}:\n"
    for name, counters in counters_results.items():
        text_info += f"{name} : Comparaisons = {counters.get('comparisons', 0)}, Échanges = {counters.get('swaps', 0)}\n"
    fig.text(0.5, 0.01, text_info, ha="center", fontsize=10, bbox=dict(facecolor="white", alpha=0.5))
    return fig

class ComparisonFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.info_label = tk.Label(self, text="Benchmark des algorithmes sur différentes tailles de tableaux", font=("Arial", 12))
        self.info_label.pack(pady=10)
        self.plot_button = ttk.Button(self, text="Lancer le benchmark", command=self.run_benchmark, style="Rounded.TButton")
        self.plot_button.pack(pady=5)
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill="both", expand=True)
        self.canvas_widget = None
        
    def run_benchmark(self):
        fig = benchmark_algorithms()
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()
        self.canvas_widget = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(fill="both", expand=True)

class QuizFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.questions = [
            {
                "question": "Quel est l'algorithme le plus efficace en moyenne ?",
                "options": ["Selection Sort", "Insertion Sort", "Quick Sort", "Merge Sort", "Tim Sort"],
                "answer": "Quick Sort"
            },
            {
                "question": "Quel algorithme utilise le principe de diviser pour régner ?",
                "options": ["Insertion Sort", "Quick Sort", "Selection Sort", "Bubble Sort"],
                "answer": "Quick Sort"
            }
        ]
        self.current_question = 0
        self.score = 0
        
        self.question_label = tk.Label(self, text="", font=("Arial", 12))
        self.question_label.pack(pady=10)
        self.options_var = tk.StringVar()
        self.options = []
        for i in range(4):
            rb = tk.Radiobutton(self, text="", variable=self.options_var, value="", font=("Arial", 10))
            rb.pack(anchor="w")
            self.options.append(rb)
        self.submit_button = tk.Button(self, text="Valider", command=self.check_answer)
        self.submit_button.pack(pady=5)
        self.feedback_label = tk.Label(self, text="", font=("Arial", 10))
        self.feedback_label.pack(pady=5)
        self.next_button = tk.Button(self, text="Question Suivante", command=self.next_question, state="disabled")
        self.next_button.pack(pady=5)
        
        self.load_question()
        
    def load_question(self):
        q = self.questions[self.current_question]
        self.question_label.config(text=q["question"])
        self.options_var.set(None)
        for i, option in enumerate(q["options"]):
            self.options[i].config(text=option, value=option)
        self.feedback_label.config(text="")
        self.next_button.config(state="disabled")
        self.submit_button.config(state="normal")
        
    def check_answer(self):
        selected = self.options_var.get()
        correct = self.questions[self.current_question]["answer"]
        if selected == correct:
            self.feedback_label.config(text="Bonne réponse !")
            self.score += 1
        else:
            self.feedback_label.config(text=f"Mauvaise réponse. La bonne réponse était : {correct}")
        self.submit_button.config(state="disabled")
        self.next_button.config(state="normal")
        
    def next_question(self):
        self.current_question += 1
        if self.current_question >= len(self.questions):
            self.question_label.config(text=f"Quiz terminé ! Votre score : {self.score}/{len(self.questions)}")
            for rb in self.options:
                rb.pack_forget()
            self.submit_button.pack_forget()
            self.next_button.pack_forget()
        else:
            self.load_question()

class SortingApp:

    def __init__(self, master):
        self.master = master
        master.title("Visualisation des Algorithmes de Tri")
        master.geometry("900x2000")
        
        self.sidebar = tk.Frame(master, width=200, bg="#242526")
        self.sidebar.pack(side=tk.LEFT, fill="y")
        
        self.sidebar_style = ttk.Style()
        self.sidebar_style.theme_use("clam")
        self.sidebar_style.configure("Sidebar.TButton",
                                     background="#242526",
                                     foreground="white",
                                     font=("Arial", 10, "bold"),
                                     borderwidth=0,
                                     padding=10)
        self.sidebar_style.map("Sidebar.TButton",
                               background=[("active", "#3a3b3c")])
        self.sidebar_style.configure("SidebarSelected.TButton",
                                     background="#3a3b3c",
                                     foreground="white",
                                     font=("Arial", 10, "bold"),
                                     borderwidth=0,
                                     padding=10)
        self.content_frame = tk.Frame(master)
        self.content_frame.pack(side=tk.RIGHT, fill="both", expand=True)
        
        self.buttons = {}
        sections = ["Selection Sort", "Insertion Sort", "Bubble Sort", "Quick Sort", "Merge Sort", "Tim Sort", "Comparison"]
        for sec in sections:
            btn = ttk.Button(self.sidebar, text=sec, command=lambda s=sec: self.show_section(s), style="Sidebar.TButton")
            btn.pack(fill="x", padx=10, pady=5)
            self.buttons[sec] = btn
        
        self.section_frame = None
        self.show_section("Selection Sort")
        
    def show_section(self, section):
        for sec, btn in self.buttons.items():
            btn.configure(style="Sidebar.TButton")
        self.buttons[section].configure(style="SidebarSelected.TButton")
        
        if self.section_frame:
            self.section_frame.destroy()
        if section in ["Selection Sort", "Insertion Sort", "Bubble Sort", "Quick Sort", "Merge Sort", "Tim Sort"]:
            if section == "Selection Sort":
                vis = SortingVisualizer(self.content_frame, section, selection_sort, theory_texts[section])
            elif section == "Insertion Sort":
                vis = SortingVisualizer(self.content_frame, section, insertion_sort, theory_texts[section])
            elif section == "Bubble Sort":
                vis = SortingVisualizer(self.content_frame, section, bubble_sort, theory_texts[section])
            elif section == "Quick Sort":
                vis = SortingVisualizer(self.content_frame, section, quick_sort, theory_texts[section])
            elif section == "Merge Sort":
                vis = SortingVisualizer(self.content_frame, section, merge_sort, theory_texts[section])
            elif section == "Tim Sort":
                vis = SortingVisualizer(self.content_frame, section, tim_sort, theory_texts[section])
            self.section_frame = vis.frame
        elif section == "Comparison":
            self.section_frame = ComparisonFrame(self.content_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingApp(root)
    root.mainloop()
