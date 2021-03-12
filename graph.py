import pandas as pd
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import statistics
import seaborn as sns
import tabulate



file_24 = "/Users/varun/Desktop/ece143_fa19_bazhou_Varun_Angela_Frank-master/Craigslist_iphone 2019-11-24.csv"

file_25 = "/Users/varun/Desktop/ece143_fa19_bazhou_Varun_Angela_Frank-master/Craigslist_iphone 2019-11-25.csv"

file_26 = "/Users/varun/Desktop/ece143_fa19_bazhou_Varun_Angela_Frank-master/Craigslist_iphone 2019-11-26.csv"

df_24 = pd.read_csv(file_24)

df_25 = pd.read_csv(file_25)

df_26 = pd.read_csv(file_26)


def plot_avg_price_per_model_per_day(df_24, df_25, df_26):

	'''
	remove items with price range 100-1000 then find average price and plot a bar graph
	param: pd.dataframe (xNumber of Days)
	return: scatter plot
	'''
	
	#Calculating average price for 24th 
	price_24 = df_24.Price
	price_24 = price_24[(price_24 <= 1000)]
	price_24 = price_24[(price_24 > 100)]
	avg_24 = price_24.mean()

	#Calculating average price for 25th 
	price_25 = df_25.Price
	price_25 = price_25[(price_25 <= 1000)]
	price_25 = price_25[(price_25 > 100)]
	avg_25 = price_25.mean()	

	#Calculating average price for 26th 
	price_26 = df_26.Price
	price_26 = price_26[(price_26 <= 1000)]
	price_26 = price_26[(price_26 > 100)]
	avg_26 = price_26.mean()	

	avg_price_day = [avg_24, avg_25, avg_26]

	day_labels = ["24th", "25th", "26th"]

	
	x = np.arange(len(day_labels))

	fig = plt.figure()
	ax = plt.axes()


	ax.plot(x, avg_price_day, color='blue', marker='o', linestyle='dashed', linewidth=2, markersize=12)

	ax.set_xlim(right= x[-1] + 0.5)


	cur_axes = plt.gca()
	cur_axes.axes.get_xaxis().set_visible(False)
	
	plt.ylabel("Price ($)")
	day_label = 24
	
	ax.text(0, avg_24, "   24th Nov")

	ax.text(1, avg_25, "   25th Nov")

	ax.text(2, avg_26, "   26th Nov")

	plt.title("Craigslist Average Price iPhone X ")
	plt.savefig("avg_price_iphoneX_CG.png")	



def avg_price_per_model_per_week(df_24, df_25, df_26):
	"""
	Average the average price per model per day ith price range 100-1000 then find average price
	:param: pd.dataframe
	:return: int
	"""

	#Calculating average price for 24th 
	price_24 = df_24.Price
	price_24 = price_24[(price_24 <= 1000)]
	price_24 = price_24[(price_24 > 100)]
	avg_24 = price_24.mean()

	#Calculating average price for 25th 
	price_25 = df_25.Price
	price_25 = price_25[(price_25 <= 1000)]
	price_25 = price_25[(price_25 > 100)]
	avg_25 = price_25.mean()	

	#Calculating average price for 26th 
	price_26 = df_26.Price
	price_26 = price_26[(price_26 <= 1000)]
	price_26 = price_26[(price_26 > 100)]
	avg_26 = price_26.mean()	


	avg_price_day_list = [avg_24, avg_25, avg_26]

	return statistics.mean(avg_price_day_list)



def plot_avg_price_per_condition(df_24, df_25, df_26):
	"""
	return a bar chart of average price per condition for craigslist
	:param: pd.dataframe
	"""

	attributes_list = []

	price_list = []

	df_sorted = df_24.sort_values(by='Attributes')
	
	# print(df_sorted["Attributes"])

	
	for i in range(len(df_sorted)):
		attributes_list.append(df_sorted["Attributes"][i])
		price_list.append(df_sorted["Price"][i])

	Unknown_total_price = 0
	Unknown_counter = 0 

	new_total_price = 0
	new_counter = 0  

	like_new_total_price = 0
	like_new_counter = 0  

	good_total_price = 0 
	good_counter = 0

	excellent_total_price = 0 
	excellent_counter = 0 


	for index in range(len(attributes_list)):
		
		if attributes_list[index] == "Unknown":
			Unknown_total_price += price_list[index]
			Unknown_counter += 1

		if attributes_list[index] == "new":
			new_total_price += price_list[index]
			new_counter += 1

		if attributes_list[index] == "like new":
			like_new_total_price += price_list[index]
			like_new_counter += 1

		if attributes_list[index] == "good":
			good_total_price += price_list[index]
			good_counter += 1

		if attributes_list[index] == "excellent":
			excellent_total_price += price_list[index]
			excellent_counter += 1


	Unknown_avg = Unknown_total_price / Unknown_counter
	new_avg = new_total_price / new_counter
	like_new_avg = like_new_total_price / like_new_counter
	good_avg = good_total_price / good_counter
	excellent_avg = excellent_total_price / excellent_counter


	# print("Unknown", Unknown_avg)
	# print("new", new_avg)
	# print("like new", like_new_avg)
	# print("good", good_avg)
	# print("excellent", excellent_avg)

	avg_price = [Unknown_avg, new_avg, like_new_avg, good_avg, excellent_avg]

	day_labels = ["Unknown", "New", "Like New", "Good", "Excellent"]

	index = np.arange(len(day_labels))
	plt.bar(x = index, height = avg_price)

	plt.xticks(index, day_labels, rotation=-30) #Rotate X Labels
	plt.ylabel("Price ($)")
	plt.title("Craigslist Average Price per Condition iPhone X")
	plt.savefig("avg_price_per_condition_iphoneX_CG.png")	
  

