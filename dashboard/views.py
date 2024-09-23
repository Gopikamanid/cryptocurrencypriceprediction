from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import statsmodels.api as sm
from django.shortcuts import render
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from plotly.offline import plot
from django.contrib.auth.models import User
from django.contrib import messages
from .models import coins
# Create your views here.
def home(request):
	#Crypto news
	api_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
	api = json.loads(api_request.content)
	#Crypto Price
	price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,XRP,ETH,BCH,EOS,LTS,LINK,BNB,TRX,ETC&tsyms=USD")
	price = json.loads(price_request.content)

	context={
	'api':api,
	'price':price
	}
	return render(request,'dashboard/home.html',context)
def details(request):
    data=request.POST.get('data')
    
    value=coins.objects.filter(name=data)
    print(value)
    return render(request,'dashboard/details.html',{'value':value})
def prices(request):
	quote=''
	pred=["0"]
	crypto=''
	history=''
	data=''
	plot_div=''
	count=0
	high=[] #The list that contains the average price of the crypto for the past 60 days
	if request.method=="POST":
		quote = request.POST['search2']
		quote = quote.upper()
		#Crypto Price
		crypto_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + quote + "&tsyms=USD")
		crypto = json.loads(crypto_request.content)
		#Crypto Historical Data
		history_request = requests.get("https://min-api.cryptocompare.com/data/v2/histoday?fsym=" + quote + "&tsym=USD&limit=2000")
		history = json.loads(history_request.content)
		print(history,'data')
		try:
			data = history['Data']['Data']

			for i in data:
				high.append((int(i['high']) + int(i['low']))/2)
				high = high[-60:]
			pred = train(high)
			x = np.linspace(0, 60,60)
			fig = go.Figure(data=go.Scatter(x=x, y=high))
			plot_div = plot(fig, output_type='div', include_plotlyjs=False)
		except:
			pass
	context={
	'quote':quote,
	'crypto':crypto,
	'history':history,
	'data':high,
	'plot':plot_div,
	'pred':int(pred[0]),
	}
	return render(request,'dashboard/prices.html',context)

def home1(request):
    return render(request,'dashboard/main.html')
def login(request):
    return render(request,'dashboard/login.html')
def register(request):
    return render(request,'dashboard/register.html')

def predict(request):
    return render(request,'dashboard\predict.html')

def emailverify(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            User.objects.get(email=email,password=password)
            return render(request,'dashboard/pricesearch.html')
        except:
            messages.info(request,'email or password incorrect')
            return render(request,'dashboard/predict.html')
    else:
        return render(request,'dashboard/predict.html')
     

def register1(request):

    if request.method == 'POST':
        
        username=request.POST.get('username')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email alredy exsist')
                return render(request,'dashboard/register.html')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'username alredy exsist')
                return render(request,'dashboard/register.html')
            else:
                user=User.objects.create(first_name=firstname,last_name=lastname,username=username,email=email,password=password1)
                user.save()
                return render(request,'dashboard/login.html')
        messages.info(request,'password dose not match ')
        return render(request,'dashboard/register.html')

    else:
        return render(request,'dashboard/register.html')

def login1(request):
	if request.method == 'POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		try:
			User.objects.get(username=username,password=password)

			value=request.POST.get('username')
			api_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
			api = json.loads(api_request.content)
			#Crypto Price
			price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,XRP,ETH,BCH,EOS,LTS,LINK,BNB,TRX,ETC&tsyms=USD")
			price = json.loads(price_request.content)

			context={
			'api':api,
			'price':price
			}
			return render(request,'dashboard/home.html',context)
		except:
			messages.info(request,'username or password incorrect')
			return render(request,'dashboard/login.html')
	else:
		return render(request,'dashboard/login.html')

def train(data):
	model = ExponentialSmoothing(np.asarray(data) ,seasonal_periods=7 ,trend='add', seasonal='add').fit()
	pred = model.forecast(1)
	return pred