import pandas as pd

defaultdata = {'INITIALS':['CBR','LS','JRE'], 
			   'TIME':[191.6, 186.3, 185.9]}

df = pd.DataFrame.from_dict(defaultdata)
#dfSorted = df.sort_index(ascending=False)
dfSort = df.groupby(['INITIALS']).min()
dfSort.to_hdf('default.hdf', 'test', mode='w')
dfSort.to_csv('default.csv')
dfSort.to_html('default.html')