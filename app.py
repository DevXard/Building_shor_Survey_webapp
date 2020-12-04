from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
import surveys

call_survey = getattr(surveys, 'satisfaction_survey')

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONCES = []


@app.route('/')
def home_page():
    title = call_survey.title
    instructions = call_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/surve/<index>')
def survey_page(index):
    i = int(index)
    survey_test = call_survey.questions
    if len(RESPONCES) != i:
        flash("Please Do not skip Questions", 'error')
        return redirect(f"/surve/{len(RESPONCES)}")
    if len(RESPONCES) == i:
        return redirect('/thanks')
    
    
    return render_template('survey.html', surveys=survey_test, index=i)

@app.route('/thanks')
def thank_you_page():
    return render_template("thank_you.html")


@app.route('/awncers/<i>', methods=['POST'])
def awncers(i):
    awncer = request.form['awncer']
    RESPONCES.append(awncer)
    print(RESPONCES)

   
    if len(RESPONCES) == call_survey.questions:
        return redirect('/thanks')
    else:
        return redirect(f"/surve/{len(RESPONCES)}")
   