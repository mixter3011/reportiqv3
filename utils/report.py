from utils.plotting import (
    plot_table_and_pie,
    plot_combined_table,
    create_fno_table_and_graph,
)
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

def get_customer_details(holding_df):
    client_row = holding_df[holding_df['Unnamed: 0'] == 'Client Equity Code/UCID/Name']
    
    if client_row.empty:
        raise ValueError("Could not find client information row in the Holding dataframe")
    
    client_info = client_row['Unnamed: 1'].iloc[0]
    
    parts = client_info.split('/')
    if len(parts) != 3:
        raise ValueError(f"Unexpected format in client information: {client_info}")
    
    ucid = parts[1]
    customer_name = parts[2]
    
    return customer_name, ucid

def create_cover_page(pdf, customer_name, ucid):
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    gradient = np.linspace(1, 0.9, 500).reshape(1, -1)
    ax.imshow(
        gradient,
        extent=(0, 1, 0, 1),
        cmap='Blues',
        aspect='auto',
        alpha=0.3
    )
    
    logo_img = plt.imread('logo.png')
    logo_ax = fig.add_axes([0.78, 0.88, 0.2, 0.08])  
    logo_ax.imshow(logo_img)
    logo_ax.axis('off')

    ax.text(
        0.04, 0.92, "CUSTOMER STATEMENT",
        fontsize=32, color='#8B0000',
        weight='light'
    )

    current_date = pd.Timestamp.now().strftime('%d-%b-%Y')
    ax.text(
        0.045, 0.88,  
        f"Report Level : Member | Report Period : Since Inception to {current_date}",
        fontsize=16, color='#2F4F4F'
    )

    ax.text(0.05, 0.6, customer_name, fontsize=28, color='#2F4F4F', weight='bold')  
    ax.text(0.05, 0.55, f"UCID : {ucid}", fontsize=20, color='#2F4F4F') 

    footer_text = (
        "This document is not valid without disclosure, please refer to the last page for the disclaimer. | "
        "Strictly Private & Confidential.\n"
        f"Incase of any query / feedback on the report, please write to query@motilaloswal.com. | "
        f"Generated Date & Time : {current_date} | {pd.Timestamp.now().strftime('%I:%M %p')}"
    )
    ax.text(
        0.5, 0.1, footer_text,
        horizontalalignment='center',
        fontsize=12,
        color='#2F4F4F',
        wrap=True
    )

    ax.text(
        0.056, 0.23, "WINNING PORTFOLIOS",
        fontsize=14,
        color='#2F4F4F',
        weight='bold'
    )

    ax.text(
        0.05, 0.2, "POWERED BY KNOWLEDGE",  
        fontsize=14,
        color='white',
        bbox=dict(
            facecolor='#FF0000',
            edgecolor='none',
            boxstyle='round,pad=0.5'
        )
    )

    footer_img = plt.imread('footer.png')
    footer_logo_ax = fig.add_axes([0.23, 0.12, 0.8, 0.2])  
    footer_logo_ax.imshow(footer_img)
    footer_logo_ax.axis('off')

    plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
    pdf.savefig(fig, bbox_inches=None, pad_inches=0)
    plt.close(fig)

