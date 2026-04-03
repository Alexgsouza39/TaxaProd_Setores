"""MIT License (c) 2025 Alex Guariroba de Souza — see LICENSE"""

"""
MIT License (see LICENSE file)
Copyright (c) 2025 Alex Guariroba de Souza

This file is part of the Relatório de Produção app.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from datetime import datetime
import pandas as pd
import re
from decimal import Decimal, ROUND_HALF_UP
import sys

def resource_path(relative_path: str) -> Path:
    if getattr(sys, 'frozen', False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).parent
    return base / relative_path


def formatar_tempo(tempo_dec):
    if tempo_dec <= 0:
        return "00:00:00"
    tempo_dec = abs(float(tempo_dec))
    horas = int(tempo_dec)
    minutos_totais = (tempo_dec - horas) * 60
    minutos = int(minutos_totais)
    segundos = int(round((minutos_totais - minutos) * 60))
    # Tratar segundo = 60 (overflow)
    if segundos == 60:
        segundos = 0
        minutos += 1
    if minutos == 60:
        minutos = 0
        horas += 1
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


def parse_time_to_decimal(time_str: str) -> float:
    """Converte string 'HH:MM' ou 'HH:MM:SS' em horas decimais (float).
    Se receber um número decimal (ex: '4.5'), tenta converter diretamente.
    Retorna 0.0 para entradas vazias ou inválidas.
    Usa Decimal para máxima precisão interna.
    """
    if time_str is None:
        return 0.0
    s = str(time_str).strip()
    if not s:
        return 0.0
    # aceita formatos com dois pontos
    if ':' in s:
        parts = s.split(':')
        try:
            h = Decimal(parts[0]) if parts[0] != '' else Decimal('0')
            m = Decimal(parts[1]) if len(parts) > 1 and parts[1] != '' else Decimal('0')
            sec = Decimal(parts[2]) if len(parts) > 2 and parts[2] != '' else Decimal('0')
            resultado = h + m/Decimal('60') + sec/Decimal('3600')
            return float(resultado)
        except Exception:
            return 0.0
    # tenta interpretar como decimal com ponto ou vírgula
    try:
        s2 = s.replace(',', '.')
        return float(Decimal(s2))
    except Exception:
        return 0.0


def limpar_string_para_arquivo(texto):
    texto_limpo = re.sub(r'[^a-zA-Z0-9_.-]', '_', str(texto).strip())
    texto_limpo = re.sub(r'_+', '_', texto_limpo)
    return texto_limpo.strip('_')


MAPEAMENTO_CT = {
    1: "TEX24", 2: "TEX25", 3: "TEX26", 4: "TEX25", 5: "TEX28",
    6: "TEX21", 7: "TEX20", 8: "TEX19", 9: "TEX04",
    10: "TEX05-350kg",
    11: "TEX06-600kg"
}

MAPEAMENTO_CORDAS = {
    1: 1, 2: 2, 3: 2, 4: 4, 5: 4,
    6: 4, 7: 4, 8: 6, 9: 6, 10: 2, 11: 4
}

PESO_FIXO_M10 = 350.0
PESO_FIXO_M11 = 600.0


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Visual moderno: tema base, fontes e espaçamentos
        style = ttk.Style(self)
        try:
            style.theme_use('clam')
        except Exception:
            pass
        default_font = ("Segoe UI", 10, 'italic', 'normal')
        style.configure('.', font=default_font)
        style.configure('Treeview', rowheight=20, font=default_font)
        style.configure('Treeview.Heading', font=("Segoe UI", 11, 'bold'))
        style.configure('Accent.TButton', font=("Segoe UI", 8, 'normal'), anchor='center', padding=6)
        style.configure('Card.TLabelframe', font=("Segoe UI", 8, 'normal'), background="#484646", anchor='center', borderwidth=1, padding=15)
        style.configure('TLabel', font=("Segoe UI", 9, 'normal'), background="#c8c8ef", anchor='center', padding=6)

        self.title("Relatório Taxas de Produção - Tinturaria & Acabamento")
        self.geometry("1050x780")
        self.configure(padx=8, pady=8, bg="#f0f0f0")
        self.export_mode = tk.StringVar(value="all")

        self._build_global_actions()

        # Cria notebook (abas)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Aba 1: Tinturaria
        self.tab_tinturaria = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tinturaria, text="Tinturaria")
        self.tab_tinturaria.grid_rowconfigure(3, weight=1)
        self.tab_tinturaria.grid_columnconfigure(0, weight=1)

        # Aba 2: Acabamento
        self.tab_acabamento = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_acabamento, text="Acabamento")
        self.tab_acabamento.grid_rowconfigure(3, weight=1)
        self.tab_acabamento.grid_columnconfigure(0, weight=1)

        # Controles para Tinturaria (dentro da aba)
        self._build_inputs_tinturaria()
        self._build_machines_frame()
        self._build_actions_tinturaria()
        self._build_treeview_tinturaria()

        # Controles para Acabamento (dentro da aba)
        self._build_inputs_acabamento()
        self._build_treeview_acabamento()
        self._build_actions_acabamento()

    def _build_inputs_tinturaria(self):
        frame = ttk.LabelFrame(self.tab_tinturaria, text="Dados do Produto", style='Card.TLabelframe')
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.tab_tinturaria.grid_columnconfigure(0, weight=1)

        ttk.Label(frame, width=15, text="Artigo:").grid(row=0, column=0, sticky="w")
        self.entry_artigo = ttk.Entry(frame, width=12)
        self.entry_artigo.grid(row=0, column=1, sticky="w", pady=6, padx=4)

        ttk.Label(frame, width=6, text="Cor:").grid(row=0, column=2, sticky="w")
        self.entry_cor = ttk.Entry(frame, width=8)
        self.entry_cor.grid(row=0, column=3, sticky="w", padx=4)

        ttk.Label(frame, width=10, text="Descrição:").grid(row=0, column=4, sticky="w")
        self.entry_desc = ttk.Entry(frame, width=30)
        self.entry_desc.grid(row=0, column=5, sticky="w", padx=4)
        
        ttk.Label(frame, text="Gramatura (g/m):").grid(row=0, column=6, sticky="w", padx=15)
        self.entry_gram = ttk.Entry(frame, width=8)
        self.entry_gram.grid(row=0, column=7, sticky="w")

        ttk.Label(frame, width=15,text="Peça (m):").grid(row=1, column=0, sticky="w", pady=6)
        self.entry_comp = ttk.Entry(frame, width=12)
        self.entry_comp.grid(row=1, column=1, sticky="w", pady=6, padx=4)

        ttk.Label(frame, text="Nº Rolos:").grid(row=1, column=2, sticky="w")
        self.entry_rolos = ttk.Entry(frame, width=8)
        self.entry_rolos.grid(row=1, column=3, sticky="w", padx=6)

        ttk.Label(frame, text="Nº Cordas:").grid(row=1, column=4, sticky="w")
        self.entry_corpos = ttk.Entry(frame, width=8)
        self.entry_corpos.grid(row=1, column=5, sticky="w", padx=6)

    def _build_global_actions(self):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        frame.columnconfigure(3, weight=1)

        ttk.Label(frame, text="Exportar:").grid(row=0, column=0, sticky="w")
        rb_all = ttk.Radiobutton(frame, text="Tudo", variable=self.export_mode, value="all")
        rb_all.grid(row=0, column=1, padx=4)
        rb_acab = ttk.Radiobutton(frame, text="Só Acabamento", variable=self.export_mode, value="acabamento")
        rb_acab.grid(row=0, column=2, padx=4)
        btn_export = ttk.Button(frame, text="Exportar Relatório", command=self.exportar, style='Accent.TButton')
        btn_export.grid(row=0, column=3, padx=4, sticky="e")

    def _build_machines_frame(self):
        frame = ttk.LabelFrame(self.tab_tinturaria, text="Tempos por Máquina (HH:MM ou Decimal)", style='Card.TLabelframe')
        frame.grid(row=1, column=0, sticky="nsew", padx=7, pady=7)
        self.tab_tinturaria.grid_columnconfigure(0, weight=1)

        self.machine_vars = {}
        col = 0
        row = 0
        for i in range(1, 12):
            label = f"{MAPEAMENTO_CT[i]} (M{i:02d}):"
            ttk.Label(frame, text=label).grid(row=row, column=col*2, sticky="w", padx=2, pady=2)
            var = tk.StringVar(value="00:00")
            entry = ttk.Entry(frame, textvariable=var, width=8)
            entry.grid(row=row, column=col*2 + 1, sticky="w", padx=2, pady=2)
            self.machine_vars[i] = var
            col += 1
            if col >= 4:
                col = 0
                row += 1

    def _build_actions_tinturaria(self):
        frame = ttk.Frame(self.tab_tinturaria)
        frame.grid(row=2, column=0, sticky="ew", padx=5, pady=8)

        btn_calc = ttk.Button(frame, text="Calcular Tinturaria", command=self.calcular_tinturaria, style='Accent.TButton')
        btn_calc.grid(row=0, column=0, padx=3)

        btn_clear = ttk.Button(frame, text="Limpar Tinturaria", command=self.limpar_tinturaria, style='Accent.TButton')
        btn_clear.grid(row=0, column=1, padx=3)

    def _build_treeview_tinturaria(self):
        cols = ["Maquina", "Cordas", "Metragem(m)", "Peso(kg)", "Gramatura(g/m)", "Tempo(Dec)", "Tempo(Horas)", "Taxa Prod.", "Unidade"]
        frame = ttk.Frame(self.tab_tinturaria)
        frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        self.tab_tinturaria.grid_rowconfigure(3, weight=1)

        self.tree_tinturaria = ttk.Treeview(frame, columns=cols, show='headings', selectmode='browse')
        for c in cols:
            self.tree_tinturaria.heading(c, text=c)
            self.tree_tinturaria.column(c, width=100, anchor='center')

        # Linhas alternadas
        self.tree_tinturaria.tag_configure('odd', background="#bdd59d")
        self.tree_tinturaria.tag_configure('even', background="#bec0cc")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree_tinturaria.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree_tinturaria.xview)
        self.tree_tinturaria.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree_tinturaria.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def limpar_tinturaria(self):
        for widget in [self.entry_artigo, self.entry_cor, self.entry_desc, self.entry_comp, self.entry_rolos, self.entry_corpos, self.entry_gram]:
            widget.delete(0, tk.END)
        for v in self.machine_vars.values():
            v.set('0')
        for item in self.tree_tinturaria.get_children():
            self.tree_tinturaria.delete(item)

    def calcular_tinturaria(self):
        try:
            artigo = self.entry_artigo.get().strip()
            cor = self.entry_cor.get().strip()
            descricao = self.entry_desc.get().strip()
            comp_rolo = float(self.entry_comp.get())
            num_rolos = int(self.entry_rolos.get())
            num_corpos = int(self.entry_corpos.get())
            gramatura = float(self.entry_gram.get())
        except Exception:
            messagebox.showerror("Erro", "Preencha corretamente os campos numéricos.")
            return

        # Validações adicionais de segurança/saneamento
        if comp_rolo <= 0:
            messagebox.showerror("Erro", "Comprimento do rolo deve ser maior que zero.")
            return
        if num_rolos < 0 or num_corpos < 0:
            messagebox.showerror("Erro", "Nº de rolos/corpos não pode ser negativo.")
            return
        if gramatura <= 0:
            messagebox.showerror("Erro", "Gramatura deve ser maior que zero.")
            return

        tempos = {}
        tempos_hh = {}
        for i, var in self.machine_vars.items():
            raw = var.get().strip()
            tempo_dec = parse_time_to_decimal(raw)
            tempos[i] = tempo_dec
            tempos_hh[i] = formatar_tempo(tempo_dec)

        tabela = []
        for i in range(1, 12):
            tempo_dec = tempos.get(i, 0.0)
            num_cordas = MAPEAMENTO_CORDAS[i]
            
            # Usar Decimal para cálculos de produção com alta precisão
            comp_rolo_dec = Decimal(str(comp_rolo))
            num_rolos_dec = Decimal(str(num_rolos))
            num_corpos_dec = Decimal(str(num_corpos))
            num_cordas_dec = Decimal(str(num_cordas))
            gramatura_dec = Decimal(str(gramatura))
            tempo_dec_decimal = Decimal(str(tempo_dec))
            
            prod_metros_calculada_dec = comp_rolo_dec * num_rolos_dec * num_corpos_dec * num_cordas_dec

            # Tratamento especial para M10 e M11: peso fixo e metragem calculada a partir do peso
            if i == 10:
                peso_kg_dec = Decimal(str(PESO_FIXO_M10))
                prod_metros_reporte_dec = (peso_kg_dec * Decimal('1000')) / gramatura_dec if gramatura_dec > 0 else Decimal('0')
            elif i == 11:
                peso_kg_dec = Decimal(str(PESO_FIXO_M11))
                prod_metros_reporte_dec = (peso_kg_dec * Decimal('1000')) / gramatura_dec if gramatura_dec > 0 else Decimal('0')
            else:
                peso_kg_dec = (prod_metros_calculada_dec * gramatura_dec) / Decimal('1000')
                prod_metros_reporte_dec = prod_metros_calculada_dec

            # Cálculo preciso de taxa de produção
            # Taxa de produção em m/h para todas as máquinas quando houver tempo
            if tempo_dec > 0:
                # usar metragem reportada (para M10/M11 vem do peso fixo)
                taxa_prod_dec = prod_metros_reporte_dec / tempo_dec_decimal
                unidade = "m/h"
            elif peso_kg_dec > 0 and i in [10, 11]:
                 unidade = "kg/h"
            else:
                taxa_prod_dec = Decimal('0')
                unidade = "-"

            tabela.append({
                "ID_TEX": MAPEAMENTO_CT[i],
                "Maquina": f"M{i:02d} - {MAPEAMENTO_CT[i]}",
                "Cordas": num_cordas,
                "Metragem(m)": float(prod_metros_reporte_dec),
                "Peso(kg)": float(peso_kg_dec),
                "Gramatura(g/m)": float(gramatura_dec),
                "Tempo(Dec)": tempo_dec,
                "Tempo(Horas)": tempos_hh.get(i, formatar_tempo(tempo_dec)),
                "Taxa Prod.": round(float(taxa_prod_dec), 2),
                "Unidade": unidade
            })

        # Preenche treeview com maior precisão
            numeric_cols = {"Metragem(m)", "Peso(kg)", "Gramatura(g/m)", "Tempo(Dec)", "Taxa Prod."}
        for item in self.tree_tinturaria.get_children():
            self.tree_tinturaria.delete(item)
        for idx, row in enumerate(tabela):
            values = []
            for c in self.tree_tinturaria['columns']:
                v = row.get(c, "")
                if c in numeric_cols:
                    try:
                        val_float = float(v)
                        # Usar maior precisão para Taxa Prod.
                        if c == "Taxa Prod.":
                            values.append(f"{val_float:.2f}")
                        else:
                            values.append(f"{val_float:.2f}")
                    except Exception:
                        values.append(v)
                else:
                    values.append(v)
            tag = 'even' if idx % 2 == 0 else 'odd'
            self.tree_tinturaria.insert('', tk.END, values=values, tags=(tag,))

        # Guarda último DataFrame para exportação
        self.last_df_tinturaria = pd.DataFrame(tabela)
        self.last_meta_tinturaria = {"artigo": artigo, "cor": cor, "Descrição": descricao}

        messagebox.showinfo("OK", "Cálculo de Tinturaria concluído e tabela exibida.")

    def _build_inputs_acabamento(self):
        frame = ttk.LabelFrame(self.tab_acabamento, text="Dados do Acabamento", style='Card.TLabelframe')
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.tab_acabamento.grid_columnconfigure(0, weight=1)
        for col in range(6):
            frame.columnconfigure(col, weight=1)

        ttk.Label(frame, width=12, text="Artigo:").grid(row=0, column=0, sticky="w")
        self.entry_acab_cod = ttk.Entry(frame, width=12)
        self.entry_acab_cod.grid(row=0, column=1, sticky="ew", pady=6, padx=4)

        ttk.Label(frame, width=8, text="Cor:").grid(row=0, column=2, sticky="w")
        self.entry_acab_cod_cor = ttk.Entry(frame, width=10)
        self.entry_acab_cod_cor.grid(row=0, column=3, sticky="ew", padx=4)

        ttk.Label(frame, width=10, text="Descrição:").grid(row=0, column=4, sticky="w")
        self.entry_acab_desc = ttk.Entry(frame, width=30)
        self.entry_acab_desc.grid(row=0, column=5, sticky="ew", padx=4)

        ttk.Label(frame, text="PS(g/m²):").grid(row=1, column=0, sticky="w", pady=6)
        self.entry_acab_ps = ttk.Entry(frame, width=12)
        self.entry_acab_ps.grid(row=1, column=1, sticky="ew", padx=4)

        ttk.Label(frame, text="PU(g/m²):").grid(row=1, column=2, sticky="w")
        self.entry_acab_pu = ttk.Entry(frame, width=12)
        self.entry_acab_pu.grid(row=1, column=3, sticky="ew", padx=4)

        ttk.Label(frame, text="Largura(m):").grid(row=1, column=4, sticky="w")
        self.entry_acab_larg = ttk.Entry(frame, width=12)
        self.entry_acab_larg.grid(row=1, column=5, sticky="ew", padx=4)

        ttk.Label(frame, text="Metragem(m):").grid(row=2, column=0, sticky="w", pady=6)
        self.entry_acab_metragem = ttk.Entry(frame, width=12)
        self.entry_acab_metragem.grid(row=2, column=1, sticky="ew", padx=4)

        ttk.Label(frame, text="Químico1:").grid(row=2, column=2, sticky="w")
        self.entry_acab_quim1 = ttk.Entry(frame, width=12)
        self.entry_acab_quim1.grid(row=2, column=3, sticky="ew", padx=4)

        ttk.Label(frame, text="Conc.Q1(g/L):").grid(row=2, column=4, sticky="w")
        self.entry_acab_conc1 = ttk.Entry(frame, width=12)
        self.entry_acab_conc1.grid(row=2, column=5, sticky="ew", padx=4)

        ttk.Label(frame, text="Químico2:").grid(row=3, column=0, sticky="w", pady=6)
        self.entry_acab_quim2 = ttk.Entry(frame, width=12)
        self.entry_acab_quim2.grid(row=3, column=1, sticky="ew", padx=4)

        ttk.Label(frame, text="Conc.Q2(g/L):").grid(row=3, column=2, sticky="w")
        self.entry_acab_conc2 = ttk.Entry(frame, width=12)
        self.entry_acab_conc2.grid(row=3, column=3, sticky="ew", padx=4)

        ttk.Label(frame, text="Químico3:").grid(row=3, column=4, sticky="w")
        self.entry_acab_quim3 = ttk.Entry(frame, width=12)
        self.entry_acab_quim3.grid(row=3, column=5, sticky="ew", padx=4)

        ttk.Label(frame, text="Conc.Q3(g/L):").grid(row=4, column=0, sticky="w", pady=6)
        self.entry_acab_conc3 = ttk.Entry(frame, width=12)
        self.entry_acab_conc3.grid(row=4, column=1, sticky="ew", padx=4)

    def _build_treeview_acabamento(self):
        cols = ["PS", "PU", "Pick-up %", "Largura(m)", "Metragem(m)", "Banho(L)", "Arraste ml/m²", "Q1", "Conc.Q1(g/L)", "Cons.Q1(g/m)", "Q2", "Cons.Q2(g/L)", "Cons. Q2(g/m)", "Q3", "Cons.Q3(g/L)", "Cons.Q3(g/m)"]
        frame = ttk.Frame(self.tab_acabamento)
        frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.tab_acabamento.grid_rowconfigure(2, weight=1)

        self.tree_acabamento = ttk.Treeview(frame, columns=cols, show='headings', selectmode='browse')
        for c in cols:
            self.tree_acabamento.heading(c, text=c)
            width = 80 if c in ["Descrição"] else 70
            self.tree_acabamento.column(c, width=width, anchor='center')

        self.tree_acabamento.tag_configure('odd', background="#bdd59d")
        self.tree_acabamento.tag_configure('even', background="#bec0cc")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree_acabamento.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree_acabamento.xview)
        self.tree_acabamento.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree_acabamento.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def _build_actions_acabamento(self):
        frame = ttk.Frame(self.tab_acabamento)
        frame.grid(row=1, column=0, sticky="ew", padx=5, pady=8)

        btn_calc = ttk.Button(frame, text="Calcular Acabamento", command=self.calcular_acabamento, style='Accent.TButton')
        btn_calc.grid(row=0, column=0, padx=3)

        btn_clear = ttk.Button(frame, text="Limpar Acabamento", command=self.limpar_acabamento, style='Accent.TButton')
        btn_clear.grid(row=0, column=1, padx=3)

    def limpar_acabamento(self):
        for widget in [self.entry_acab_cod, self.entry_acab_cod_cor, self.entry_acab_desc, 
                       self.entry_acab_ps, self.entry_acab_pu, self.entry_acab_larg, 
                       self.entry_acab_vel, self.entry_acab_metragem,
                       self.entry_acab_quim1, self.entry_acab_conc1,
                       self.entry_acab_quim2, self.entry_acab_conc2,
                       self.entry_acab_quim3, self.entry_acab_conc3]:
            widget.delete(0, tk.END)
        for item in self.tree_acabamento.get_children():
            self.tree_acabamento.delete(item)

    def calcular_acabamento(self):
        try:
            codigo = self.entry_acab_cod.get().strip()
            cod_cor = self.entry_acab_cod_cor.get().strip()
            descricao = self.entry_acab_desc.get().strip()
            ps = float(self.entry_acab_ps.get())  # Peso seco (g/m²)
            pu = float(self.entry_acab_pu.get())  # Peso úmido (g/m²)
            largura = float(self.entry_acab_larg.get())  # Largura em m
            metragem = float(self.entry_acab_metragem.get())  # Metragem em m
            quim1 = self.entry_acab_quim1.get().strip()
            conc1 = float(self.entry_acab_conc1.get() or 0)
            quim2 = self.entry_acab_quim2.get().strip()
            conc2 = float(self.entry_acab_conc2.get() or 0)
            quim3 = self.entry_acab_quim3.get().strip()
            conc3 = float(self.entry_acab_conc3.get() or 0)
        except Exception:
            messagebox.showerror("Erro", "Preencha corretamente todos os campos numéricos do Acabamento.")
            return

        # Validações
        if ps <= 0:
            messagebox.showerror("Erro", "g/m² Seco deve ser maior que zero.")
            return
        if pu <= 0:
            messagebox.showerror("Erro", "g/m² Úmido deve ser maior que zero.")
            return
        if largura <= 0:
            messagebox.showerror("Erro", "Largura deve ser maior que zero.")
            return
        if metragem <= 0:
            messagebox.showerror("Erro", "Metragem deve ser maior que zero.")
            return

        # Cálculos usando Decimal para precisão
        ps_dec = Decimal(str(ps))
        pu_dec = Decimal(str(pu))
        larg_dec = Decimal(str(largura))
        metragem_dec = Decimal(str(metragem))
        conc1_dec = Decimal(str(conc1))
        conc2_dec = Decimal(str(conc2))
        conc3_dec = Decimal(str(conc3))

        # Pick-up (arraste) = (PU - PS) / PS * 100 (%)
        pickup_pct = ((pu_dec - ps_dec) / ps_dec) * Decimal('100')
        arraste_ml_m2 = pu_dec - ps_dec

        # Volume total de banho em litros
        area_m2 = metragem_dec * larg_dec
        volume_banho_l = (arraste_ml_m2 * area_m2) / Decimal('1000')

        consumo1_g = volume_banho_l * conc1_dec
        consumo2_g = volume_banho_l * conc2_dec
        consumo3_g = volume_banho_l * conc3_dec

        consumo1_gpm = consumo1_g / metragem_dec if metragem_dec > 0 else Decimal('0')
        consumo2_gpm = consumo2_g / metragem_dec if metragem_dec > 0 else Decimal('0')
        consumo3_gpm = consumo3_g / metragem_dec if metragem_dec > 0 else Decimal('0')

        tabela = [{
            "Artigo": codigo,
            "Cor": cod_cor,
            "Descrição": descricao,
            "PS": float(ps_dec),
            "PU": float(pu_dec),
            "Pick-up %": round(float(pickup_pct), 2),
            "Largura(m)": float(larg_dec),
            "Metragem(m)": float(metragem_dec),
            "Total Banho(L)": round(float(volume_banho_l), 2),
            "Arraste Total ml/m²": round(float(arraste_ml_m2), 2),
            "Quim1": quim1,
            "Conc.Quím1(g/L)": float(conc1_dec),
            "Cons. Quím1(g/m)": round(float(consumo1_gpm), 4),
            "Quim2": quim2,
            "Conc. Quím2(g/L)": float(conc2_dec),
            "Consumo Quím2(g/m)": round(float(consumo2_gpm), 4),
            "Quim3": quim3,
            "Conc.Quím3(g/L)": float(conc3_dec),
            "Consumo Quím3(g/m)": round(float(consumo3_gpm), 4)
        }]

        # Preenche treeview
        numeric_cols = {"PS", "PU", "Pick-up %", "Largura(m)", "Metragem(m)", "Total Banho(L)", "Arraste Total ml/m²", "Conc.Quím1(g/L)", "Cons.Quím1(g/m)", "Conc.Quím2(g/L)", "Cons.Quím2(g/m)", "Conc.Quím3(g/L)", "Cons.Quím3(g/m)"}
        for item in self.tree_acabamento.get_children():
            self.tree_acabamento.delete(item)
        for idx, row in enumerate(tabela):
            values = []
            for c in self.tree_acabamento['columns']:
                v = row.get(c, "")
                if c in numeric_cols:
                    try:
                        val_float = float(v)
                        values.append(f"{val_float:.2f}")
                    except Exception:
                        values.append(v)
                else:
                    values.append(v)
            tag = 'even' if idx % 2 == 0 else 'odd'
            self.tree_acabamento.insert('', tk.END, values=values, tags=(tag,))

        # Guarda para exportação
        self.last_df_acabamento = pd.DataFrame(tabela)
        self.last_meta_acabamento = {"Código": codigo, "Cor": cod_cor, "Descrição": descricao}

        messagebox.showinfo("OK", "Cálculo de Acabamento concluído e tabela exibida.")

    def exportar(self):
        # Verifica se há dados de Tinturaria e/ou Acabamento
        tem_tinturaria = hasattr(self, 'last_df_tinturaria') and self.last_df_tinturaria is not None
        tem_acabamento = hasattr(self, 'last_df_acabamento') and self.last_df_acabamento is not None

        if not tem_tinturaria and not tem_acabamento:
            messagebox.showwarning("Aviso", "Gere pelo menos um relatório (Tinturaria ou Acabamento).")
            return

        # Pergunta por arquivo
        meta = self.last_meta_tinturaria if tem_tinturaria else self.last_meta_acabamento
        artigo = meta.get('artigo', meta.get('Código', ''))
        cor = meta.get('cor', meta.get('Cor', ''))
        descricao = meta.get('Descrição', '')

        destination_arquivo = filedialog.asksaveasfilename(
            defaultextension='.xlsx',
            filetypes=[('Excel files', '*.xlsx'), ('CSV files', '*.csv'), ('All files', '*.*')],
            initialfile=f"Relatorio_TX_Produção_{limpar_string_para_arquivo(artigo)}_{limpar_string_para_arquivo(cor)}_{limpar_string_para_arquivo(descricao)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            title='Salvar relatório como'
        )

        if not destination_arquivo:
            return

        export_mode = self.export_mode.get()
        if export_mode == 'acabamento' and not tem_acabamento:
            messagebox.showwarning("Aviso", "Gere o relatório de acabamento primeiro para exportar somente acabamento.")
            return

        try:
            path = Path(destination_arquivo)
            # Evita salvar em diretórios de sistema comuns (Windows) por segurança
            blocked_dirs = [Path(r"C:\\Windows"), Path(r"C:\\Program Files"), Path(r"C:\\Program Files (x86)")]
            parent_resolved = path.parent.resolve()
            if any(str(parent_resolved).startswith(str(b)) for b in blocked_dirs):
                messagebox.showerror("Erro", f"Salvar em {parent_resolved} não é permitido.")
                return
            if not path.parent.exists():
                path.parent.mkdir(parents=True, exist_ok=True)

            if path.suffix.lower() == '.xlsx':
                with pd.ExcelWriter(path, engine='openpyxl') as writer:
                    if export_mode == 'all':
                        if tem_tinturaria:
                            df_tinturaria = self._prepare_df_export(self.last_df_tinturaria)
                            df_tinturaria.to_excel(writer, sheet_name='Tinturaria', index=False)
                        if tem_acabamento:
                            df_acabamento = self._prepare_df_export(self.last_df_acabamento)
                            df_acabamento.to_excel(writer, sheet_name='Acabamento', index=False)
                    else:
                        df_acabamento = self._prepare_df_export(self.last_df_acabamento)
                        df_acabamento.to_excel(writer, sheet_name='Acabamento', index=False)
            else:
                if export_mode == 'all' and tem_tinturaria and tem_acabamento:
                    with path.open('w', encoding='utf-8-sig', newline='') as f:
                        f.write('Tinturaria\n')
                        self._prepare_df_export(self.last_df_tinturaria).to_csv(f, sep=';', index=False)
                        f.write('\n')
                        f.write('Acabamento\n')
                        self._prepare_df_export(self.last_df_acabamento).to_csv(f, sep=';', index=False)
                elif export_mode == 'all' and tem_tinturaria:
                    df_to_save = self._prepare_df_export(self.last_df_tinturaria)
                    df_to_save.to_csv(path, sep=';', encoding='utf-8-sig', index=False)
                else:
                    df_to_save = self._prepare_df_export(self.last_df_acabamento)
                    df_to_save.to_csv(path, sep=';', encoding='utf-8-sig', index=False)

            messagebox.showinfo("Sucesso", f"Relatório salvo em:\n{path}")
        except ImportError:
            messagebox.showerror("Erro", "Biblioteca 'openpyxl' não instalada. Instale com: pip install openpyxl")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar o arquivo:\n{e}")

    def _prepare_df_export(self, df):
        """Prepara DataFrame para exportação com formatação adequada."""
        df_export = df.copy()
        
        # Identifica colunas numéricas
        numeric_cols = []
        for col in df_export.columns:
            if col in ["Metragem(m)", "Peso(kg)", "Gramatura(g/m)", "Tempo(Dec)", "Taxa Prod.", 
                       "g/m² Seco", "g/m² Úmido", "Pick-up %", "Largura (m)", 
                       "Metragem (m)", "Total Banho (L)", "Arraste Total ml/m²", 
                       "Conc. Quím1 (g/L)", "Consumo Quím1 (g/m)", "Conc. Quím2 (g/L)", "Consumo Quím2 (g/m)", 
                       "Conc. Quím3 (g/L)", "Consumo Quím3 (g/m)"]:
                numeric_cols.append(col)
        
        # Arredonda colunas numéricas
        for col in numeric_cols:
            if col in df_export.columns:
                df_export[col] = pd.to_numeric(df_export[col], errors='coerce').round(2).fillna(0.0)
        
        return df_export


if __name__ == '__main__':
    app = App()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        try:
            app.quit()
        except Exception:
            pass