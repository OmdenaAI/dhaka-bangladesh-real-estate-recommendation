# ------------------------------------------------------------------------------------
# 
# The R function that predicts property prices using the two lmer models and the input
# 
# ------------------------------------------------------------------------------------

predict_property_price <- function(area = 1000, 
                                   num_bath_rooms = 1, 
                                   num_bed_rooms = 2, 
                                   zone='Mirpur', 
                                   purpose = "sale"){    

    #     Create a data frame with user input
    newdata <- data.frame(area, num_bath_rooms, num_bed_rooms, zone)

    #     Load the model
    if(purpose == "sale")
        mod.reg <- readRDS("lmer.sale.allZones.rds")
    else if(purpose == "rent")
        mod.reg <- readRDS("lmer.rent.allZones.rds")
    else{
        print("ERROR: Purpose should be either 'sale' or 'rent'")
        return(0)
    }

    #     Generate predictions
    y_predicted <- predict(mod.reg, newdata = newdata, re.form = NULL)

    #     Back-transform the log-transformed price value
    y_predicted_backtransformed <- exp(y_predicted)
    
    # print(paste(round(as.numeric(y_predicted_backtransformed)), "BDT", "for", purpose, "of", area, "Sq. ft", "in", zone))
    return(round(as.numeric(y_predicted_backtransformed)))
}

# Code to call the function based on the input
# A list of top 10 zones in terms of the no. data points in the training set
zones_top_10 = c('Mirpur',
 'Chattogram City',
 'Bashundhara R/A',
 'Khilgaon',
 'Mohammadpur',
 'Uttara',
 'Badda',
 'Dakshin Khan',
 'Sub-district of Chattogram',
 'Dhaka Cantonment')

area           = 4000
num_bath_rooms = 1
num_bed_rooms  = 2
zone           = zones_top_10[3]
purpose        = "sale"

predicted_price = predict_property_price(area, num_bath_rooms, num_bed_rooms, zone, purpose)

print(paste(predicted_price, "BDT", "for", purpose, "of", area, "Sq. ft", "in", zone))

# print("")
# print(paste("Predicted sale price:", predicted_price))