def create_footer_page(pdf):
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111)
    
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    gradient = np.linspace(1, 0.9, 500).reshape(1, -1)
    ax.imshow(
        gradient,
        extent=(0, 1, 0, 1),
        cmap='Blues',
        aspect='auto',
        alpha=0.3
    )

    logo_img = plt.imread('logo.png')
    logo_ax = fig.add_axes([0.79, 0.9, 0.2, 0.08])  
    logo_ax.imshow(logo_img)
    logo_ax.axis('off')
    
    ax.text(
        0.11, 0.92, "Notes & Assumptions",
        fontsize=32, color='#8B0000',
        weight='light'
    )

    current_date = pd.Timestamp.now().strftime('%d-%b-%Y')
    
    main_txt = (
        "1. All valuation as on last available Price / NAV.\n\n"
        "2. Unrealised Gain / Loss = Market Value - Investment at cost. It does not account for Dividend / Interest Paid out. XIRR will be frozen for that day till next valuation is available.\n\n"
        "3. XIRR and Benchmark Values are calculated on balance units for open scripts / folios. In case there are reinvestments in a prior closed script / folio, then all historical cashflow of that script / foliow will be considered\n\n     for XIRR & Benchmark Calculations.\n\n"
        "4. All Private Equity Funds(RE) and Real Estate Funds(RE) are classified as Alternates (Unquoted).Since Quoted Valuations of PE & RE Funds are not available its Market value is computed as Total Drawdown(Cost) -\n\n    Capital Returned.XIRR and benchmarks are not computed for PE & RE Funds.\n\n"
        "5. If bifurcation between Capital Return & Profit is not provided by Manufacturers for AIF / PE / RE distribution, they will appear as Profit / Unallocated distribution in report.\n\n"
        "6. Net investments for PMS might not match with AMC statement due to difference in calculation methodology.In case if cost in folio is less than equal to zero and Market Value is less than 50000, we will consider this\n\n    as a cloud investment and will not appear in report.\n\n"
        "7. For Mutual Funds, less than 1 units or fraction unit is considered as closed.\n\n"
        "8. Capital Gain / (Loss) – for Equity Stocks / Mutual Fund: Short Term < 1 Year, Long Term > 1 Year; & for Debt Mutual Fund Only, Short Term < 3 Years, Long Term > 3 Years. Long Term Capital Gains (LTCG) and Short\n\n     Term Capital Gains (STCG) does not account for Exit Loads.\n\n"
        "9. Interest accrued - all unpaid interest is accrued on FV from the last Interest Payment date.\n\n"
        "10. Bonds & Other listed instruments: Valuation of instruments that are actively traded on the exchange will be shown at the market price. Due to market dependent bid - ask spreads,the availability of the price\n\n      displayed cannot be guaranteed. For debt instruments which are not actively traded on the exchange, valuation will be shown at Face Value.\n\n"
        "11. For Direct equity transactions, balance quantity is adjusted on trade date, while the Demat Service provider may account for it within T + 3 days.\n\n"
        "12. Any case where DP is not with Motilal Oswal Financial Services Limited, all stock trades will be squared off at the end of day.\n\n"
        "13. In Case of a corporate action on a Direct Equity Stock, Holdings in Report might not Tally with DP due to delay in receiving corporate action transactions in DP.\n\n"
        "14. In case of any security held as collateral, this will appear in the client portfolio and might not tally with actual DP holdings.\n\n"
        "15. Unit rate of Stocks acquired in ESOP / bought via other brokers / Off Market Transfers might not tally with actual buying price. Please contact your Advisor to update the same.\n\n"
        "16. Since values are displayed in Lakhs, total of individual rows might not match with Grand Total Row on account of rounding off differences.\n\n"
        "17. In case of IPO issue price declared will be taken as cost.\n\n"
        "18. Arbitrage Funds are classified in the report as Debt based on underlying risk. This differs from SEBI classification.\n\n"
        "19. Benchmark XIRR calculations are done by imitating the cash flows of each security on underlying benchmark (as per benchmark list).\n\n"
        "20. The ledger balances depicted above is held with Motilal Oswal Financial Services Limited: No changes.\n\n"
        "21. The Bank balances depicted above are held with HDFC Bank having Power of Attorney with Motilal Oswal Wealth Limited/HDFC Custody.\n\n"
        "22. We are showing the Bank and Ledger balances August 1st, 2023 onwards. We are not displaying back-dated bank and ledger balances.\n\n"
    )
    
    ax.text(
        0.04, 0.04,
        main_txt,
        horizontalalignment='left',
        fontsize=10,
        color='#2F4F4F'
    )

    footer_text = (
        "This document is not valid without disclosure, please refer to the last page for the disclaimer. | "
        "Strictly Private & Confidential.\n"
        f"Incase of any query / feedback on the report, please write to query@motilaloswal.com. | "
        f"Generated Date & Time : {current_date} | {pd.Timestamp.now().strftime('%I:%M %p')}"
    )
    ax.text(
        0.5, 0.02, footer_text,
        horizontalalignment='center',
        fontsize=10,
        color='#2F4F4F',
        wrap=True
    )
    
    footer = plt.imread('header.png')
    footer_ax = fig.add_axes([0.02, 0.77, 0.9, 0.3])
    footer_ax.imshow(footer)
    footer_ax.axis('off')

    pdf.savefig(fig, bbox_inches=None, pad_inches=0)
    plt.close(fig)

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

def create_portfolio_reports(data, portfolio_dir):
    try:
        Portfolio_Value = data['Portfolio Value']
        Holding = data['Holding']
        xirr = data['XIRR']
        equity = data['Equity']
        debt = data['Debt']
        fno = data['FNO']
        profit = data['Profits']
        
        customer_name, ucid = get_customer_details(Holding)
        
        Portfolio_Value_Modified, cash_equivalent_value, cash_equivalent_percentage, equity_allocation_percentage = rearrange_and_add_total(
            Portfolio_Value
        )
        
        portfolio_dir = Path(portfolio_dir)
        
        with PdfPages(portfolio_dir / 'portfolio_report.pdf') as pdf:
            # Create cover page with extracted customer details
            create_cover_page(pdf, customer_name, ucid)

            fig1 = plot_table_and_pie(
                Portfolio_Value_Modified,
                Holding,
                xirr,
                cash_equivalent_value,
                cash_equivalent_percentage,
                equity_allocation_percentage,
            )
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
            pdf.savefig(fig3, bbox_inches='tight')
            plt.close(fig3)

            fig4 = create_fno_table_and_graph(fno)
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
            pdf.savefig(fig6, bbox_inches='tight')
            plt.close(fig6)
            
            create_footer_page(pdf)

    except Exception as e:
        print(f"Error generating reports: {e}")