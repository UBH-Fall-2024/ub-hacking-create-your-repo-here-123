from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
import os
import json


def save_resume(request):
    if request.method == 'POST':
        file_name = request.POST.get('file_name')
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            upload_dir = os.path.join(settings.MEDIA_ROOT, f'docs/users')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            fs = FileSystemStorage(location=upload_dir)
            saved_file_name = file_name if file_name else uploaded_file.name
            saved_file_path = fs.save(saved_file_name, uploaded_file)

            return JsonResponse({'message': 'File uploaded successfully!'})

        return JsonResponse({'error': 'No file uploaded'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def send_bulk_emails(request):
    if request.method == 'POST':
        data = request.POST.get('data')

        if not data:
            return JsonResponse({'error': 'No data provided'}, status=400)

        name = request.user.first_name + " " + request.user.last_name
        sender_email = request.user.email
        designation = request.POST.get('designation')
        company_name = request.POST.get('company_name')

        # Check if required details (designation, company name) are present
        if not designation or not company_name:
            return JsonResponse({'error': 'Missing designation or company name'}, status=400)

        try:
            # Use json.loads instead of eval for security reasons
            emails_data = json.loads(data)
            if not isinstance(emails_data, list):
                return JsonResponse({'error': 'Invalid data format'}, status=400)

            # Prepare the list of email messages
            emails = []
            for email_data in emails_data:
                email = email_data.get('email')
                body = email_data.get('body')
                
                if email and body:
                    subject = f"[{name}]: Exploring {designation} Roles at {company_name}"
                    emails.append((subject, body, sender_email, [email]))
                else:
                    return JsonResponse({'error': 'Missing email or body in data'}, status=400)

            # Send the bulk emails using send_mass_mail
            send_mail(
                subject=subject,
                message=body,
                from_email=sender_email,
                recipient_list=[email],
            )

            return JsonResponse({'message': 'Emails sent successfully!'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format in data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error processing data: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
