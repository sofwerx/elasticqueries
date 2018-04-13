

MyData <- read.csv(file="/mnt/safehouse-data-transformations1/transaction_data.csv", header=TRUE, sep=",")
install.packages("rlang", type = "source")
install.packages("cowplot")
devtools::install_url("https://github.com/wilkelab/cowplot/archive/0.6.3.zip")
devtools::install_github("kassambara/ggpubr")
devtools::install_github("kassambara/factoextra")
library("devtools")
library("FactoMineR")
library("factoextra")


#MyData2 <- data.frame(lapply(MyData, function(x) as.factor(as.character(x))))

MyData2 <- MyData[,sapply(MyData)]


res.mca <- MCA(MyData2)
eig.val <- get_eigenvalue(res.mca)

fviz_screeplot(res.mca, addlabels = TRUE, ylim = c(0, 45))




