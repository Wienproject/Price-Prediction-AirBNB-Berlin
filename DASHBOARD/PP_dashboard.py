from flask import Flask, render_template, request
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
import joblib

PP = pd.read_csv('./static/final10.csv')
app = Flask(__name__)


def category_plot(
	cat_plot = 'histplot',
	cat_x = 'neighbourhood_group', cat_y = 'price',
	estimator = 'avg', hue = 'room_type'):


	if cat_plot == 'histplot':

		data = []

		for val in PP[hue].unique():
			hist = go.Histogram(
				x=PP[PP[hue]==val][cat_x],
				y=PP[PP[hue]==val][cat_y],
				histfunc=estimator,
				name=val
			)

			data.append(hist)

		title='Count Plot'
	elif cat_plot == 'boxplot':
		data = []

		for val in PP[hue].unique():
			box = go.Box(
				x=PP[PP[hue] == val][cat_x], #series
				y=PP[PP[hue] == val][cat_y],
				name = val
			)
			data.append(box)
		title='Box'

	if cat_plot == 'histplot':
		layout = go.Layout(
			title=title,
			xaxis=dict(title=cat_x),

			boxmode = 'group'
		)
	else:
		layout = go.Layout(
			title=title,
			xaxis=dict(title=cat_x),
			yaxis=dict(title=cat_y),

		)
	#simpan config plot dan layout pada dictionary
	result = {'data': data, 'layout': layout}

	#json.dumps akan mengenerate plot dan menyimpan hasilnya pada graphjson
	graphJSON = json.dumps(result, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON


#1 Home/index
@app.route('/')
def index():
	plot = category_plot()

	list_plot = [('histplot', 'Count Plot'), ('boxplot', 'Box Plot')]
	list_x = [('room_type', 'room_type'),('neighbourhood_group', 'District')]
	list_y = [('price', ' price'), ('bathrooms', 'bathrooms'),('bedrooms', 'bedrooms'),('beds', 'beds')]
	list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
	list_hue = [('instant_bookable','Instant Booking'), ('room_type', 'Room Type'), 
	('neighbourhood_group', 'District')]

	return render_template('category1.html', plot = plot, focus_plot = 'histplot', focus_x = 'neighbourhood_group', focus_estimator = 'count', focus_hue = 'room_type', drop_plot = list_plot, drop_x = list_x, drop_y = list_y, drop_estimator = list_est, drop_hue = list_hue)

#2. Visualisasi (menampilkan plot)
@app.route('/cat_fn/<nav>')
def cat_fn(nav):

	
	if nav == 'True':
		cat_plot = 'histplot'
		cat_x = 'neighbourhood_group'
		cat_y = 'price'
		estimator = 'avg'
		hue = 'bedrooms'
	
	
	else:
		cat_plot = request.args.get('cat_plot')
		cat_x = request.args.get('cat_x')
		cat_y = request.args.get('cat_y')
		estimator = request.args.get('estimator')
		hue = request.args.get('hue')

	
	if estimator == None:
		estimator = 'count'
	
	
	if cat_y == None:
		cat_y = 'price'

	# Dropdown menu
	list_plot = [('histplot', 'Count Plot'), ('boxplot', 'Box Plot')]
	list_x = [('room_type', 'room_type'),('neighbourhood_group', 'District')]
	list_y = [('price', ' price'), ('bathrooms', 'bathrooms'),('bedrooms', 'bedrooms'),('beds', 'beds')]
	list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
	list_hue = [('instant_bookable','Instant Booking'), ('room_type', 'Room Type'), 
	('neighbourhood_group', 'District')]
	plot = category_plot(cat_plot, cat_x, cat_y, estimator, hue)
	
	return render_template('category.html',plot=plot,focus_plot='histplot',focus_x='loan_status',focus_estimator='count',focus_hue='loan_status',drop_plot=list_plot,drop_x=list_x,drop_y=list_y,drop_estimator=list_est,drop_hue=list_hue)

#3 DATASET + PREDICTING
@app.route('/predict')
def prediction():
	PP1 = pd.read_csv("./static/data_predict.csv").head(100)
	PP1.index.name = None
	titles = " "
	
	# data.to_html()
	return render_template('predict.html', tables = [PP.to_html(classes = 'data', header = 'true')], titles = titles)


#4 RESULT
@app.route('/result', methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		input = request.form

		host_response_rate = int(input['host_response_rate'])
		availability_365 = int(input['availability_365'])
		accommodates = int(input['accommodates'])
		bedrooms = float(input['bedrooms'])
		beds = int(input['beds'])
		minimum_nights = int(input['minimum_nights'])
		review_scores_rating = int(input['review_scores_rating'])
		amenities = int(input['amenities'])
		calculated_host_listings_count = int(input['calculated_host_listings_count'])
		bathrooms = float(input['bathrooms'])
		instant_bookable_encode = int(input['instant_bookable_encode'])
		host_is_superhost_encode = int(input['host_is_superhost_encode'])
		room_type = (input['room_type'])
		property_type = (input['property_type'])
		neighbourhood_group =(input['neighbourhood_group'])


		if neighbourhood_group == 'Charlottenburg-Wilm.':
			ng=[1,0,0,0,0,0,0,0,0,0,0,0]
		elif neighbourhood_group == 'Friedrichshain-Kreuzberg':
			ng=[0,1,0,0,0,0,0,0,0,0,0,0]
		elif neighbourhood_group == 'Lichtenberg':
			ng=[0,0,1,0,0,0,0,0,0,0,0,0]
		elif neighbourhood_group == 'Marzahn - Hellersdorf':
			ng=[0,0,0,1,0,0,0,0,0,0,0,0]
		elif neighbourhood_group == 'Mitte':
			ng=[0,0,0,0,1,0,0,0,0,0,0,0]
		elif neighbourhood_group == 'Neukölln':
			ng=[0,0,0,0,0,1,0,0,0,0,0,0]
		elif neighbourhood_group == 'Pankow':
			ng=[0,0,0,0,0,0,1,0,0,0,0,0]
		elif neighbourhood_group == 'Reinickendorf':
			ng=[0,0,0,0,0,0,0,1,0,0,0,0]
		elif neighbourhood_group == 'Spandau':
			ng=[0,0,0,0,0,0,0,0,1,0,0,0]
		elif neighbourhood_group == 'Steglitz - Zehlendorf':
			ng=[0,0,0,0,0,0,0,0,0,1,0,0]
		elif neighbourhood_group == 'Tempelhof - Schöneberg':
			ng=[0,0,0,0,0,0,0,0,0,0,1,0]
		elif neighbourhood_group == 'Treptow - Köpenick':
			ng=[0,0,0,0,0,0,0,0,0,0,0,1]

		if room_type == 'Entire home/apt':
			rty=[1,0,0,0]
		elif room_type == 'Hotel room':
			rty=[0,1,0,0]
		elif room_type == 'Private room':
			rty=[0,0,1,0]
		elif room_type == 'Shared room':
			rty=[0,0,0,1]

		if property_type == 'Entire property':
			pty=[1,0,0,0]
		elif property_type == 'Other':
			pty=[0,1,0,0]
		elif property_type == 'Private room':
			pty=[0,0,1,0]
		elif property_type == 'Shared room':
			pty=[0,0,0,1]



		data_pred = pd.DataFrame(data =[[host_response_rate, availability_365, accommodates,bedrooms, beds,minimum_nights,review_scores_rating, amenities,
										 calculated_host_listings_count,bathrooms,instant_bookable_encode,host_is_superhost_encode,
										 ng[0],ng[1],ng[2],ng[3],ng[4],ng[5],ng[6],ng[7],ng[8],ng[9],ng[10],ng[11],
										 rty[0],rty[1],rty[2],rty[3],
										 pty[0],pty[1],pty[2],pty[3]]],
								columns= ['host_response_rate', 'availability_365', 'accommodates', 'bedrooms','beds', 'minimum_nights', 'review_scores_rating', 'amenities',
	   									'calculated_host_listings_count', 'bathrooms','instant_bookable_encode', 'host_is_superhost_encode',
										'neighbourhood_group_Charlottenburg-Wilm.',
										'neighbourhood_group_Friedrichshain-Kreuzberg',
										'neighbourhood_group_Lichtenberg',
										'neighbourhood_group_Marzahn - Hellersdorf',
										'neighbourhood_group_Mitte', 'neighbourhood_group_Neukölln',
										'neighbourhood_group_Pankow', 'neighbourhood_group_Reinickendorf',
										'neighbourhood_group_Spandau',
										'neighbourhood_group_Steglitz - Zehlendorf',
										'neighbourhood_group_Tempelhof - Schöneberg',
										'neighbourhood_group_Treptow - Köpenick', 'room_type_Entire home/apt',
										'room_type_Hotel room', 'room_type_Private room',
										'room_type_Shared room', 'property_type_Entire property',
										'property_type_Other', 'property_type_Private Room',
										'property_type_Shared Room'])


## Predicting
	model = joblib.load('XGB_tuned_model')


	pred = model.predict(data_pred)[0]

	finale= (np.exp(pred).round(2))

	return render_template('result.html', 
								host_response_rate = host_response_rate,
								availability_365 = availability_365,
								accommodates = accommodates,
								bedrooms = bedrooms,
								beds = beds,
								minimum_nights = minimum_nights,
								review_scores_rating = review_scores_rating,
								amenities = amenities,
								calculated_host_listings_count = calculated_host_listings_count,
								bathrooms = bathrooms,
								instant_bookable_encode = instant_bookable_encode,
								host_is_superhost_encode = host_is_superhost_encode,
								room_type = room_type,
								property_type = property_type,
								neighbourhood_group = neighbourhood_group,
								price_suggestion = finale)





if __name__ == '__main__':
	## Load Model
	model = joblib.load('XGB_tuned_model')
	app.run(debug=True)