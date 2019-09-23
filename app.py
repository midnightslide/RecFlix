from flask import Flask, jsonify, Response, render_template, request, redirect, url_for
import json
from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, SubmitField, validators
from engine import *
from fuzzywuzzy import process
import requests
from api_key import api_key

app = Flask(__name__)
app.static_folder = 'static'

# CREATE A GENERIC SECRET KEY BECAUSE THE FORM REQUIRES IT FOR VALIDATION AND WE WON'T BE NEEDING ANYTHING SECURE FOR OUR PURPOSES
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

# COMPILES A LIST OF MOVIE TITLES TO BE PASSED INTO THE AUTOCOMPLETE FORM
movie_list = movies['title'].tolist()

# INDEX ROUTE - SELECTS 6 MOVIES AT RANDOM FROM MOVIES DF AND DISPLAYS THEM ON THE PAGE AS A STARTING POINT
# ALSO LISTENS FOR THE POST FROM THE AUTOCOMPLETE FORM AND ROUTES THE FORM SUBMISSION TO THE REC ROUTE
@app.route("/", methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    if request.method == 'POST':
        form_cont = form.autocomp.data
        str2Match = form_cont
        strOptions = movie_list
        # GET THE STRING WITH THE HIGHEST MATCHING PERCENTAGE
        highest = process.extractOne(str2Match,strOptions)
        fuzzyresult = highest[0]
        # IF THE STRING IS AN EXACT MATCH, THERE IS NO NEED TO GO TO THE SEARCH PAGE. 
        if form_cont == fuzzyresult:
            return redirect('../rec/' + fuzzyresult)
        else:
            return redirect('../results/' + form_cont)
    # CREATE A DATAFRAME WITH 8 RANDOM MOVIES FROM OUR DATABASE
    rando_df = movies.sample(8)
    title2 = []
    url = []
    y = 0
    for x in rando_df.title:
        title2.append(x)
    while y < 6:
        j = rando_df.tmdbId.iloc[y]
        tmdb = requests.get(f'https://api.themoviedb.org/3/movie/{j}?api_key={api_key}')
        data = tmdb.json()
        if data.get("poster_path") != None:
            poster_path = data['poster_path']
            url.append("https://image.tmdb.org/t/p/original/" + poster_path)
            y += 1
        else:
            pass
    return render_template('index.html', title2=title2, url=url, form=form)

@app.route("/results/<title>", methods=['GET', 'POST'])
def searchResults(title):
    form = SearchForm(request.form)
    if request.method == 'POST':
        form_cont = form.autocomp.data
        str2Match = form_cont
        strOptions = movie_list
        Ratios = process.extract(str2Match,strOptions)
        highest = process.extractOne(str2Match,strOptions)
        fuzzyresult = highest[0]
        if form_cont == fuzzyresult:
            return redirect('../rec/' + fuzzyresult)
        else:
            return redirect('../results/' + form_cont)
    resultString = title
    resultOptions = movie_list
    Ratios = process.extract(resultString,resultOptions)
    resultList = []
    matchPer = []
    # EXTRACT THE MOVIE TITLES AND MATCH ACCURACY FROM OUR FUZZY SEARCH RESULTS
    for x in range(len(Ratios)):
        resultList.append(Ratios[x][0])
        matchPer.append(Ratios[x][1])
    movieURL = []
    # CREATE A LIST OF LINKS FOR OUR RESULTS
    for x in resultList:
        movieURL.append("http://gregrecflix.herokuapp.com/rec/" + x)
    resultPosters = []
    resultDescription = []
    for x in resultList:
        # IDENTIFY THE TITLE THAT WAS PASSED IN
        titleloc = movies.loc[movies['title'] == x]
        # GET THE DESCRIPTION OF THE MOVIE THAT WAS PASSED IN
        desc_index = titleloc['tmdbId'].iloc[0]
        resultPosters.append("https://image.tmdb.org/t/p/original/" + titleloc['poster_path'].iloc[0])
        tmdb_desc = requests.get(f'https://api.themoviedb.org/3/movie/{desc_index}?api_key={api_key}')
        desc_data = tmdb_desc.json()
        if desc_data.get("overview") != None:
            resultDescription.append(desc_data['overview'])
        else:
            pass   
    return render_template('results.html', title=title, resultString=resultString, resultList=resultList, resultPosters=resultPosters, resultDescription=resultDescription, form=form)


@app.route("/rec/<title>", methods=['GET', 'POST'])
def movie_bot_final(title):
    form = SearchForm(request.form)
    # IDENTIFY THE TITLE THAT WAS PASSED IN
    titleloc = movies.loc[movies['title'] == title]
    # GET THE DESCRIPTION OF THE MOVIE THAT WAS PASSED IN
    desc_index = titleloc['tmdbId'].iloc[0]
    tmdb_desc = requests.get(f'https://api.themoviedb.org/3/movie/{desc_index}?api_key={api_key}')
    desc_data = tmdb_desc.json()
    if desc_data.get("overview") != None:
        description = desc_data['overview']
    else:
        pass
    # GET THE YOUTUBE TRAILER LINK FOR THE ID THAT WAS PASSED IN
    tmdb_trailer = requests.get(f'https://api.themoviedb.org/3/movie/{desc_index}/videos?api_key={api_key}')
    trailer_data = tmdb_trailer.json()['results'][0]
    if trailer_data.get('key') != None:
        trailer_path = trailer_data['key']
        trailer_url = ("https://www.youtube.com/watch?v=" + trailer_path)
    else:
        pass
    # FORM SUBMISSION
    if request.method == 'POST':
        form_cont = form.autocomp.data
        str2Match = form_cont
        strOptions = movie_list
        Ratios = process.extract(str2Match,strOptions)
        highest = process.extractOne(str2Match,strOptions)
        fuzzyresult = highest[0]
        if form_cont == fuzzyresult:
            return redirect('../rec/' + fuzzyresult)
        else:
            return redirect('../results/' + form_cont)
    # ML BASED ON THE MOVIE GENRE
    titles = movies['title']
    indices = pd.Series(movies.index, index=movies['title'])
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    movie_indices = [i[0] for i in sim_scores]
    # TAKES THE 12 MOST SIMILAR MOVIES TO THE TITLE MOVIE INPUT
    mv = titles.iloc[movie_indices].head(12).to_frame()
    cols = ['title']
    temp_df = mv.join(movies.set_index(cols), on=cols)
    moviename = []
    url1 = []
    # PULLS THE IMAGE URL FROM THE MOVIES DF AND APPENDS THEM TO THE URL PREFIX FOR THE MOVIE POSTERS
    # PASSES THE MOVIE POSTER URL INTO THE RECS.HTML PAGE
    titleurl = ("https://image.tmdb.org/t/p/original/" + titleloc['poster_path'].iloc[0])
    bgurl = ("https://image.tmdb.org/t/p/original/" + desc_data['backdrop_path'])
    runtime = str(desc_data['runtime'])
    for film in temp_df.title:
        moviename.append(film)
    for poster in temp_df.poster_path:
        url1.append("http://image.tmdb.org/t/p/w185" + str(poster))
    return render_template('recs.html', moviename=moviename, url1=url1, title=title, titleurl=titleurl, bgurl=bgurl, form=form, description=description, runtime=runtime, trailer_url=trailer_url)

# SETS UP THE FORM WITH THE AUTOCOMP TEXT FIELD AND SUBMISSION BUTTON
class SearchForm(Form):
    autocomp = TextField('Enter Movie Title', id='movie_autocomplete')
    submit = SubmitField('Search')

# THE BRAINS OF THE AUTOCOMPLETE. PULLS THE MOVIES FROM THE LIST VARIABLE AND RETURNS A JSON THAT CAN BE PARSED BY THE JQUERY ON THE HTML PAGE
@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(movie_list), mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True)