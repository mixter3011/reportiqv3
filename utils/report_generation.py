from utils.plotting import (
    plot_table_and_pie,
    plot_combined_table,
    create_fno_table_and_graph,
)
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import pandas as pd

def create_portfolio_reports(data, portfolio_dir):
    try:
        Portfolio_Value = data['Portfolio Value']
        Holding = data['Holding']
        xirr = data['XIRR']
        equity = data['Equity']
        debt = data['Debt']
        fno = data['FNO']
        profit = data['Profits']
        
        Portfolio_Value_Modified, cash_equivalent_value, cash_equivalent_percentage, equity_allocation_percentage = rearrange_and_add_total(
            Portfolio_Value
        )
        fig1 = plot_table_and_pie(
            Portfolio_Value_Modified,
            Holding,
            xirr,
            cash_equivalent_value,
            cash_equivalent_percentage,
            equity_allocation_percentage,
        )
        with PdfPages(portfolio_dir / 'portfolio_overview.pdf') as pdf:
            pdf.savefig(fig1, bbox_inches='tight')
        plt.close(fig1)

        fig2, ax2 = plt.subplots(figsize=(18, 12))
        direct_equity_df, de_sums = preprocess_table(
            equity[equity['Category'] == 'Direct Equity'], "Direct Equity"
        )
        equity_etf_df, etf_sums = preprocess_table(
            equity[equity['Category'] == 'Equity ETF'], "Equity ETF"
        )
        equity_mf_df, mf_sums = preprocess_table(
            equity[equity['Category'] == 'Equity Mutual Fund'], "Equity Mutual Fund"
        )
        plot_combined_table(
            [direct_equity_df, equity_etf_df, equity_mf_df],
            [de_sums, etf_sums, mf_sums],
            ax2,
        )
        with PdfPages(portfolio_dir / 'equity_holdings.pdf') as pdf:
            pdf.savefig(fig2, bbox_inches='tight')
        plt.close(fig2)

        fig3, ax3 = plt.subplots(figsize=(18, 12))
        debt_mf, mf_sums = preprocess_table(
            debt[debt['Category'] == 'Debt Mutual Fund'], "Debt Mutual Fund"
        )
        debt_etf, etf_sums = preprocess_table(
            debt[debt['Category'] == 'Debt ETF'], "Debt ETF"
        )
        plot_combined_table([debt_etf, debt_mf], [etf_sums, mf_sums], ax3)
        with PdfPages(portfolio_dir / 'debt_holdings.pdf') as pdf:
            pdf.savefig(fig3, bbox_inches='tight')
        plt.close(fig3)

        fig4 = create_fno_table_and_graph(fno)
        with PdfPages(portfolio_dir / 'fno_analysis.pdf') as pdf:
            pdf.savefig(fig4, bbox_inches='tight')
        plt.close(fig4)

        fig5 = plt.figure(figsize=(12, 8))
        profit_cleaned = profit.dropna().iloc[:-1]
        table1 = plt.table(
            cellText=profit_cleaned.values,
            colLabels=profit_cleaned.columns,
            cellLoc='center',
            loc='center',
        )
        table1.auto_set_font_size(False)
        table1.set_fontsize(9)
        table1.scale(1.0, 1.5)
        plt.title('Realised Gain', pad=10, size=14, weight='bold')
        plt.axis('off')
        with PdfPages(portfolio_dir / 'realized_gains.pdf') as pdf:
            pdf.savefig(fig5, bbox_inches='tight')
        plt.close(fig5)

        fig6 = plt.figure(figsize=(8, 4))
        product_gains = calculate_unrealized_gains(Holding)
        colors = ['#B7E3E4', '#B5D5A7']
        plt.pie(
            product_gains.values(),
            labels=product_gains.keys(),
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
        )
        plt.title('Unrealized Gains Distribution', pad=20)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig6.gca().add_artist(centre_circle)
        with PdfPages(portfolio_dir / 'unrealized_gains.pdf') as pdf:
            pdf.savefig(fig6, bbox_inches='tight')
        plt.close(fig6)

    except Exception as e:
        print(f"Error generating reports: {e}")


def rearrange_and_add_total(df):
    df["Portfolio Value"] = pd.to_numeric(df["Portfolio Value"], errors='coerce')
    df["Portfolio Value"] = df["Portfolio Value"].round().astype(int)
    order = ["Available Cash", "Debt", "Equity", "Gold"]
    ordered_df = df[df["Portfolio Component"].isin(order)].copy()
    ordered_df["Order"] = ordered_df["Portfolio Component"].map(lambda x: order.index(x))
    ordered_df = ordered_df.sort_values(by="Order").drop(columns=["Order"])

    grand_total_value = ordered_df["Portfolio Value"].sum()
    cash_equivalent_value = ordered_df.loc[
        ordered_df["Portfolio Component"].isin(["Available Cash", "Debt"]),
        "Portfolio Value",
    ].sum()
    cash_equivalent_percentage = round((cash_equivalent_value / grand_total_value) * 100)
    equity_allocation_percentage = 100 - cash_equivalent_percentage

    grand_total_row = {
        "Portfolio Component": "Grand Total",
        "Portfolio Value": f"{grand_total_value:,}",
    }
    result_df = pd.concat([ordered_df, pd.DataFrame([grand_total_row])], ignore_index=True)

    return result_df, cash_equivalent_value, cash_equivalent_percentage, equity_allocation_percentage


def preprocess_table(dataframe, category_name):
    dataframe = dataframe.sort_values(by='Market Value', ascending=False)
    numeric_columns = ['Quantity', 'Buy Price', 'CMP', 'PandL', 'Market Value']
    sums = dataframe[numeric_columns].sum()
    dataframe['Category'] = category_name

    total_row = pd.DataFrame(
        {col: [sums[col] if col in sums else ''] for col in dataframe.columns}
    )
    total_row['Category'] = f"{category_name} Total"
    result_df = pd.concat([dataframe, total_row], ignore_index=True)

    return result_df, sums


def calculate_unrealized_gains(Holding):
    product_gains = {}
    
    equity_mask = Holding['Unnamed: 0'].str.contains('Equity:-', na=False)
    if equity_mask.any():
        equity_start = equity_mask.idxmax() + 2
        equity_data = Holding.iloc[equity_start:].copy()
        total_row = equity_data[equity_data['Unnamed: 0'] == 'Total:']
        if not total_row.empty:
            try:
                equity_gain = float(total_row['Unnamed: 10'].iloc[0])
                product_gains['Equity'] = equity_gain
            except ValueError:
                product_gains['Equity'] = 0.0

    mf_mask = Holding['Unnamed: 0'].str.contains('Mutual Fund:-', na=False)
    if mf_mask.any():
        mf_start = mf_mask.idxmax() + 2
        mf_data = Holding.iloc[mf_start:].copy()
        mf_total_row = mf_data[mf_data['Unnamed: 0'] == 'Total:']
        if not mf_total_row.empty:
            try:
                mf_gain = float(mf_total_row['Unnamed: 10'].iloc[0])
                product_gains['Mutual Fund'] = mf_gain
            except ValueError:
                product_gains['Mutual Fund'] = 0.0

    return product_gains
