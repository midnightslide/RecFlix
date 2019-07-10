<center> <h1>"RecFlix"</h1> </center>

![Image of RecFlix](https://i.imgur.com/UgAF0em.jpg)

This project was based around a movie recommendation website idea. It uses a cosine similarity machine learning algorithm to suggest movies to users based on the genre of their selection. To keep the package lighter and minimize the information required to host the site, the flask app makes a call to the tmdb api to get the box title images, movie poster images, trailer url, and movie descriptions.

![Image of RecFlix](https://i.imgur.com/ZkByD99.jpg)

![Image of RecFlix Search](https://i.imgur.com/Ykah7qM.jpg)


The ‘RECFLIX’ project utilizes Python, Flask, HTML, CSS, and a small amount of Javascript/AJAX for the autocomplete search bar.

Future plans include deploying the website to heroku and setting up a PostgreSQL database with the information, modifying the autocomplete to accept fuzzy words and movie descriptions and limiting the results to a maximum of 10, and implementing a second recommendation algorithm that analyzes keywords in the description of the selected movie to come up with recommendations in different genres. 

Example:

The description for Hellraiser II:

"Doctor Channard is sent a new patient, a girl warning of the terrible creatures that have destroyed her family, Cenobites who offer the most intense sensations of pleasure and pain. But Channard has been searching for the doorway to Hell for years, and Kirsty must follow him to save her father and witness the power struggles among the newly damned."

The algorithm would parse the text and compare it to the description of all of the movies in the database, then return the most similar results. This would return a completely different set of results from the original algorithm, while theoretically returning accurate suggestions based on the user's movie preferences.
