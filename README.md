# Final-Project-COMP3006

  ## Data Sets 
  - annual_aqi_by_county.csv: data breaking down air quality metrics by state and county
  - birth_data.csv: data breaking down average birth weight by state and county
  - combined.csv: a merging and massaging of the birth data and air quality data set with derived metrics sucha as air quality score 
  and state breakdowns of min, max, and avg birth weights for further analysis
  
  ## Research Question
  Does the air quality of a given state have an  effect on birth weights?
     
     
  ## Conclusiuon:
  NOTE high Air Quiality Score (AQS) means poor air quality, eg: California AQ ~ 185, this is poorer air quality then a lower AQS
  
  We did an aggregation of all the counties within the state to gain an "Air Quality Score by State" and an "Average Birth Weight by State" for 46 States. 
  Then created four quadrants that categorized states in the following: 
  
  - quadrant 1: High AQS, High ABW 
  - quadrant 2: High AQS, Low ABW
  - quadrant 3: Low AQS, Low ABW
  - quadrant 4: Low AQS, High ABW
  
  Out of 46 States,  14 are in quadrant 2, 14  are in quadrant 4, 9  are in quadrant quadrant 1, and 9 are in quadrant 3. 
  Over 60% of the states fall in a category of High AQS and low ABW (dirtier air lower birth weight), or low AQS high ABW( cleaner air higher birth weight).
  This  implies a possible correlation between air quality and birth weight. Visulaizations that further explain this analysis are available with the combined         choice presented below.
  
  # How To Operate
  run requirments.txt in a venv, then use command python3 air*.py with below command line arguments
  
  ### Required Command Line Arguments (choose one, listed options are required)
  - store:  stores pdf or csv locally (required options: --pdf or  --csv)
  - render: renders charts/analysis on your browser (required option: --web)
  
  ### options (choice required)
  - -p, --pdf:   prints analytic graphs to a pdf 
  - -c, --csv:  writes the data sets listed above to a csv
  - -w, --web:  renders the analytic graphs to your browser 
 
  ### choices:
  NOTE choices need to proceed (-p --pdf, -c --csv, -w --web)
  - air_quality:  outputs air_quality analysis proceeding  
  - birth weight: outputs birth weight analysis proceeding 
  - combined:     outputs combined analysis proceeding 
  - all:            outputs all of the above analysis 



  
  

  
  
  
  
