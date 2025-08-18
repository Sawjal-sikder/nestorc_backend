from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.contrib.auth import get_user_model
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from reportlab.lib import colors
from openpyxl import Workbook
from io import BytesIO

User = get_user_model()


def download_all_user_pdf(request):
    # Create buffer
    buffer = BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']

    # Heading
    elements.append(Paragraph("All User List", title_style))
    elements.append(Spacer(1, 20))

      # Table header
    data = [["Full Name", "Email", "Phone", "Active"]]

      # Fetch all users
    users = User.objects.filter(is_active=True)
    for user in users:
            full_name = user.full_name
            email = user.email
            phone = user.phone_number 
            is_active = "Yes" if user.is_active else "No"
            data.append([full_name, email, phone, is_active])

    # Table styling
    table = Table(data, colWidths=[150, 200, 100, 50])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME', (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0),(-1,0), 12),
        ('BOTTOMPADDING', (0,0),(-1,0), 12),
        ('BACKGROUND',(0,1),(-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    elements.append(table)

    # Build PDF
    doc.build(elements)

    # Return response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_users.pdf"'
    return response


def download_all_user_excel(request):
    # Create workbook and sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Users"

    # Header row
    ws.append(["Full Name", "Email", "Phone", "Active"])

    # Fetch active users
    users = User.objects.filter(is_active=True)
    for user in users:
        full_name = user.full_name
        email = user.email
        phone = user.phone_number
        is_active = "Yes" if user.is_active else "No"
        ws.append([full_name, email, phone, is_active])

    # Create HTTP response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="all_users.xlsx"'

    # Save workbook to response
    wb.save(response)
    return response