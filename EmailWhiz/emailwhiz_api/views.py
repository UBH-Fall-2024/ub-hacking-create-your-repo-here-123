from django.shortcuts import render
from django.http import HttpResponse
from PyPDF2 import PdfReader
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import ResumeSelectionForm, TemplateSelectionForm
import os

import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage


genai.configure(api_key='AIzaSyDwBGdGTwqP05cx5GdvuQeZ-F9whEQr1uA')

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)


def get_template(details):
    template = '''Giving you my text of resume.\n
    {resume} 
    \n
    \n
    I want you to provide me a cold email template mail which I can send to a recruiter.\n
    For that try to extract details from specific sections of Resume Text  & it should include the following.\n
    \n
    1. Extract Skills - Use it in creating template in a separate paragraph.\n
    2. Template should contain information from work experience as well in a separate paragraph.\n
    3. Template should include why you are a good fit for the particular role.\n
    4. Use internet and search the internet about the company and add in the template (40 words) that why the candidate is inspired by the company's info in a separate paragraph.\n
    5. Add pursuing a degree if graduation done is False, else write completed  graduation: True.\n
    6. Don't include where I find the opportunity.\n
    7. The template should not contain [....] like thing. If possible search on internet.\n
    \n
    Also use the below critical information:\n
    \n
    1.First name of user: {first_name}\n 
    2. Last Name of user: {last_name}\n 
    3. University: {university}\n
    4. Target Company: {target_company}\n 
    5. Target role: {target_role}\n 
    6. Email: {email}\n
    7. Linkedln Profile: {linkedin_url}\n 
    8. Phone Number: {phone}\n
    9. Recruiter Name: {senders_name}\n
    10. Graduation Done: {graduation_complete_boolean}\n
    11. Degree Name: {degree_name}\n
    \n
    \n
    I just want the body of the generated email template in response from your side as I want to use this in an API, so please give me only the body (without subject) in HTML. Please make sure to stick to the first 7 points & use the information from the critical information.'''

    return template.format(
    resume=details["resume"],
    first_name=details['first_name'],
    last_name=details["last_name"],
   university=details["university"],
    target_company=details['target_company'],
    target_role=details["target_role"],
    email=details["email"],
    linkedin_url=details['linkedin_url'],
    phone=details["phone"],
    senders_name=details["senders_name"],
    graduation_complete_boolean=details['graduation_complete_boolean'],
    degree_name=details["degree_name"])








def save_resume(request):
    if request.method == 'POST':
        file_name = request.POST.get('file_name')
        uploaded_file = request.FILES.get('file')
        details= {}
        details['email'] = 'bhuvanthirwani@gmail.com'
        if uploaded_file:
            upload_dir = os.path.join(settings.MEDIA_ROOT, f'{details["email"]}/resumes')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            fs = FileSystemStorage(location=upload_dir)
            saved_file_name = file_name if file_name else uploaded_file.name
            saved_file_path = fs.save(f'{saved_file_name}.pdf', uploaded_file)

            return  render(request, 'base.html')

        return JsonResponse({'error': 'No file uploaded'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)



def list_resumes(request, user):
    print("G1")
    user_resumes = os.listdir(f"/users/{user}/resumes")
    if request.method == "POST":
        form = ResumeSelectionForm(request.POST, user_resumes=user_resumes)
        if form.is_valid():
            selected_resume = form.cleaned_data['resume']
            request.session['selected_resume'] = selected_resume  # Store selection in session
            return redirect('select_template', user=user)
    else:
        form = ResumeSelectionForm(user_resumes=user_resumes)
    return render(request, 'myapp/list_resumes.html', {'form': form})

# def select_template(request, user):
#     email_type = request.POST.get("template_type", "")
#     user_templates = os.listdir(f"/users/{user}/templates/{email_type}")
#     if request.method == "POST":
#         form = TemplateSelectionForm(request.POST, templates=user_templates)
#         if form.is_valid():
#             if form.cleaned_data['use_gemini']:
#                 # Call Gemini API here and save template choice
#                 pass
#             else:
#                 selected_template = form.cleaned_data['template_choice']
#                 request.session['selected_template'] = selected_template
#             return redirect('upload_excel', user=user)
#     else:
#         form = TemplateSelectionForm(templates=user_templates)
#     return render(request, 'myapp/select_template.html', {'form': form})


def upload_excel(request, user):
    if request.method == "POST":
        excel_file = request.FILES['excel']
        # Process Excel data and render table
        request.session['excel_data'] = ...  # Save processed data in session for preview
        return redirect('preview_template', user=user)
    return render(request, 'myapp/upload_excel.html')

def preview_template(request, user):
    selected_resume = request.session.get('selected_resume')
    selected_template = request.session.get('selected_template')
    excel_data = request.session.get('excel_data')
    if request.method == "POST":
        # Send the email here
        return redirect('success_page')
    return render(request, 'myapp/preview_template.html', {
        'resume': selected_resume,
        'template': selected_template,
        'excel_data': excel_data,
    })

def generate_template(request):
    if request.method == 'POST':
        user_email = 'bhuvanthirwani@gmail.com'  # Replace with actual user logic
        selected_resume = request.POST.get('selected_resume')
        
        resume_path = os.path.join(settings.MEDIA_ROOT, user_email, 'resumes', selected_resume)
        print("Resume_PATH: ", resume_path)
        # Extract text from the selected resume
        extracted_text = extract_text_from_pdf(resume_path)
        print("extracted_text: ", extracted_text)
        # Create prompt for Gemini
        details = {}
        details['resume'] = extracted_text
        prompt = get_template(details)
        
        # Call Gemini API
        response = call_gemini_api(prompt)
        print("Response: ", response)
        if response:
            template_text = response.text
            return render(request, 'generated_template.html', {'template_text': template_text})
        else:
            return render(request, 'generated_template.html', {'error': "Failed to generate template."})
    else:
        return redirect('list_resumes')

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    

    return text

def call_gemini_api(prompt):
    # url = "https://gemini-api-url.com/generate"  # Replace with actual Gemini API endpoint
    # headers = {"Authorization": "Bearer your_gemini_api_key", "Content-Type": "application/json"}
    # data = {"prompt": prompt}
    # return requests.post(url, json=data, headers=headers)

    chat_session = model.start_chat(
    history=[
    ]
    )

    response = chat_session.send_message(prompt)
    return response

def send_email(request):
    return "Mail Sent"

