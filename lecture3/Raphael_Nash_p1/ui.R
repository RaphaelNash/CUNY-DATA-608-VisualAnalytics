##
#UI logic for CUNY DATA 608 Lecure 3 p1
# 2010 Mortality Rate Ranking
#Author: Raphael Nash

library(shiny)
library(dplyr)
library(DT)
library("ggplot2")

mortality_df  <- read.csv('cleaned-cdc-mortality-1999-2010-2.csv')
mortality_df <- mortality_df %>% filter(Year==2010) 

shinyUI(fluidPage(

  
  # Application title
  titlePanel("2010 Crude Mortality Rates Ranking"),
  
  # Sidebar with a slider input for number of bins 

fluidRow(
  
   column(12,selectInput( "dx", "Select a Diagnosis:", unique(mortality_df$ICD.Chapter), selected = "Neoplasms", width = "400px"))  
  
)  ,

fluidRow(

    # Show a plot of the generated distribution

      tabsetPanel(
        tabPanel( "Graph", plotOutput("plot")) ,
        tabPanel( "Data Table", DT::dataTableOutput('mydata')) ,
        tabPanel( "Map", plotOutput("map")) 
      
    
  ))))

