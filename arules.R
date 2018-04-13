  
  
  
  
  # Load the libraries
  library(arules)
 
  library(datasets)
  
  
  trans = read.transactions("test3.csv", format = "single", sep = ",", cols = c("transactionID", "sequence"))
  #tests = read.transactions("test.csv", format = "single", sep = ",", cols = c("transactionID", "value") ,rm.duplicates=FALSE)
  

  
  rules<-apriori(data=trans, parameter=list(supp=0.10,conf = 0.20, minlen=2), 
                 # appearance = list(default="rhs", lhs = c("nannannanFrontLock1nannanUnlockednannannan Manny Kinwebhook") ),
                 control = list(verbose=F))
  rules<-sort(rules, decreasing=TRUE, by="count")
  
  #rules1=subset(rules, lhs)
  df = data.frame(
    lhs = labels(lhs(rules)),
    rhs = labels(rhs(rules)), 
    rules@quality)
  head(df)
  
  
  
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
  
  sizelabels<-length(trans)
  for(i in 1:sizelabels){
  
    print(i)
    tests = trans[i]
  
    size.labels<-length(trans)
  
  
    common=""
    common <- intersect(labels(lhs(rules)),labels(tests))
    
    if(!identical(common, character(0))){
      print("Positive number")
      right = right + 1
      # vector output
      RIGHT <- common#some processing
      
      # add vector to a dataframe
      dfright <- data.frame(RIGHT)
      right_total <- rbind(right_total,dfright)

      print(common)
      #print(inspect(tests))
  
    } else {
      
      wrong = wrong + 1
      print("Wrong")
      WRONG <- labels(tests)

      # add vector to a dataframe
      dfwrong <- data.frame(WRONG)
      wrong_total <- rbind(wrong_total,dfwrong)
      print(inspect(tests))
    }
  
  }
  
  print(wrong)
  print(right)
  
 # compare=data.frame(right_total,wrong_total)
  compare= merge(data.frame(right_total), data.frame(wrong_total, row.names=NULL), by = 0, all = TRUE)[-1]
 
  write.csv(compare, file = "compare1.csv")
  

  
  

