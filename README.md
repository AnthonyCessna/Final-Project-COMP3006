# Final-Project-COMP3006

## Data Sets 
- annual_aqi_by_county.csv: data breaking down air quality metrics by state and county
- birth_data.csv: data breaking down average birth weight by state and county
- combined.csv: a merging and massaging of the birth data and air quality data set with derived metrics sucha as air quality score 
  and state breakdowns of min, max, and avg birth weights for further analysis
  
  ## Research Question
  Does a states air quality effect birth weights?
     
     
  ## Conclusiuon:
  ### note( high Air Quiality Score (AQS) means poor air quality, eg: California AQ ~ 185, this is poorer air quality then a lower AQS)
  We did an aggregation of all the counties within the state to gain an "Air Quality Score by State" and an "Average Birth Weight by State" for 46 States. 
  Then created four quadrants that categorized states in the following: 
  
  quadrant 1: High AQS, High ABW 
  quadrant 2: High AQS, Low ABW
  quadrant 3: Low AQS, Low ABW
  quadrant 4: Low AQS, High ABW
  
  out of 46 States we had 14 in quadrant 2, 14 in quadrant 4, 9 in quadrant quadrant 1, 9 in quadrant 3. 
  60% of the states fall in a category of High AQS and low ABW (dirtier air lower birth weight), or low AQS high ABW( cleaner air higher birth weight).
  This does imply a slight correlation with the change  air quality and the change of birthweight.
  
  # How To Operate
  run requirments.txt in a venv, then use command python3 air*.py with below command line arguments
  ### commands:
  -p --pd   prints analytic graphs to a pdf
  -c --csv  writes the data sets listed above to a csv
  -w --web  renders the analytic graphs to your browser 
 
 ### choices:
 air_quality:  outputs air_quality analysis or data to a PDF, CSV or a web browser depending on the command  (-p --pdf, -c --csv, -w --web)
 birth weight: outputs birth weight analysis or data to a PDF, CSV or a web browser depending on the command  (-p --pdf, -c --csv, -w --web)
 combined:     outputs full research of combined data analysis or data to a PDF, CSV or a web browser depending on the command  (-p --pdf, -c --csv, -w --web)
 all:          outputs all of the above analysis or data to a PDF, CSV or a web browser depending on the command  (-p --pdf, -c --csv, -w --web)



  
  

  
  
  
  
