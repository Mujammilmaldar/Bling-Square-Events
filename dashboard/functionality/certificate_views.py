from django.shortcuts import render, HttpResponse
from django.template.loader import render_to_string
from datetime import date
from tempfile import NamedTemporaryFile
import subprocess

def certificate_form(request):
    if request.method == 'POST':
        intern_name = request.POST.get('intern_name')
        designation = request.POST.get('designation')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        praise = request.POST.get('praise')
        
        # Get today's date
        today_date = date.today().strftime("%B %d, %Y")

        # Render the certificate template with the form data and today's date
        context = {
            'intern_name': intern_name,
            'designation': designation,
            'start_date': start_date,
            'end_date': end_date,
            'praise': praise,
            'today_date': today_date,
        }
        return render(request, 'certificate_template.html', context)

    return render(request, 'certificate_form.html')

def generate_certificate(request):
    if request.method == 'POST':
        intern_name = request.POST.get('intern_name', '')
        designation = request.POST.get('designation', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        praise = request.POST.get('praise', '')
        
        # Get today's date
        today_date = date.today().strftime("%B %d, %Y")

        # Prepare data to pass to the template
        context = {
            'intern_name': intern_name,
            'designation': designation,
            'start_date': start_date,
            'end_date': end_date,
            'praise': praise,
            'today_date': today_date,
        }

        # Render HTML content from a Django template with the provided context
        html_content = render_to_string('certificate_template.html', context)

        # Write HTML content to a temporary file
        with NamedTemporaryFile(suffix='.html', delete=False) as temp_html_file:
            temp_html_file.write(html_content.encode('utf-8'))

        # Specify output PDF file path
        pdf_file = temp_html_file.name.replace('.html', '.pdf')

        # Generate PDF using wkhtmltopdf
        subprocess.run(['wkhtmltopdf', temp_html_file.name, pdf_file], check=True)

        # Serve PDF as a downloadable attachment
        with open(pdf_file, 'rb') as f:
            pdf_data = f.read()

        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
        return response

    else:
        return HttpResponse("Invalid request method. Please submit the form.")
