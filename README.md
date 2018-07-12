# Facets

Facets is a Google AI tool that contains two visualizations for understanding and analyzing machine learning datasets: 
- Facets Overview 
- Facets Dive

You can read more about facets from https://github.com/PAIR-code/facets. 
Also, you can try a love demo of Facets where you can upload your data and visualize them online without having to install anything on your PC through https://pair-code.github.io/facets/.


This repository is intended to hold a simple Python code that will initiate an interactive HTML web page using Facets Dive.

You can generate facets-dive html page throught the rdbms_main.py file through Bash:

  python test1.py FIELD INPUT

  Arguments:
  
    FIELD    Search specified column from database
    INPUT    The query

**NOTE: you may enter any number of FIELD-INPUT arguments
