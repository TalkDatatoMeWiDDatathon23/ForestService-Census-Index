import pandas as pd
import geopandas as gpd
import pyarrow
import sys

def open_shapefile_state():

	print('Opening census shapefile dataset')

	gdf = gpd.read_file('tl_2019_us_county/tl_2019_us_county.shp') #file is too large to commit; download from https://catalog.data.gov/dataset/tiger-line-shapefile-2019-nation-u-s-current-county-and-equivalent-national-shapefile
	print('Shapefile ready')

	#reading FIPS info from https://gist.github.com/dantonnoriega/bf1acd2290e15b91e6710b6fd3be0a53#file-us-state-ansi-fips-csv
	print('Opening state information dataset')
	stateFP = pd.read_csv('data/us-state-ansi-fips.csv')
	stateFP['ST'] = stateFP['ST'].str.replace(' ', '')


	print('State information ready!')

	#keep FP and ST only
	
	stateFP = stateFP.drop(['STATE_NAME'], axis=1)
	
	#reformat FP numbers
	
	stateFP.FP = [str(num).zfill(2) for num in stateFP.FP]
	
	
	
	return gdf,stateFP
	

def filter_state(state):
	'''
	Input = state as a string, 
	abbreviation of a US state input to run the function
	'''
	gdf,stateFP = open_shapefile_state()
	fp_state = stateFP[stateFP['ST'] == state]
	
	print(fp_state)
	gdf_state = gdf[gdf['STATEFP'] == str(fp_state.iloc[0,0])]
	
	return gdf_state
	

def main():
	if len(sys.argv) == 2:
		state_abbreviation = sys.argv[1].upper()  # Convert to uppercase for consistency

		# List of valid state abbreviations
		valid_state_abbreviations = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
									 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
									 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
									 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
									 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

		if state_abbreviation in valid_state_abbreviations:
			
			print(f'Processing census shapefile for {state_abbreviation} state.')

			print('Preparing files to process')


			print('Filtering about to beginning')

			state = state_abbreviation

			df = filter_state(state)

			print(f'The census data for {state_abbreviation} is ready to be saved.')

			filename_csv = f'census_{state_abbreviation}.csv'
			df.to_csv(f'data/{filename_csv}', index=False)
			print('CSV file saved. Now saving the census data to parquet')

			filename_parquet = f'census_{state_abbreviation}.parquet'
			df.to_parquet(f'data/{filename_parquet}', index=False)
			print('Parquet file saved!')
			print('You can now check the data/ folder and proceed to the next steps of the analysis. Enjoy!')
		
		else:
			print(f'{state_abbreviation} is not a valid state abbreviation.')

	else:
		print('Please provide a single state abbreviation as the argument. Example: python state_filtering.py NY')



if __name__ == "__main__":
	main()

