from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'greentreemonitor1357'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

global survey_complete
survey_complete = False
SURVEY = satisfaction_survey
RESPONSES  = []

@app.after_request
def after_request(response):
    """
    Prevents cached responses from the server
    https://stackoverflow.com/questions/47376744/how-to-prevent-cached-response-flask-server-using-chrome
    """
    response.headers["Cache-Control"] = "public no-cache, no-store, must-revalidate, max-age=0, post-check=0, pre-check=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = 0
    return response

@app.route('/')
def home_page():
    # app.logger.info('RESPONSES length: %s', len(RESPONSES))
    return render_template('home.html', survey=SURVEY)

@app.route('/start-survey', methods=['POST'])
def start_survey():
    session['responses'] = []
    return redirect('/questions/0')


@app.route('/questions/<int:num>', methods=['GET'])
def question_page(num):
    #################################
    questions = SURVEY.questions
    responses_length = len(RESPONSES)
    questions_length = (len(list(SURVEY.questions)))
    #################################
    global survey_complete
    if(survey_complete):
        return redirect('/thankyou')
    if(num != responses_length):
        flash('Page redirected: Attempt to access an invalid question')
        return redirect(f'/questions/{responses_length}')
    if(responses_length == questions_length and num == questions_length):
        survey_complete = True
        return redirect('/thankyou')
    return render_template('questions.html', questions=questions, num=num)

@app.route('/answer', methods=['POST'])
def answer():
    #################################
    form_question = request.form['question']
    num = int(form_question[0])
    choice = SURVEY.questions[int(form_question[0])].choices[int(form_question[-1])]
    #################################
    # import pdb;  pdb.set_trace()
    #################################
    RESPONSES.append(choice)
    _responses = session['responses']
    _responses.append(choice)
    session['responses'] = _responses
    return redirect(f'/questions/{num+1}')

@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html', survey=SURVEY)