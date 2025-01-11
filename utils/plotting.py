import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from typing import List, Dict
import pandas as pd
import numpy as np


def plot_table_and_pie(df, Holding, xirr, cash_equivalent_value, cash_equivalent_percentage, equity_allocation_percentage):
    fig = plt.figure(figsize=(16, 10))

    fig.patches.extend([plt.Rectangle((0, 0.85), 1, 0.15, 
                                      facecolor='lightblue', 
                                      transform=fig.transFigure, 
                                      figure=fig, alpha=0.3)])

    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1])
    
    ax_table = fig.add_subplot(gs[0])
    ax_table.axis('tight')
    ax_table.axis('off')

    xirr_value = (
        float(xirr['Remarks'].iloc[-1]) * 100 
        if not xirr.empty and 'Remarks' in xirr.columns else "N/A"
    )
    if isinstance(xirr_value, float):
        xirr_value = f"{xirr_value:.2f}%"
    
    client_info_raw = (
        Holding['Unnamed: 1'].iloc[1]
        if not Holding.empty and 'Unnamed: 1' in Holding.columns and len(Holding) > 1
        else "N/A"
    )
    if '/' in client_info_raw:
        parts = client_info_raw.split('/')
        name = parts[-1]
        id_num = parts[0]
    else:
        name = client_info_raw
        id_num = ""

    fig.text(0.5, 0.94, name, fontsize=16, fontweight='bold', ha='center')
    fig.text(0.5, 0.89, id_num, fontsize=16, fontweight='bold', ha='center')

    summary_data = [
        ("Portfolio Value", df.iloc[-1]['Portfolio Value']),
        ("Cash Equivalent", f"{cash_equivalent_value:,}"),
        ("Cash Equivalent %", f"{cash_equivalent_percentage:.2f}%"),
        ("Equity Allocation %", f"{equity_allocation_percentage:.2f}%"),
        ("XIRR Value", xirr_value),
    ]

    y_pos = 0.75
    line_height = 0.06
    for label, value in summary_data:
        ax_table.text(0.1, y_pos, f"{label}:", transform=fig.transFigure, fontweight='bold', fontsize=14, horizontalalignment='left')
        ax_table.text(0.45, y_pos, str(value), transform=fig.transFigure, fontsize=14, horizontalalignment='right')
        y_pos -= line_height

    table_y_pos = y_pos - 0.05
    table_data = df.values
    table = ax_table.table(
        cellText=table_data,
        colLabels=["Portfolio Component", "Portfolio Value (Sum)"],
        loc='center',
        cellLoc='right',
        colColours=["#E6E6FA", "#E6E6FA"],
        bbox=[-0.06, table_y_pos - 0.19, 1.2, 0.24],
        colWidths=[0.6, 0.4]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    for (row, col), cell in table._cells.items():
        cell.set_height(0.1)
        cell.set_text_props(ha='left' if col == 0 else 'right')
        cell.set_edgecolor('#D3D3D3')
        cell.set_facecolor('white')

    ax_pie = fig.add_subplot(gs[1])
    fig.text(0.685, 0.76, "Portfolio Composition", fontsize=14, fontweight='bold', ha='center')
    pie_data = []
    pie_labels = []

    for _, row in df.iterrows():
        if row['Portfolio Component'] != "Grand Total":
            try:
                value = float(str(row['Portfolio Value']).replace(',', ''))
                if value > 0:
                    pie_data.append(value)
                    pie_labels.append(row['Portfolio Component'])
            except (ValueError, AttributeError):
                continue

    colors = ['#B7E3E4', '#B5D5A7', '#D9E1F2', '#FFE699']
    wedges, texts, autotexts = ax_pie.pie(
        pie_data,
        labels=[''] * len(pie_data),
        autopct='%1.0f%%',
        startangle=90,
        colors=colors,
        pctdistance=0.75,
        center=(0, -0.1),
    )
    plt.setp(autotexts, size=10, weight="bold", color='black')
    ax_pie.legend(wedges, pie_labels, loc='center right', bbox_to_anchor=(1.3, 0.5))
    centre_circle = plt.Circle((0, -0.1), 0.60, fc='white')
    ax_pie.add_artist(centre_circle)
    ax_pie.axis('equal')

    plt.subplots_adjust(top=0.85, right=0.85, left=0.1, bottom=0.1)

    return fig


def plot_combined_table(dataframes: List[pd.DataFrame], raw_sums: List[Dict[str, float]], ax):
    combined_df = pd.concat(dataframes, ignore_index=True)

    if raw_sums:
        grand_totals = {}
        for col in ['Quantity', 'Buy Price', 'CMP', 'PandL', 'Market Value']:
            total = sum(sums.get(col, 0) for sums in raw_sums)
            if total != 0:
                grand_totals[col] = total

        formatted_grand_totals = {col: f"{value:,.2f}" for col, value in grand_totals.items()}

        grand_total_data = []
        for col in combined_df.columns:
            if col == 'Category':
                grand_total_data.append("Grand Total")
            elif col == 'Instrument Name':
                grand_total_data.append("")
            elif col in formatted_grand_totals:
                grand_total_data.append(formatted_grand_totals[col])
            else:
                grand_total_data.append("")

        grand_total_row = pd.DataFrame([grand_total_data], columns=combined_df.columns)
        combined_df = pd.concat([combined_df, grand_total_row], ignore_index=True)

    ax.axis('tight')
    ax.axis('off')
    table = ax.table(
        cellText=combined_df.values,
        colLabels=combined_df.columns,
        loc='center',
        cellLoc='center',
        colLoc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)

    for key, cell in table._cells.items():
        if key[1] == 1:
            cell.set_width(0.30)
        else:
            cell.set_width(0.15)
        cell.set_height(0.12)
        cell.set_text_props(weight='normal')

        if key[0] > 0:
            cell_text = str(combined_df.iloc[key[0]-1, 0])
            if "Total" in cell_text:
                cell.set_facecolor('#f0f0f0')
                cell.set_text_props(weight='bold')

        if key[0] == 0:
            cell.set_text_props(weight='bold')

    return table

def create_fno_table_and_graph(df):
    df_cleaned = df.drop(columns=['Order'], errors='ignore')
    df_sorted = df_cleaned.sort_values(by='FNO Profits Till Date', ascending=True)

    total_profit = df_sorted['FNO Profits Till Date'].iloc[-1]
    avg_profit = df_sorted['FNO Profits'].mean()

    fig, (ax_table, ax_text, ax_graph) = plt.subplots(
        3, 1, figsize=(12, 14), height_ratios=[2, 0.3, 2], gridspec_kw={'hspace': 0.3}
    )

    ax_table.axis('tight')
    ax_table.axis('off')
    table = ax_table.table(
        cellText=df_sorted.values,
        colLabels=df_sorted.columns,
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    ax_table.set_title("FNO Data Table", pad=20)

    ax_text.axis('off')
    ax_text.text(0.1, 0.5, f"Total FNO Profit: {total_profit:,.2f}", fontsize=12, weight='bold')
    ax_text.text(0.1, 0.1, f"Average FNO Profit: {avg_profit:,.2f}", fontsize=12, weight='bold')

    ax_graph.plot(
        df_sorted['Month'],
        df_sorted['FNO Profits Till Date'],
        marker='o',
        linewidth=2,
        markersize=8
    )
    ax_graph.set_xlabel("Month")
    ax_graph.set_ylabel("FNO Profits Till Date")
    ax_graph.grid(True, linestyle='--', alpha=0.7)
    ax_graph.tick_params(axis='x', rotation=45)

    return fig
