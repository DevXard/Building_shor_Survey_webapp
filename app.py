from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

call_survey = getattr(surveys, 'satisfaction_survey')

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONCES_key = 'responses'


@app.route('/')
def home_page():
    title = call_survey.title
    instructions = call_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/start', methods=['POST'])
def starting_survey():
    session[RESPONCES_key] = []
    
    return redirect('/surve/0')

@app.route('/surve/<index>')
def survey_page(index):
    i = int(index)
    responses = session.get(RESPONCES_key)
    survey_test = call_survey.questions
    print(responses)
    if responses is None:
        return redirect('/')
    if len(responses) == len(survey_test):
        return redirect('/thanks')
    if len(responses) != i:
        flash("Please Do not skip Questions", 'error')
        return redirect(f"/surve/{len(responses)}")
   
    
    
    return render_template('survey.html', surveys=survey_test, index=i)

@app.route('/thanks')
def thank_you_page():
    return render_template("thank_you.html")


@app.route('/awncers/<i>', methods=['POST'])
def awncers(i):
    print(session['awncers'])
    
    awncer = request.form['awncer']

    responses = session[RESPONCES_key]
    responses.append(awncer)
    session[RESPONCES_key] = responses
   
    if len(responses) == call_survey.questions:
        return redirect('/thanks')
    else:
        return redirect(f"/surve/{len(responses)}")
   