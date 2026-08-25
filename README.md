# Job interview

This branch was created for a job interview and focus on the descriptive analysis of the incidents between 2015 - 2025 and timeseries analysis

This is a toy project of mine to practice several programming skills and engage in various visualisation design to understand the best strategy for different scenarios. Some analyses may not be exactly suitable to this data, but they are just for practicing purposes. 

This github repository also launches a github page which allows readers to read some of the analysis and explore visualisations. The component relevant to the webpage is
.

Below is a quick introduction to the directories and files in the repositories, those in **bold** are particularly relevant to the job interview:
1. `index.html`,`styles.css`,`charts/`: Used for github page which allows readers to read some of the analysis and explore visualisations. The page and files in the `charts/` directory would be automatically updated when relevant scripts is run and pushed.  
2. **`data`**: Consisted of the raw data between 2015- 2025 scraped from the Wasdale Mountain Rescue https://www.wmrt.org.uk/, and they are used in most analyses. The `PATH` to this data is recorded in `scripts/utils/variables.py.
3. `data_archive`: Consisted of the raw data since 1968 - 2025 and it was initial pilot to explore the available data. The `PATH_archive` to this data is recorded in `scripts/utils/variables.py.
4. `scripts`: consisted of different modules corresponding to various skills I am practicing.
1. `llm` - accessing an API of a LLM and using it to help identify information from text about mountain rescue incidents.
2. `scraping` - scraping a website - Wasdale Mountain Rescue https://www.wmrt.org.uk/, only publicly available content (Incident reports) is scraped.
3. `plotting` - various kinds of plots are designed to both explore the data as well as to achieve the goal of making a data journalism piece. I moved some of the scripts to another `plotting_archive` for those scripts I won't be discussing during the interview,and to `presented_on_page` for those scripts that produced visualisations on the webpage. 
4. `timeseries` - statistical modelling and plotting (arima, sarima, decomposition) and machine learning (linear regression, SVM, random forest, xgboost) and hybrid of both to predict monthly number of incidents in timeseries
5. `network` - using the graph theory to visualise the relationship of weather conditions in each mountain rescue incident.
6. `nlp` - apply what I learnt from 'NLP in action' to the data
7. `miscellenous` - various other explorations.
8. 
9. `utils` - utilities functions created to be used in other modules 

