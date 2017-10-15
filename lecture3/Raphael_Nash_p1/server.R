##
#Server logic for CUNY DATA 608 Lecure 3 p1
# 2010 Mortality Rate Ranking
#Author: Raphael Nash


library(shiny)
library(dplyr)
library(DT)
library("ggplot2")
library("maps")
library(DT)


 
shinyServer(function(input, output) {
  
mortality_df  <- read.csv('https://raw.githubusercontent.com/RaphaelNash/CUNY-DATA-608-VisualAnalytics/master/lecture3/Raphael_Nash_p1/cleaned-cdc-mortality-1999-2010-2.csv')
  
mort_reactive <-   reactive({input$var
  filter(mortality_df, Year==2010) %>% 
    filter(ICD.Chapter == input$dx) %>% 
    arrange((Crude.Rate)) %>% 
    mutate(State = factor(State, State)  ) %>% 
    select(State, Crude.Rate ) %>% 
    mutate(rank = dense_rank((Crude.Rate)))
   
   })
  
  
  output$mydata <-DT::renderDataTable({
    DT::datatable(mort_reactive())
  })
  
  output$plot <- renderPlot({
    
     ggplot(mort_reactive(), aes(x=State, y=Crude.Rate) )+ 
      geom_bar(stat = "Identity") +
      coord_flip() +
      geom_text(aes(label=Crude.Rate) , colour="black" , size  = 5 , hjust= -.5)  
  
  }, height = 1000
  )
  states <- map_data( "state" ) 
  
  #mapping code based on:  http://sebastianbarfort.github.io/sds/slides/lecture4.html#8 
  state_data <-  reactive({input$var
      mort <- filter(mortality_df, Year==2010) %>% 
        filter(ICD.Chapter == input$dx) %>% 
        arrange((Crude.Rate)) %>% 
        mutate(State = factor(State, State)  ) %>% 
        select(State, Crude.Rate ) %>% 
        mutate(rank = dense_rank((Crude.Rate)))
      
      state_codes <- read.csv("http://www.fonz.net/blog/wp-content/uploads/2008/04/states.csv")
      state_codes$State<- tolower(state_codes$State)
      state_codes$State<- tolower(state_codes$State)
      names(state_codes) <- c("region", "State")
      state_data <- left_join(mort, state_codes)
      state_data <- left_join( states, state_data)
      
    })

  output$map <- 
    renderPlot (
      ggplot(state_data(), aes(x = long, y = lat, group = group)) + 
        geom_polygon(aes(fill = rank)) + 
        scale_fill_gradient(low = "green", high = "red") +
        expand_limits() + 
        theme_minimal()
    )
})
