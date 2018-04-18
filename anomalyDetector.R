#install.packages("arules")



# Load the libraries
library(arules)
library(datasets)

#Reset value
x <- 0
send <- data.frame(x)
write.csv(send, file = "wrong.csv")


trans = read.transactions("test3.csv", format = "single", sep = ",", cols = c("transactionID", "sequence"))
anomaly = read.transactions("anomaly.csv", format = "single", sep = ",", cols = c("transactionID", "sequence") )
#tmp <- data.frame(labels(anomaly))




# if(is.data.frame(tmp) && nrow(tmp) == "{}"){
#   print("data.frame is empty")
# }else{
#   print("data.frame contains data")
# }

rules<-apriori(data=trans, parameter=list(supp=0.10,conf = 0.20, minlen=2), 
               # appearance = list(default="rhs", lhs = c("nannannanFrontLock1nannanUnlockednannannan Manny Kinwebhook") ),
               control = list(verbose=F))
rules<-sort(rules, decreasing=TRUE, by="count")

#rules1=subset(rules, lhs)
df = data.frame(
  lhs = labels(lhs(rules)),
  rhs = labels(rhs(rules)), 
  rules@quality)
#head(df)



write.csv(df, file = "MyData.csv")


#############################################################################
#############################################################################
#############################################################################


# 
# size.labels<-length(trans)
#                         

# }

right_total = data.frame()
wrong_total = data.frame()
right = 0
wrong = 0

sizelabels<-length(anomaly)
for(i in 1:sizelabels){
  
  print(i)
  tests = anomaly[i]
  
  size.labels<-length(anomaly)
  
  
  common=""
  common <- intersect(labels(lhs(rules)),labels(tests))
  
  if(!identical(common, character(0))){
    print("Positive number")
    right = right + 1
    # vector output
    RIGHT <- common#some processing
    
    # add vector to a dataframe
    dfright <- data.frame(RIGHT)
    right_total <- rbind(right_total , dfright)
    
    print(common)
    #print(inspect(tests))
    
  } else if(identical(common, character(0))) {
    
    wrong = wrong + 1
    print("Wrong")
    WRONG <- labels(tests)
    
    # add vector to a dataframe
    dfwrong <- data.frame(WRONG)
    wrong_total <- rbind(wrong_total,dfwrong)
    print(inspect(tests))
  }
  
}


compare= merge(data.frame(right_total), data.frame(wrong_total, row.names=NULL), by = 0, all = TRUE)[-1]

write.csv(compare, file = "compare1.csv")

if(wrong > 0){
  x<-1
  send <-data.frame(x)
  write.csv(send, file = "wrong.csv")
}




print(paste0("Wrong: ", wrong))
print(paste0("Correct: ", right))




