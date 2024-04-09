from django.template.loader import render_to_string
from django.http import HttpResponse
from tempfile import NamedTemporaryFile
import subprocess
import os
from ..models import CustomUser

def generate_pdf(request):
    try:
        # Check if wkhtmltopdf is installed
        subprocess.run(['wkhtmltopdf', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        
        id = request.user.id
        data = CustomUser.objects.get(id=id)
        # Prepare context data to pass to the template
        context = {
            'current_user':data,
            # Add any other context variables here
        }

        # Render HTML content from a Django template with the provided context
        html_content = render_to_string('id_card_template.html', context)

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
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'
        return response

    except subprocess.CalledProcessError as e:
        if e.stderr:
            error_message = e.stderr.decode()
        else:
            error_message = "Unknown error"
        return HttpResponse(f'Error generating PDF: {error_message}', status=500)

    except Exception as e:
        return HttpResponse(f'Error generating PDF: {e}', status=500)

    finally:
        # Clean up temporary files
        if 'temp_html_file' in locals() and temp_html_file:
            temp_html_file.close()
            os.unlink(temp_html_file.name)
        if 'pdf_file' in locals() and os.path.exists(pdf_file):
            os.unlink(pdf_file)

