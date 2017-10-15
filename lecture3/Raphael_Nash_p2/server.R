##
#Server logic for CUNY DATA 608 Lecure 3 p2
# Change in mortality Rates
#Author: Raphael Nash

library(shiny)
library(dplyr)
library(DT)
library("ggplot2")
library("maps")
library(DT)
library(tidyr)



 
shinyServer(function(input, output) {
  
mortality_df  <- read.csv('https://raw.githubusercontent.com/RaphaelNash/CUNY-DATA-608-VisualAnalytics/master/lecture3/Raphael_Nash_p1/cleaned-cdc-mortality-1999-2010-2.csv')
  
mort_reactive <-   reactive({input$var

  mort_df <- filter(mortality_df, Year %in% c(2010, 1999) )  %>% 
    filter(ICD.Chapter == input$dx) %>% 
    select(State, Year, Crude.Rate, Deaths, Population )  %>% 
    unite (  Deaths_Population_Crude.Rate, Deaths, Population, Crude.Rate) %>% 
    spread( Year, Deaths_Population_Crude.Rate) %>% 
    separate( "1999", c( "Deaths_1999", "Population_1999","Crude.Rate_1999" ))  %>% 
    separate( "2010", c("Deaths_2010", "Population_2010","Crude.Rate_2010" ))
  
  mort_df <- mort_df[complete.cases(mort_df), ]
  mort_df$Deaths_2010 <- as.numeric(mort_df$Deaths_2010)
  mort_df$Population_2010 <- as.numeric(mort_df$Population_2010)
  mort_df$Crude.Rate_2010 <- as.numeric(mort_df$Crude.Rate_2010)
  mort_df$Deaths_1999 <- as.numeric(mort_df$Deaths_1999)
  mort_df$Population_1999 <- as.numeric(mort_df$Population_1999)
  mort_df$Crude.Rate_1999 <- as.numeric(mort_df$Crude.Rate_1999)
  mort_df$percent_change <- (mort_df$Crude.Rate_2010 - mort_df$Crude.Rate_1999) / mort_df$Crude.Rate_1999 *100
  mort_df$percent_change <- round(mort_df$percent_change, 2)
    
  mort_df %>% 
    arrange((percent_change)) %>% 
    mutate(State = factor(State, State)  ) %>% 
    mutate(rank = dense_rank((percent_change)))
   })
  

us_average_rate_change <- reactive({
  mm <- mort_reactive()
  deaths_1999 <- sum( mm$Deaths_1999)
  deaths_2010 <- sum( mm$Deaths_2010)
  pop_1999 <-  sum( mm$Population_1999)
  pop_2010 <-  sum( mm$Population_2010)
  
  cr_1999 <- (deaths_1999 / pop_1999 ) 
  cr_2010 <- (deaths_2010 / pop_2010 )
  
  round(((cr_2010 - cr_1999 )/cr_1999)*100,2)
  
})
  output$data_table <-DT::renderDataTable({
    
    mm<-  mort_reactive() %>% 
      select(State,percent_change, rank )
    colnames(mm) <- c("State", "Mortality Percentage Change", "Rank")
    
    DT::datatable(mm)
  })
  
  
  output$preg_error <- renderText({ 
    err <- ""
    if ( input$dx == "Pregnancy, childbirth and the puerperium") {
       err <- "Deaths too low to computer percentages"
    }
    err
  })
  
  output$us_average_rate_change_txt <- renderText({ 
    paste ( "Average US change in Crude Mortality Rate: ", us_average_rate_change(), "%" ,sep = "") 
  })
  
  output$plot <- renderPlot({

     ggplot(mort_reactive(), aes(x=State, y=percent_change) )+ 
      geom_bar(stat = "Identity") +
      geom_hline(yintercept = us_average_rate_change(), color="blue") +
      coord_flip() +
      geom_text(aes(label=percent_change) , colour="black" , size  = 5 , hjust= -.5)  + 
      ylab ( "Percent Change in Mortality")
  
  }, height = 1000
  )
  
  
  
 



})
