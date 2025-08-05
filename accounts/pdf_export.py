from django.http import HttpResponse, HttpResponseServerError
from datetime import datetime
from .models import CustomUser

def download_user_pdf(modeladmin, request, queryset):
    """Export selected users to PDF only"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
    except ImportError:
        # Return error response if reportlab is not installed
        return HttpResponseServerError("ReportLab is required for PDF generation. Please install reportlab package.")
    
    # Enhanced PDF generation if reportlab is available
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="selected_users.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    
    # Header
    p.setFont("Helvetica-Bold", 20)
    p.drawString(100, height - 100, "Selected Users Report")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 130, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(100, height - 150, f"Total Users: {queryset.count()}")
    
    # Draw a line
    p.line(100, height - 170, width - 100, height - 170)
    
    # Table headers
    y = height - 200
    p.setFont("Helvetica-Bold", 10)
    p.drawString(100, y, "Full Name")
    p.drawString(250, y, "Email")
    p.drawString(400, y, "Phone")
    p.drawString(500, y, "Active")
    
    # Table content
    p.setFont("Helvetica", 9)
    y -= 20
    
    for user in queryset:
        if y < 50:  # Start new page if near bottom
            p.showPage()
            y = height - 100
            # Repeat headers on new page
            p.setFont("Helvetica-Bold", 10)
            p.drawString(100, y, "Full Name")
            p.drawString(250, y, "Email")
            p.drawString(400, y, "Phone")
            p.drawString(500, y, "Active")
            p.setFont("Helvetica", 9)
            y -= 20
        
        # Truncate long text to fit
        full_name = (user.full_name or 'N/A')[:20]
        email = user.email[:25] if len(user.email) > 25 else user.email
        phone = (user.phone_number or 'N/A')[:15]
        active_status = "Yes" if user.is_active else "No"
        
        p.drawString(100, y, full_name)
        p.drawString(250, y, email)
        p.drawString(400, y, phone)
        p.drawString(500, y, active_status)
        y -= 15

    p.showPage()
    p.save()
    return response

download_user_pdf.short_description = "Download PDF of selected users (PDF only)"


def download_all_users_pdf(request):
    """Download all users as PDF only"""
    queryset = CustomUser.objects.all()
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
    except ImportError:
        # Return error response if reportlab is not installed
        return HttpResponseServerError("ReportLab is required for PDF generation. Please install reportlab package.")
    
    # Enhanced PDF generation
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_users_report.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    
    # Header
    p.setFont("Helvetica-Bold", 20)
    p.drawString(100, height - 100, "Nestorc Users Report")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 130, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(100, height - 150, f"Total Users: {queryset.count()}")
    
    # Draw a line
    p.line(100, height - 170, width - 100, height - 170)
    
    # Table headers
    y = height - 200
    p.setFont("Helvetica-Bold", 10)
    p.drawString(100, y, "Full Name")
    p.drawString(250, y, "Email")
    p.drawString(400, y, "Phone")
    p.drawString(500, y, "Active")
    
    # Table content
    p.setFont("Helvetica", 9)
    y -= 20
    
    for user in queryset:
        if y < 50:  # Start new page if near bottom
            p.showPage()
            y = height - 100
            # Repeat headers on new page
            p.setFont("Helvetica-Bold", 10)
            p.drawString(100, y, "Full Name")
            p.drawString(250, y, "Email")
            p.drawString(400, y, "Phone")
            p.drawString(500, y, "Active")
            p.setFont("Helvetica", 9)
            y -= 20
        
        # Truncate long text to fit
        full_name = (user.full_name or 'N/A')[:20]
        email = user.email[:25] if len(user.email) > 25 else user.email
        phone = (user.phone_number or 'N/A')[:15]
        active_status = "Yes" if user.is_active else "No"
        
        p.drawString(100, y, full_name)
        p.drawString(250, y, email)
        p.drawString(400, y, phone)
        p.drawString(500, y, active_status)
        y -= 15

    p.showPage()
    p.save()
    return response

download_all_users_pdf.short_description = "Download all users as PDF (PDF only)"
