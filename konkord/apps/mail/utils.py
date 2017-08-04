# coding: utf-8
import re
import smtplib
import urllib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from .models import MailTemplate
from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils.translation import get_language


def send_email(subject, text, to, html="", reply_email=''):
    from_email = settings.FROM_EMAIL

    mail = EmailMultiAlternatives(
        subject=subject, body=text, from_email=from_email, to=to)

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = from_email
    msgRoot['To'] = ', '.join(to)

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText(text.encode('UTF-8'), 'plain', 'UTF-8')
    msgAlternative.attach(msgText)

    links = re.compile("<img[^>]*\ssrc=\"(.*?)\"").findall(html)
    media_root = settings.MEDIA_ROOT
    static_root = settings.STATIC_ROOT
    for i, link in enumerate(links):
        try:
            name = 'image%s' % i
            html = html.replace(link, 'cid:%s' % name)
            link = urllib.parse.unquote(
                link)
            if '/media/' in link and not link.startswith('/media/'):
                link = '/media/' + link.split('/media/')[1]
            elif '/static/' in link and not link.startswith('/static/'):
                link = '/static/' + link.split('/static/')[1]
            if '/media/' in link:
                path = os.path.join(media_root, link.split('/media/')[-1])
            elif '/static/' in link:
                path = os.path.join(
                    static_root, link.split('/static/')[-1])
            fp = open(path, 'rb')
            msgImage = MIMEImage(fp.read(), _subtype=path.split('.')[-1])
            fp.close()

            msgImage.add_header('Content-ID', '<%s>' % name)
            msgRoot.attach(msgImage)
        except Exception as e:
            pass

    msgText = MIMEText(html.encode('UTF-8'), 'html', 'UTF-8')
    msgAlternative.attach(msgText)

    if to:
        try:
            use_gmail = getattr(settings, 'USE_GMAIL_SMTP', False)
            if use_gmail:
                smtp = smtplib.SMTP(settings.EMAIL_HOST)
                smtp.starttls()
            else:
                smtp = smtplib.SMTP()
                smtp.connect(settings.EMAIL_HOST)
            smtp.login(
                str(settings.EMAIL_HOST_USER),
                str(settings.EMAIL_HOST_PASSWORD)
            )
            smtp.sendmail(msgRoot['From'], to, msgRoot.as_string())
            smtp.quit()
        except:
            mail.attach_alternative(html, "text/html")
            mail.send(fail_silently=True)

def render(path, **params):
    """Looking for template in DB firstly, than looking for the
    template on disk.
    """
    name, file_type = path.split('/')[-1].split('.')
    site = Site.objects.get_current()
    site_url = f"{settings.SITE_PROTOCOL}://{site}"
    data = params
    language = get_language() or settings.LANGUAGE_CODE
    data.update({
        'shop_name': getattr(
            settings, 'SHOP_NAME_%s' % language.upper(), ""),
        'site': site,
        'site_url': site_url
    })
    try:
        mail_template = MailTemplate.objects.get(name=name)
        template = mail_template.html_template

        t = Template(template)
        data.update({
            'topic': mail_template.comment,
        })
        c = Context(data)
        return t.render(c)
    except MailTemplate.DoesNotExist:
        return render_to_string(path, data)
