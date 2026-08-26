# Mountain rescue incidents


This is a toy project of mine to practice several programming skills and engage in various visualisation design to understand the best strategy for different scenarios. Some analyses may not be exactly suitable to this data, but they are just for practicing purposes. 

This github repository also launches a github page https://shiminc.github.io/mountain_rescue/ which allows readers to read some of the analysis and explore the visualisations. On the github page, there would be link to relevant scripts in the repo.  

Below is a quick introduction to the directories and files in the repositories
1. `index.html`,`styles.css`,`charts/`,`assets/`: Used for the github page. The page and files in the `charts/` directory would be automatically updated when relevant scripts in `scripts/presented_on_page` is run and pushed.  
2. `data`: Consisted of the raw data between 2015- 2025 scraped from the Wasdale Mountain Rescue https://www.wmrt.org.uk/, and they are used in most analyses. The `PATH` to this data file is recorded in `scripts/utils/variables.py. 
3. `data_archive`: Consisted of the raw data since 1968 - 2025 and it was initial pilot to explore the available data. The `PATH_archive` to this data is recorded in `scripts/utils/variables.py`.
4. `scripts`: consisted of different modules corresponding to various skills and analysis I am practicing.
- `analysis` - conducting chisquare using scipy statsmodel and presented the finding in  html with plot to give overview.
-`archive_notebook` - some scraps in the notebook before I moved to the proper scripts in this repo.
- `llm` - accessing an API of a LLM and using it to help identify information from text about mountain rescue incidents.
- `miscellenous` - various other explorations.
- `network` - using the graph theory to visualise the relationship of weather conditions in each mountain rescue incident.
- `nlp` - apply what I learnt from 'NLP in action' to the data
- `plotting`- various kinds of plots are designed to both explore the data as well as to achieve the goal of making a data journalism piece. I moved some of the scripts to another `plotting_archive` as they are initial pilots, and to `presented_on_page` for those scripts that produced visualisations on the webpage. 
- `processing` - it is used to produce selected data for trial and error for other work, include d3. 
- `scraping` - scraping a website - Wasdale Mountain Rescue https://www.wmrt.org.uk/, only publicly available content (Incident reports) is scraped.
- `timeseries` - statistical modelling (arima, sarima, decomposition) and plotting  and machine learning (linear regression, SVM, random forest, xgboost) and hybrid of both to predict monthly number of incidents in timeseries.
- `utils` - modules containing utilities functions created to be used in other scripts. 

Most python file has a docstring at the top to briefly introduce what the file is. When it is a script, it means that there is a `main` function that runs when you run the script. In these scripts, there are some function written there mainly because they are only unique to that particular script. When the script is a module, it just contains various functions that are used across most of the scripts.

