# -*- coding: utf-8 -*-

def index():
    db.survey.description.readable=False
    db.survey.choices.readable=False
    grid = SQLFORM.grid(db.survey,create=False,editable=False,deletable=False,details=True,csv=False,
                        links=[lambda row: A('take',_href=URL('take_survey',args=row.uuid),_class="btn"),
                               lambda row: A('results',_href=URL('see_results',args=row.uuid),_class="btn")])
    return locals()

@auth.requires_login()
def create_survey():
    def f(form):
        form.vars.results = [0]*len(request.vars.choices)
    from gluon.utils import web2py_uuid
    db.survey.uuid.default = uuid = web2py_uuid()
    form = SQLFORM(db.survey,submit_button='Create').process(onvalidation=f)
    if form.accepted:
        redirect(URL('take_survey',args=uuid))
    return locals()

@auth.requires_login()
def delete_survey():
    uuid = request.args(0)
    survey = db.survey(uuid=uuid) or redirect(URL('index'))
    if survey.created_by!=auth.user.id:
        session.flash = 'User not authorized'
        redirect(URL('index'))
    if survey.created_by==auth.user.id:
        db.execute('delete from survey where uuid=?',(uuid))
    return locals()

def take_survey():
    uuid = request.args(0)
    survey = db.survey(uuid=uuid) or redirect(URL('index'))
    if survey.requires_login:
        if not auth.user:
             redirect(URL('user/login',vars=dict(_next=URL(args=uuid))))
        vote = db.vote(survey=survey.id,created_by=auth.user.id)
        if vote:
             session.flash = 'You voted already!'
             redirect(URL('thank_you'))
    if request.post_vars:
         k = int(request.post_vars.choice)
         survey.results[k]+=1
         survey.update_record(results=survey.results)
         if survey.requires_login:
             db.vote.insert(survey=survey.id)
         redirect(URL('thank_you'))
    return locals()

@auth.requires_login()
def see_results():
    uuid = request.args(0)
    survey = db.survey(uuid=uuid) or redirect(URL('index'))
    return locals()

def thank_you():
    return dict()

def user():
    return dict(form=auth())


@cache.action()
def download():
    return response.download(request, db)


def call():
    return service()


@auth.requires_signature()
def data():
    return dict(form=crud())
