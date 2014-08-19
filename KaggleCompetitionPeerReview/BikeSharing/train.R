setwd("~/Google Drive/Projects/coursera-introduction-to-data-science/KaggleCompetitionPeerReview/BikeSharing")
traindata <- read.csv("data/train.csv", header=TRUE, stringsAsFactors=FALSE)
testdata <- read.csv("data/test.csv", header=TRUE, stringsAsFactors=FALSE)

library("lubridate")
library("rpart")
#install.packages('rattle')
#install.packages('rpart.plot')
#install.packages('RColorBrewer')
#install.packages('Metrics')
library(rattle)
library(rpart.plot)
library(RColorBrewer)
library(Metrics)
library(caret)


#function for add custom columns
enhancedata <- function (data)
{
  data$dt <- ymd_hms(data$datetime)
  data$hour <- hour(data$dt)
  data$datetime=strptime(as.character(data$datetime), format="%Y-%m-%d %H:%M:%S")
  data$weekday = as.factor(weekdays(data$datetime))
  
  data$windrange[data$windspeed < 10] <- '<10'
  data$windrange[data$windspeed >= 10 & data$windspeed < 20] <- '10-20'
  data$windrange[data$windspeed >= 20 & data$windspeed < 30] <- '20-30'
  data$windrange[data$windspeed >= 30] <- '30+'
  data$windrange = as.factor(data$windrange)
  
  data$humrange[data$humidity < 25] <- '<25'
  data$humrange[data$humidity >= 25 & data$humidity < 50] <- '25-50'
  data$humrange[data$humidity >= 50 & data$humidity < 75] <- '50-75'
  data$humrange[data$humidity >= 75 & data$humidity <100] <- '50-75'
  data$humrange[data$humidity >= 100] <- '100+'
  data$humrange = as.factor(data$humrange)
  
  data$working[data$holiday == 1] <- 0
  data$working[data$weekday == "Saturday"] <- 0
  data$working[data$weekday == "Sunday"] <- 0
  data$working[is.na(data$working)] <- 1
  data$working = as.factor(data$working)
  
  data$hour = as.numeric(data$datetime$hour)
  return(data)
} 

traindata <- enhancedata(traindata)
testdata <- enhancedata(testdata)

#split data in train and test
df <- traindata
bound <- floor((nrow(df)/5)*1)         #define % of training and test set

df <- df[sample(nrow(df)), ]           #sample rows 
train <- df[1:bound, ]              #get training set
test <- df[(bound+1):nrow(df), ] 


library(reshape)

#pivot table

WeekHour=aggregate(count ~ + hour+ weekday, data =train, FUN=mean)
WorkingHour=aggregate(count ~ + hour+ working, data =train, FUN=mean)


library(ggplot2)
#Line chart
ggplot(WorkingHour, aes(x=hour, y=count)) + geom_line(aes(group=working, color=working),size=2,alpha=0.5)

#Heat map
ggplot(WeekHour, aes(x=hour, y=weekday)) + geom_tile(aes(fill = count))+ scale_fill_gradient(low="white", high="red")



#str(train)
#prop.table(table(train$count))
#table(train$workingday, train$count)

#summary(train$count[train$workingday==0])
#summary(train$count[train$workingday==1])
#summary(train$atemp)

#aggregate(count ~ hour + humrange, data=train, FUN=function(x) {sum(x)/length(x)})  

fit <- rpart(count ~ hour + working + atemp + season + weather + humrange + windrange, data=test, method="anova")#, control=rpart.control(minsplit=2, cp=0.02))
fancyRpartPlot(fit)

test$prediction <- predict(fit)
rmsle(test$count, test$prediction)

#rmsle: 0.88818

#create submition file
prediction <- predict(fit, testdata)
submit <- data.frame(datetime = testdata$datetime, count = prediction)
head(submit)
submit[submit$datetime > '25/03/2012  01:00:00']
write.csv(submit, file = "regtree.csv", row.names = FALSE)


