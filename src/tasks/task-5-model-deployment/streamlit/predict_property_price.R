# ------------------------------------------------------------------------------------
# 
# The R function that predicts property prices using the two lmer models and the input
# 
# ------------------------------------------------------------------------------------

predict_property_price <- function(area = 1000, 
                                   num_bath_rooms = 1, 
                                   num_bed_rooms = 2, 
                                   zone='Mirpur', 
                                   purpose = "sale",
                                   building_nature = "Residential"
){    
  #     Load the model
  if(purpose == "sale"){
    #     Create a data frame with user input
    newdata <- data.frame(area, num_bath_rooms, num_bed_rooms, zone)
    mod.reg <- readRDS("lmer.sale.allZones.rds")
  }
  
  else if(purpose == "rent"){
    #     Create a data frame with user input
    newdata <- data.frame(area, num_bath_rooms, num_bed_rooms, zone, building_nature)
    mod.reg <- readRDS("lmer.rent.allZones.rds")
  }
  
  else{
    print("ERROR: Purpose should be either 'sale' or 'rent'")
    return(0)
  }
  
  #     newdata <- data.frame(area, num_bath_rooms, num_bed_rooms, zone, building_nature, purpose)
  # #     mod.reg <- readRDS(model)
  #     mod.reg <- readRDS("lmer.comb.allZones.rds")
  
  #     Generate predictions
  y_predicted <- predict(mod.reg, newdata = newdata, re.form = NULL)
  
  #     Back-transform the log-transformed price value
  y_predicted_backtransformed <- exp(y_predicted)
  
  # print(paste(round(as.numeric(y_predicted_backtransformed)), "BDT", "for", purpose, "of", area, "Sq. ft", "in", zone))
  return(round(as.numeric(y_predicted_backtransformed)))
}


input = read.csv(file = 'input.csv')

area           = input$area[1]
num_bath_rooms = input$num_bath_rooms[1]
num_bed_rooms  = input$num_bed_rooms[1]
zone           = input$zone[1]
purpose        = input$purpose[1]

predicted_price = predict_property_price(area, num_bath_rooms, num_bed_rooms, zone, purpose)

print(paste('', predicted_price, ''))