def newPost(dt,update):
    '''
    return the number of newly added post
    update: date of the generated file. e.g. the file was generated on 2019-11-24 then update = '2019-10-24'
    '''
    dt.postDate = dt.postDate.apply(lambda x: x[0:10]) # remove time stamp, leave only yr-month-day
    gp = dt.groupby('postDate').groups
    return gp[update].size


def plot_new_post(df_24, df_25, df_26):

	"""
	return a scatter plot of new daily posts
	:param: pd.dataframe 

	"""

	no_24 = newPost(df_24, '2019-11-24')

	no_25 = newPost(df_25, '2019-11-25')

	no_26 = newPost(df_26, '2019-11-26')

	new_posts_list = [no_24, no_25, no_26]

	day_labels = ["24th", "25th", "26th"]

	
	x = np.arange(len(day_labels))

	fig = plt.figure()
	ax = plt.axes()


	ax.plot(x, new_posts_list, color='blue', marker='o', linestyle='dashed', linewidth=2, markersize=12)

	ax.set_xlim(right= x[-1] + 0.5)


	cur_axes = plt.gca()
	cur_axes.axes.get_xaxis().set_visible(False)
	
	plt.ylabel("Price ($)")
	
	ax.text(0, no_24, "   24th Nov")

	ax.text(1, no_25, "   25th Nov")

	ax.text(2, no_26, "   26th Nov")

	plt.title("Craigslist Daily New Posts iPhone X ")
	plt.savefig("new_posts_iphoneX_CG.png")	



def distance(dt):
    
    t1 = dt[(dt.Price > 100)]
    t2 = t1[(t1.Price <= 1000)]
    under_ten = len(t2[(t2.distance < 10)])
    ten_to_fifty = len(t2[(t2.distance < 50)]) - under_ten
    fifty_above = len(t2[(t2.distance >= 50)])
    return [under_ten, ten_to_fifty, fifty_above] 

def plot_distance(df_24, df_25, df_26):

	"""


	"""
	dist_24 = distance(df_24)
	dist_25 = distance(df_25)
	dist_26 = distance(df_26)

	avg_no_dist_under_ten = (dist_24[0] + dist_25[0] + dist_26[0]) / 3
	avg_no_dist_ten_to_fifty = (dist_24[1] + dist_25[1] + dist_26[1]) / 3
	avg_no_dist_fifty_above = (dist_24[2] + dist_25[2] + dist_26[2]) / 3

	# print(dist_24)


	
	avg_no_dist = [avg_no_dist_under_ten, avg_no_dist_ten_to_fifty, avg_no_dist_fifty_above ]

	# Pie chart
	labels = ["<10 mi", "10 - 50 mi", ">50 mi"]

	
	# fig1, ax1 = plt.subplots()
	# ax1.pie(avg_no_dist, labels=labels, autopct='%1.1f%%', startangle=90)
	# # Equal aspect ratio ensures that pie is drawn as a circle
	# ax1.axis('equal')  
	# plt.tight_layout()
	




	
	# #add colors
	# colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
	# fig1, ax1 = plt.subplots()
	# ax1.pie(avg_no_dist, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
	# # Equal aspect ratio ensures that pie is drawn as a circle
	# ax1.axis('equal')
	# plt.tight_layout()
	


	fig1, ax1 = plt.subplots()
	#add colors
	colors = ['#ff9999','#66b3ff','#99ff99']
	
	# explsion
	explode = (0.05,0.05,0.05)
	 
	ax1.pie(avg_no_dist, colors = colors, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85, explode = explode)
	
	#draw circle
	centre_circle = plt.Circle((0,0),0.70,fc='white')
	fig = plt.gcf()
	fig.gca().add_artist(centre_circle)

	ax1.axis('equal')  
	plt.title("Average Seller Distance of iPhoneX CG")
	plt.savefig("distance_pie.png")






plot_distance(df_24, df_25, df_26)


# plot_new_post(df_24, df_25, df_26)

# plot_avg_price_per_condition(df_24, df_25, df_26)

#plot_avg_price_per_model_per_day(df_24, df_25, df_26)

# print(avg_price_per_model_per_week(df_24, df_25, df_26))








