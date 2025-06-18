import tkinter as tk
from tkinter import messagebox, scrolledtext

# Grammar
rules = """
    K -> S P | X1 Ket | X1 Pel | X1 X2
    X1 -> S P
    X2 -> Pel Ket
    S -> NP Det | NP Noun | NP AdjP
    P -> NP NP
    Ket -> Prep NP | Prep NumP
    Pel -> Det AdjP | AdjP | Det VP 
    NP -> Noun | NP Noun | Pronoun | NP Pronoun | NP Ket | NP Det | NP AdjP 
    AdjP -> Adj | AdjP Adv | Adv AdjP | AdjP NP
    VP -> Verb | VP Verb | VP NP | Adv VP 
    PP -> Prep NP | Prep PP | Prep AdjP
    NumP -> Num | NumP NP | NP NumP
    Noun -> timpal | nasi | goreng | ajengan | bapak | bupati | gianyar | semeton | adin | dasar | tahun | taun | pragina | desan | nyoman | budi | sopir | motor | trunyan | juru | parkir | sepedane | wayan | darta | bapane | carik | pak | polisi | lalu-lintas | denpasar | jero | balian | sakit | basang | putu | gede | umah | memen | desane | baju | baru | lemarine | tukang | pns | luh | sari | serombotan | anake | bapakne | pianakne | diri | tingkat | 2020 | desa | ketua | koperasi | pasar | badung | mahasiswa | baru | i | putu | gede | guru | olahraga | sekolah | ibu | puspa | dosen | matematika | kampus 
    Pronoun -> tiang | tiange | titiang | ipun 
    Adj -> lanang | wanen | jegeg | demenin | luh | becik | seleg | sesai | luung | sakti | jegeg-jegeg
    Adv -> paling | pisan | rauh | semeng | sekancan | pinaka 
    Verb -> ngajar | anggone | ngatehin | ngatur | ngubadin | meli 
    Num -> telung | limang | dasa | besik
    Prep -> di | ring | saking | uli | ka | sampun | tuni | dados 
    Det -> punika | puniki | sane | ento | tiange
"""

# Mengubah grammar string menjadi dictionary
def parse_grammar(grammar_string):
    grammar_dict = {}
    for line in grammar_string.split('\n'):
        if not line.strip():
            continue
        head, productions = line.split(' -> ')
        productions = productions.split(' | ')
        grammar_dict[head.strip()] = [production.split() for production in productions]
    return grammar_dict

# Menerapkan aturan unary
def apply_unary_rules(cell, rules):
    to_process = set(cell)
    processed = set()

    while to_process:
        current = to_process.pop()
        processed.add(current)

        for lhs, rhs in rules.items():
            for production in rhs:
                if len(production) == 1 and production[0] == current:
                    if lhs not in processed:
                        cell.add(lhs)
                        to_process.add(lhs)

    return cell

# Algoritma CYK
def cykParse(w, R):
    n = len(w)

    T = [[set() for _ in range(n)] for _ in range(n)]

    for j in range(n):
        for lhs, rule in R.items():
            for rhs in rule:
                if len(rhs) == 1 and rhs[0] == w[j]:
                    T[j][j].add(lhs)

        T[j][j] = apply_unary_rules(T[j][j], R)

    for span in range(2, n + 1):
        for i in range(n - span + 1):
            j = i + span - 1
            for k in range(i, j):
                for lhs, rule in R.items():
                    for rhs in rule:
                        if len(rhs) == 2 and rhs[0] in T[i][k] and rhs[1] in T[k + 1][j]:
                            T[i][j].add(lhs)
                T[i][j] = apply_unary_rules(T[i][j], R)

    return T

# Menampilkan tabel CYK
def displayCYKTable(w, R):
    table = cykParse(w, R)
    
    result = "\n\n\nTabel CYK:\n"
    n = len(w)

    # Header Kolom
    result += "     "
    for j in range(n):
        result += f"{j:^18} "  # Lebar kolom
    result += "\n" + "-" * (n * 19)  

    # Baris Tabel
    for i in range(n):
        result += f"\n\n{i:^5} |"  
        for j in range(n):
            if j >= i:
                cell_content = ", ".join(sorted(table[i][j]))
                result += f" {cell_content:<18} "  # Lebar kolom
            else:
                result += f" {'-':<18} "  

    result += "\n" + "-" * (n * 19)

    # Hasil analisis kalimat
    if "K" in table[0][n - 1]:
        result += "\n\nHasil : Kalimat yang dimasukkan VALID."
    else:
        result += "\n\nHasil : Kalimat yang dimasukkan TIDAK VALID."
    
    return result

# Fungsi untuk menjalankan parsing
def run_parser():
    input_string = input_entry.get().strip()
    if not input_string:
        messagebox.showerror("ERROR!", "Kalimat tidak boleh kosong!")
        return

    words = input_string.split()
    result = displayCYKTable(words, R)  

    output_text.delete(1.0, tk.END)  
    output_text.insert(tk.END, result)  


R = parse_grammar(rules)

# GUI Utama
root = tk.Tk()
root.title("Periksa Kalimat Bahasa Bali")
root.geometry("800x600")  
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, padx=10, pady=10, bg="#ffffff")
frame.pack(pady=20, fill=tk.BOTH, expand=True)

input_frame = tk.Frame(frame, bg="#ffffff")
input_frame.pack(pady=10, fill=tk.X)

input_label = tk.Label(input_frame, text="Masukkan kalimat:", bg="#ffffff", font=("Arial", 12))
input_label.pack(side=tk.LEFT, padx=5)

input_entry = tk.Entry(input_frame, width=50, font=("Arial", 12), borderwidth=2, relief="groove")
input_entry.pack(side=tk.LEFT, padx=5)

parse_button = tk.Button(input_frame, text="Periksa", command=run_parser, bg="#4CAF50", fg="white", font=("Arial", 12), relief="raised")
parse_button.pack(side=tk.LEFT, padx=5)

output_frame = tk.Frame(frame, bg="#ffffff")
output_frame.pack(pady=10, fill=tk.BOTH, expand=True)

output_text = scrolledtext.ScrolledText(output_frame, height=20, width=100, font=("Arial", 12), wrap=tk.WORD, bg="#f9f9f9", borderwidth=2, relief="groove")
output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

root.mainloop()