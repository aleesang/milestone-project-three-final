import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv('.env')
from flask_share import Share
share = Share()

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'Music_Library'
app.config["MONGO_URI"] = os.getenv('DATABASE_URL')

mongo = PyMongo(app)

# for sharing on socials on view song page
share.init_app(app)

# routes to home page where all genres are displayed
@app.route('/')
def home():
    return render_template('home.html')
    
    
# routes songs to "country" genre
@app.route('/get_country')
def get_country():
    return render_template('country.html', 
                           # sorts songs in genre by artist name
                           songs=mongo.db.songs.find({"genre_name":"Country"}).sort("artist_name"))
    
    
# routes songs to "chill" genre
@app.route('/get_chill')
def get_chill():
    return render_template('chill.html', 
                           # sorts songs in genre by artist name
                           songs=mongo.db.songs.find({"genre_name":"Chill"}).sort("artist_name"))


# routes songs to "folk" genre
@app.route('/get_folk')
def get_folk():
    return render_template('folk.html', 
                           # sorts songs in genre by artist name
                           songs=mongo.db.songs.find({"genre_name":"Folk"}).sort("artist_name"))


# routes songs to "pop" genre 
@app.route('/get_pop')
def get_pop():
    return render_template('pop.html', 
                           # sorts songs in genre by artist name
                           songs=mongo.db.songs.find({"genre_name":"Pop"}).sort("artist_name"))


# routes songs to "rock" genre 
@app.route('/get_rock')
def get_rock():
    return render_template('rock.html', 
                           # sorts songs in genre by artist name
                           songs=mongo.db.songs.find({"genre_name":"Rock"}).sort("artist_name"))
 
 
# routes songs to "reggae" genre 
@app.route('/get_reggae')
def get_reggae():
    return render_template('reggae.html', 
                           # sorts songs in genre by artist name
                           songs=mongo.db.songs.find({"genre_name":"Reggae"}).sort("artist_name"))


# routes songs to "urban" genre 
@app.route('/get_urban')
def get_urban():
    return render_template('urban.html', 
                           # sorts songs in genre by artist name
                           songs=mongo.db.songs.find({"genre_name":"Urban"}).sort("artist_name"))


# routes songs to "other" genre 
@app.route('/get_other')
def get_other():
    return render_template('other.html', 
                           # sorts songs in genre by artist name
                           songs=mongo.db.songs.find({"genre_name":"Other"}).sort("artist_name"))
           
              
# routes page to all songs in database    
@app.route('/get_songs')
def get_songs():
    return render_template('allsongs.html', 
                           # sort list to last inserted doc so users can find their song in list easily
                           songs=mongo.db.songs.find().sort("_id", -1))
                           
                           
# routes to view song info
@app.route("/show_song/<song_id>")
def show_song(song_id):
        the_song = mongo.db.songs.find_one({"_id": ObjectId(song_id)})
        all_genres = mongo.db.genre.find()
        return render_template('showsong.html', song=the_song, genres=all_genres)
    

# page to add a new song
@app.route('/add_song')
def add_song():
    return render_template('addsong.html',
                           song=mongo.db.songs.find(),
                           genres=mongo.db.genre.find())   


# inserts new song
@app.route('/insert_song', methods=['GET', 'POST'])
def insert_song():
    songs =  mongo.db.songs
    songs.insert_one(request.form.to_dict())
    return redirect(url_for('get_songs'))


# page to edit song
@app.route('/edit_song/<song_id>', methods=['GET', 'POST'])
def edit_song(song_id):
    the_song =  mongo.db.songs.find_one({"_id": ObjectId(song_id)})
    all_genres =  mongo.db.genre.find()
    return render_template('editsongs.html', song=the_song, genres=all_genres)


# updates song after user saves changes from edit and redirects to "all songs" page
@app.route('/update_song/<song_id>', methods=['POST'])
def update_song(song_id):
    songid = song_id
    songs = mongo.db.songs
    songs.update( 
    {'_id': ObjectId(song_id)},
    {
        'genre_name':request.form.get('genre_name'),
        'song_image':request.form.get('song_image'),
        'album_name':request.form.get('album_name'),
        'song_name':request.form.get('song_name'),
        'artist_name':request.form.get('artist_name'),
        'song_link':request.form.get('song_link'),
    })
    return redirect(url_for('get_songs'))


# removes song after user clicks delete
@app.route('/delete_song/<song_id>', methods=['POST'])
def delete_song(song_id):
    mongo.db.songs.remove({'_id': ObjectId(song_id)})
    return redirect(url_for('get_songs'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 4444)),
            debug=False)