##
#UI logic for CUNY DATA 608 Lecure 3 p2
# Change in mortality Rates
#Author: Raphael Nash


library(shiny)
library(dplyr)
library(DT)
library("ggplot2")
library(tidyr)

mortality_df  <- read.csv('cleaned-cdc-mortality-1999-2010-2.csv')
mortality_df <- mortality_df %>% filter(Year==2010) 

shinyUI(fluidPage(

  # Application title
  titlePanel("Change in Mortality Rates 1999-2010"),
  
  # Sidebar with a slider input for number of bins 

fluidRow(
  
   column(12,selectInput( "dx", "Select a Diagnosis:", unique(mortality_df$ICD.Chapter), selected = "Neoplasms", width = "400px"))  
  
)  ,

fluidRow(
  textOutput("us_average_rate_change_txt")
),
fluidRow(
  textOutput("preg_error")
),

fluidRow(

    # Show a plot of the generated distribution

      tabsetPanel(
        tabPanel( "Graph", plotOutput("plot")) ,
        tabPanel( "Data Table", DT::dataTableOutput('data_table')) 

  ))))

