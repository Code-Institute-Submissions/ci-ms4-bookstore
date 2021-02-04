from django import template
from home.forms import NewsForm, MailForm

register = template.Library()

@register.inclusion_tag('_inc_news_form.html')
def load_newsform():    
    return {'news_form': NewsForm()}

@register.inclusion_tag('_inc_footer.html')
def load_footer():    
    return {'mail_form': MailForm()}