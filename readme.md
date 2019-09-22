<center> <h1>"RecFlix" - A Movie Recommendation System</h1> </center>

Project URL: http://gregrecflix.herokuapp.com

![Image of RecFlix](https://i.imgur.com/UgAF0em.jpg)

This project was based around a movie recommendation website idea. It uses a cosine similarity machine learning algorithm to suggest movies to users based on the genre of their selection. To keep the package lighter and minimize the information required to host the site, the flask app makes multiple calls to different tmdb api endpoints to get the box title images, movie poster images, trailer url, and movie descriptions (they weren't all available from one endpoint).

Example of API call:
```
url = []
tmdb = requests.get(f'https://api.themoviedb.org/3/movie/{j}?api_key={api_key}')
data = tmdb.json()
   if data.get("poster_path") != None:
      poster_path = data['poster_path']
      url.append("https://image.tmdb.org/t/p/original/" + poster_path)
```

To add additional useful functionality, I have implemented a search bar with an autocomplete feature to assist in movie selections. To expand on this, I have implemented 'fuzzy search' functionality to deliver close matches to search terms entered by the user and return them as suggestions on a search results page, while preventing crashes as a result of non-exact or misspelled titles.

Example of search code:
```
form = SearchForm(request.form)
if request.method == 'POST':
   form_cont = form.autocomp.data
   str2Match = form_cont
   strOptions = movie_list
   # String with the highest matching percentage
   highest = process.extractOne(str2Match,strOptions)
   fuzzyresult = highest[0]
   if form_cont == fuzzyresult:
      return redirect('../rec/' + fuzzyresult)
   else:
      return redirect('../results/' + form_cont)
```

![Image of RecFlix](https://i.imgur.com/ZkByD99.jpg)

![Image of RecFlix Search](https://i.imgur.com/Ykah7qM.jpg)


The ‘RECFLIX’ project utilizes the following languages/libraries:
<ul>
  <li>Python</li>
  <li>Flask</li>
  <li>scikit-learn</li>
  <li>fuzzywuzzy</li>
  <li>WTForms</li>
  <li>Requests</li>
  <li>Javascript / AJAX</li>
  <li>HTML / CSS / Bootstrap</li>
</ul>

Recent Additions:

<ul>
  <li>Modified the autocomplete to accept fuzzy words to prevent crashes.</li>
  <li>Created a primitive search engine within the site that displays close matches to the user's search entry.</li>
</ul>

Future plans include:

<ul>
  <li>Expand the functionality of the search feature to include movie descriptions.</li>
  <li>Implementing a second recommendation algorithm that analyzes keywords in the description of the selected movie to come up with recommendations in different genres.</li>
</ul>

Example:

The description for Hellraiser II:

"Doctor Channard is sent a new patient, a girl warning of the terrible creatures that have destroyed her family, Cenobites who offer the most intense sensations of pleasure and pain. But Channard has been searching for the doorway to Hell for years, and Kirsty must follow him to save her father and witness the power struggles among the newly damned."

The algorithm would parse the text and compare it to the description of all of the movies in the database, then return the most similar results. This would return a completely different set of results from the original algorithm, while theoretically returning accurate suggestions based on the user's movie preferences.
