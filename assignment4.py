import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import datetime as dt
import seaborn as sns
cols = [1,12,13,16,17]




def data_processing():
    with open('NYPD_Arrests_Data__Historic_.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        with open('arrest_data_modifyed.csv', 'w', newline='') as new_file:
            csv_writer = csv.writer(new_file)
            for line in csv_reader:
                if line[1] is not None and '/' in line[1]:
                    date = line[1].split('/')
                    if len(date) == 3:
                        new_line = line
                        new_line[1] = date[2]
                        csv_writer.writerow(new_line)
                elif line[1] == 'ARREST_DATE':
                    csv_writer.writerow(line)
    chunks = []
    arrest_data_chunks = pd.read_csv('arrest_data_modifyed.csv', usecols=cols, chunksize=1000)
    for chunk in arrest_data_chunks:
            chunks.append(chunk)
    arrest_data_concat = pd.concat(chunks)
    #pd.to_datetime(arrest_data_concat['ARREST_DATE'], format= '%m/%d/%Y', errors='coerce')
    return arrest_data_concat

ARREST_DATA = data_processing()

def total_arrest_per_race():
    race_arrest = ARREST_DATA['PERP_RACE'].value_counts()
    
    graph = race_arrest.plot.pie(title="% of Arrests Organized by Ethnicity", textprops={'fontsize': 0})
    graph.set_ylabel('')
    graph.legend(title="Ethnicity", loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.savefig('Figure_1.png', bbox_inches='tight')




def arrest_over_time():
    fig, ax = plt.subplots(figsize=(10,7.5))
    graph = ARREST_DATA.groupby(['ARREST_DATE', 'PERP_RACE']).size().unstack().plot(ax=ax, title='# Arrests per Year')
    print(ARREST_DATA.groupby(['ARREST_DATE', 'PERP_RACE']).size().head(500))
    graph.set_xlabel("Year")
    graph.set_ylabel("# of Arrest")
    graph.legend(title="Ethnicity", fontsize=7)
    plt.savefig('Figure_2.png')

def heat_map():
    x = ARREST_DATA['Longitude'].dropna()
    y = ARREST_DATA['Latitude'].dropna()
    extent = [[-74.257159, -73.699215], [40.495992, 40.915568]] # new york city bounding box
    plt.clf()
    plt.hist2d(x, y, bins=100, cmin=100, range=extent, cmap=plt.cm.jet)
    plt.colorbar()
    plt.title("NYC Arrest Heatmap")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig('Figure_3.png')

if __name__ == "__main__":
    total_arrest_per_race()
    arrest_over_time()
    heat_map()