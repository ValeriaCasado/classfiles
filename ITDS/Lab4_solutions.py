import sqlite3
import sys
import csv
from collections import Counter
import matplotlib.pyplot as plt

##Exercise 1
def float_or_none(x):
	try:
		return float(x);
	except:
		return None;
  
conn = sqlite3.connect("SE4ALL.db")
c = conn.cursor()

c.execute('''CREATE TABLE energy (CountryName TEXT NOCASE, IndicatorCode TEXT NOCASE, Year INTEGER, Value REAL)''') #<--make sure to only do this once ;)
conn.commit()
with open("SE4ALLData.csv", 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	headers = next(reader);
	headerid = {};
	for i,h in enumerate(headers):
		headerid[h] = i;
	
	for row in reader:
		for year in range(1990,2017):
			c.execute("INSERT INTO energy VALUES (:CountryName, :IndicatorCode, :Year, :Value)", {
			'CountryName': row[0],
			'IndicatorCode': row[3],
			'Year': year,
			'Value': float_or_none( row[headerid[str(year)]] )
			})

conn.commit()


##Exercise 2
c.execute("SELECT CountryName, Value FROM energy WHERE IndicatorCode = '4.1_SHARE.RE.IN.ELECTRICITY' AND Year = 1990 ORDER BY Value");
print(c.fetchall())

#
#INNER JOIN 
# 

for row in c.execute("""
SELECT rural.CountryName, rural.value, urban.value, rural.value/urban.value
FROM (SELECT CountryName, Value FROM energy WHERE IndicatorCode = '1.2_ACCESS.ELECTRICITY.RURAL' AND Year = 2016) as rural 
INNER JOIN (SELECT CountryName, Value FROM energy WHERE IndicatorCode = '1.3_ACCESS.ELECTRICITY.URBAN' AND Year = 2016) as urban ON rural.CountryName = urban.CountryName
WHERE rural.value IS NOT NULL and urban.value is NOT NULL 
ORDER BY rural.value/urban.value DESC
"""):
	print(row)

rural = { row[0]:row[1] for row in c.execute("""SELECT CountryName, Value FROM energy WHERE IndicatorCode = '1.2_ACCESS.ELECTRICITY.RURAL' AND Year = 2016""") }
urban = { row[0]:row[1] for row in c.execute("""SELECT CountryName, Value FROM energy WHERE IndicatorCode = '1.3_ACCESS.ELECTRICITY.URBAN' AND Year = 2016""") }
ratios = { k:rural[k]/urban[k] for k in rural if rural[k] != None and urban[k] != None }
for k in sorted(ratios, key=ratios.get, reverse=True): print(k, ratios[k] )
	

	
		

##Exercise 3
countries = ["United Kingdom", "Germany", "China", "Nigeria", "India", "United States"]
cl = ", ".join([ "'{}'".format(c) for c in countries])

data = {}
for country in countries:
	c.execute("SELECT Year, Value FROM energy WHERE IndicatorCode = '4.1_SHARE.RE.IN.ELECTRICITY' AND CountryName IN ('{}')".format(country) );
	data[ country ] = [[], []]
	for row in c.fetchall():
		data[ country ][0].append( row[0] );
		data[ country ][1].append( row[1] );
		
	plt.plot(data[ country ][0], data[ country ][1], label=country)
	
plt.legend()
plt.xlabel("Year")
plt.ylabel("Renewable electricity share of total electricity output (%)")
plt.show();
plt.close();


##Exercise 4
##If you don't have 1 TB of ram your code will likely crash!
with open("BIG_FILE.csv", 'r') as infile:
	csvreader = csv.reader(infile, delimiter=",")
	for row in csvreader:
		continue

##Exercise 5
x = ['A', 'A', 'B', 'B', 'C', 'A', 'C', 'A', 'A']
##using a dict
count = {}
for elem in x:
	if elem not in count:
		count[elem] = 1
	else:
		count[elem] += 1
for k in sorted(count, key = count.get):		
	print(k, count[k])

##Exercise 6
x = ['A', 'A', 'B', 'B', 'C', 'A', 'C', 'A', 'A']
i = 0;
majority_elem = None;
for elem in x:
	if i == 0: 
		majority_elem = elem;
		i = 1;
	else:
		if elem == majority_elem:
			i += 1;
		else:
			i -= 1;

print("majority candidate = ", majority_elem)		

count = 0;	
lenx = 0;	
for elem in x:
	lenx += 1
	if elem == majority_elem:
		count += 1

if 2*count > lenx :
	print(majority_elem, "is a majority element");
else:
	print("There is no majority element")

##Exercise 7
x = ['A', 'A', 'B', 'B', 'C', 'A', 'C', 'A', 'A']
##using sets
distinct = set();
for elem in x:
	distinct.add(elem)
print(len(distinct), distinct)	


##Exercise 8
import numpy as np	
np.random.seed(123456789)
sum_n = 0;

for i in range(1000):
	if i%10 == 0: print(i, "/ 1000")
	
	n = 0;
	while True:
		if np.random.randint(0,1000) == 0: break;
		n += 1;

	sum_n += n
	
print("average of n = ", sum_n / 1000 )


##Exercise 9
#The answer above should be ~1000
