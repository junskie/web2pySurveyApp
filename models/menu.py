# -*- coding: utf-8 -*-



response.logo = A(B('Surveys'),XML('&trade;&nbsp;'),
                  _class="brand",_href="http://www.web2py.com/")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None


response.menu = [
    (T('All Surveys'), False, URL('default', 'index'), [])
]


if "auth" in locals(): auth.wikimenu()
