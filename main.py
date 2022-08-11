from flask import *
import pickle
import re
from nltk.corpus import wordnet 
from nltk.stem import PorterStemmer,WordNetLemmatizer
from nltk.corpus import stopwords

#from flask_ngrok import run_with_ngrok




lemma = WordNetLemmatizer()

with open('static/model/news_sentiment_model.sav', 'rb') as file:
      
    # Call load method to deserialze
    model = pickle.load(file)

def cleanText(x):
    x= str(x).lower()
    x= re.findall('[a-z]+',x)
    x = [lemma.lemmatize(i,wordnet.VERB) for i in x if len(i) > 2 and i not in stopwords.words('english')]
    return " ".join(x)


#app =Flask(__name__)

app = Flask(__name__)
#run_with_ngrok(app)  # Start ngrok when app is run
#app = create_app(dev_config)
usernames = {}
usernames['qanit'] = 'qanit123'
usernames['dipti'] = 'dipto'
usernames['chinmay'] = 'chinmax'
usernames['admin'] = 'admin'
@app.route('/',methods = ['GET'])
def home():
	return render_template('home.html')

@app.route('/loginpage',methods =['POST','GET'])
def login():
	if request.method == 'POST':
		username = request.form.get('user')
		password = request.form.get('password')
		if username in list(usernames.keys()):
			if usernames[username] == password:
				return render_template('dashboard.html',user=username.title())
			else:
				return render_template('falselogin.html')
		else:
			return render_template('falselogin.html')
	elif request.method == 'GET':
		return redirect('/')


@app.route('/v1/sentiment/<news>',methods = ['POST','GET'])
def sentiment(news):
	senti = model.predict([cleanText(news)])
	if senti[0] == 0 : senti = 'Negative'
	else: senti = 'Positive' 
	return {'sentiment':senti}
if __name__ == '__main__':
	app.run()
