# Hi!

In this repository I have attached all the codes along with pre-requisites that is required to make a real time twitter map,
that will take a keyword from you and display the tweets on a leaflet map on thier city level location.

You must create a seperate file, credentials.py and type in
API KEY = 'abcd..'
API_SECRET_KEY = 'abcd..'
ACCESS_TOKEN = 'abcd...'
ACCESS_TOKEN_SECRET ='abcd..'

and get these keys from your Twitter Developer profile.

Then you have to start the kafka server. Please follow the instructions in this playlist from video 1 to 6 - https://www.youtube.com/playlist?list=PL2UmzTIzxgL7Bq-mW--vtsM2YFF9GqhVB by Author - Code and Dogs

After that you can start the twitter.py file, which will stream tweets.

This stream, if the kafka server is done right, should be put directly into the kafka consumer.

Then we can start the frontend.py file which will start a localhost server, and you can open that server and see your live map.

Please keep in mind, the static and templates folders contain, the leafleft.js and index.html respectively, and you can if you wish, edit your webpage, add leafleft plugins, hotspot maps and so on.

# Thank you for reading!
