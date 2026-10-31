from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
STATUS_FILLS = {
    "Up": PatternFill("solid", fgColor="F8CBAD"),       # گرانی: قرمز روشن
    "Down": PatternFill("solid", fgColor="C6EFCE"),     # ارزانی: سبز روشن
    "New": PatternFill("solid", fgColor="DDEBF7"),      # جدید: آبی روشن
    "Removed": PatternFill("solid", fgColor="D9D9D9"),  # حذف‌شده: خاکستری
}


def style_header(ws):
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center")
    ws.freeze_panes = "A2"


def autofit(ws, max_width=50):
    for column in ws.columns:
        max_len = max(len(str(c.value)) if c.value is not None else 0 for c in column)
        ws.column_dimensions[column[0].column_letter].width = min(max_len + 4, max_width)


def format_report(filename):
    wb = load_workbook(filename)

    for ws in wb.worksheets:
        style_header(ws)

    # جداکننده‌ی هزارگان برای ستون‌های قیمت
    for ws in wb.worksheets:
        headers = {cell.value: cell.column for cell in ws[1]}
        formats = {
            "Price": "#,##0",
            "Price_old": "#,##0",
            "Diff": "#,##0",
            "Pct": '0.0"%"',
        }
        for name, fmt in formats.items():
            if name in headers:
                col = headers[name]
                for row in ws.iter_rows(min_row=2, min_col=col, max_col=col):
                    row[0].number_format = fmt
    # رنگ ردیف‌ها در شیت Changes
    if "Changes" in wb.sheetnames:
        ws = wb["Changes"]
        headers = {cell.value: cell.column for cell in ws[1]}
        status_col = headers["Status"]
        for row in ws.iter_rows(min_row=2):
            fill = STATUS_FILLS.get(row[status_col - 1].value)
            if fill:
                for cell in row:
                    cell.fill = fill

    for ws in wb.worksheets:
        autofit(ws)

    wb.save(filename)