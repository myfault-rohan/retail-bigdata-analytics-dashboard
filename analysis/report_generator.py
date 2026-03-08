import pandas as pd
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Define file paths
DATA_PATH = "data/processed_sales.csv"
PDF_REPORT = "sales_report.pdf"
EXCEL_REPORT = "sales_report.xlsx"

def generate_reports():
    print(f"Loading data from {DATA_PATH}...")
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} not found.")
        return

    df = pd.read_csv(DATA_PATH)
    
    # 2. Compute summary metrics
    total_sales = df['total_sales'].sum()
    num_countries = df['Country'].nunique()
    top_5_countries = df.groupby('Country')['total_sales'].sum().reset_index()
    top_5_countries = top_5_countries.sort_values(by='total_sales', ascending=False).head(5)

    print("Computing metrics...")
    print(f"Total Sales: ${total_sales:,.2f}")
    print(f"Number of Countries: {num_countries}")

    # 3. Generate PDF report
    print(f"Generating PDF: {PDF_REPORT}...")
    doc = SimpleDocTemplate(PDF_REPORT, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=1, # Center
        spaceAfter=30
    )
    elements.append(Paragraph("Retail Sales Analytics Report", title_style))

    # Metrics Section
    elements.append(Paragraph("<b>Summary Metrics</b>", styles['Heading2']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<b>Total Global Sales:</b> ${total_sales:,.2f}", styles['Normal']))
    elements.append(Paragraph(f"<b>Number of Unique Countries:</b> {num_countries}", styles['Normal']))
    elements.append(Spacer(1, 24))

    # Top 5 Countries Table
    elements.append(Paragraph("<b>Top 5 Countries by Sales</b>", styles['Heading2']))
    elements.append(Spacer(1, 12))

    # Prepare table data
    table_data = [["Country", "Total Sales ($)"]]
    for _, row in top_5_countries.iterrows():
        table_data.append([row['Country'], f"{row['total_sales']:,.2f}"])

    table = Table(table_data, colWidths=[200, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)

    # Build PDF
    doc.build(elements)
    print("PDF generation complete.")

    # 6. Export Excel report
    print(f"Generating Excel: {EXCEL_REPORT}...")
    # Create a summary sheet and a top 5 sheet
    with pd.ExcelWriter(EXCEL_REPORT, engine='openpyxl') as writer:
        summary_df = pd.DataFrame({
            "Metric": ["Total Global Sales", "Number of Countries"],
            "Value": [f"${total_sales:,.2f}", num_countries]
        })
        summary_df.to_sheet_name = "Summary"
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        top_5_countries.to_excel(writer, sheet_name="Top 5 Countries", index=False)
    
    print("Excel generation complete.")
    print("All reports generated successfully!")

if __name__ == "__main__":
    generate_reports()
