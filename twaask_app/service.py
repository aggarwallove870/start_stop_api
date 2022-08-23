from django.conf import settings
import os,errno
from django.core.mail import EmailMultiAlternatives
from weasyprint import  HTML


def create_pdf(html,filename,pdf_folder):
    media = settings.MEDIA_ROOT + pdf_folder

    if not os.path.exists(os.path.dirname(media)):  # create directory if not exists
        try:
            os.makedirs(os.path.dirname(media))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    path = media+filename
    response = HTML(string=html, base_url=__file__).write_pdf(path)
    return response

def send_mail(filename,client_email,pdf_folder):
    subject, from_email, to = 'Snake Script Solution', 'gaurav@snakescript.com', client_email
    text_content = 'This is an important message for you.'
    html_content = '<p>Your buy pachage from Snake script pvt. ltd. full detail of puchasing in attach document.</p>'
    sent_mail(subject, text_content, from_email, to,html_content,filename,pdf_folder)
    A_subject, A_to = 'Purchage Package', 'sawan@snakescript.com'
    A_text_content = 'This is an important message for you.'
    A_html_content = '<p>Client perchage pachage please revert to client.</p>'
    sent_mail(A_subject,A_text_content, from_email, A_to,A_html_content,filename,pdf_folder)


def sent_mail(subject, text_content, from_email, to,html_content,filename,pdf_folder):
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.attach_file('media/'+pdf_folder+filename)
    msg.send()