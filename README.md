# **Stock Analysis**

## **Objective**
The objective of this project is to help track the stock prices of some selected tickers listed on IBOVESPA. The point here is not to evaluate the quality of the company; the analyses are just a way to find stocks that are far from their maximum value and close to the minimum (maybe it is a good time to buy IF the company is good)

## **Sources**
All the extracted information comes from the yfinance library of Yahoo Finance and the CVM page. Since these are public and free sources, there is a great possibility of them ceasing to work, requiring maintenance in the code.

## **ETL execution**
First of all, you can choose the tickers to analyze; you just need to inform them in the file  ".data/extract/stock_list.csv"

It's possible to run the scripts manually; they are inside the "notebook" folder. However, if you want to run all of them in a more convenient way, install Docker and run the docker-compose.yaml

*docker-compose up -d*

the ETL will save .csv files into the folder .data/gold/

## **Data Visualization**
The visualization isn't finished yet, but most of the files are linked to the .pbix saved in ".pbix/stock_panel.pbix"


## *Contact*
If you have any questions or critiques, you can reach me on LinkedIn (https://www.linkedin.com/in/duanimperatori/)

