import pandas as pd
import geopandas as gpd
import pyarrow

def open_shapefile_state():
	gdf = gpd.read_file('tl_2019_us_county/tl_2019_us_county.shp') #file is too large to commit; download from https://catalog.data.gov/dataset/tiger-line-shapefile-2019-nation-u-s-current-county-and-equivalent-national-shapefile
	
	#reading FIPS info from https://gist.github.com/dantonnoriega/bf1acd2290e15b91e6710b6fd3be0a53#file-us-state-ansi-fips-csv
	stateFP = pd.read_csv('data/us-state-ansi-fips.csv')
	
	#reformat FP numbers
	stateFP.FP = [str(num).zfill(2) for num in stateFP.FP]
	#keep FP and ST only
	stateFP = stateFP['FP','ST']

	return gdf,stateFP
	
def filter_state(state):
	'''
	Input = state as a string, 
	abbreviation of a US state input to run the function
	'''
	fp_state = stateFP[stateFP['ST'] == state]
    gdf_state = gdf[gdf['STATEFP'] == str(fp_state.iloc[0,0])]
    
	return state, gdf_state
    

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
            state = sys.argv[1]
			print(f'Processing census shapefile for state: {state_abbreviation}.')

            return state
        else:
            print(f'{state_abbreviation} is not a valid state abbreviation.')

    else:
        print('Please provide a single state abbreviation as the argument. Example: python state_filtering.py NY')



if __name__ == "__main__":
	main()


