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

#####START PREDICTION#######
test$prediction <- 0
fit <- rpart(count ~ hour + working + atemp + season + weather + humrange + windrange, data=train, method="anova", control=rpart.control(minsplit=2, cp=0))
#fancyRpartPlot(fit)
test$prediction <- predict(fit, test)
rmsle(test$count, test$prediction)
#rmsle: 0.60624 position 305

#create submit file
prediction <- predict(fit, testdata)
submit <- data.frame(datetime = testdata$datetime, count = prediction)
write.csv(submit, file = "regtree.csv", row.names = FALSE)

#predict registered and casual count
test$prediction <- 0
fit.reg <- rpart(registered ~ hour + working + atemp + season + weather + humrange + windrange, data=train, method="anova", control=rpart.control(minsplit=2, cp=0))
fit.cas <- rpart(casual ~ hour + working + atemp + season + weather + humrange + windrange, data=train, method="anova", control=rpart.control(minsplit=2, cp=0))
test$prediction.registered = predict(fit.reg, test)
test$prediction.casual = predict(fit.cas, test)
test$prediction = test$prediction.registered + test$prediction.casual
rmsle(test$count, test$prediction)

#create submit file
prediction.reg <- predict(fit.reg, testdata)
prediction.cas <- predict(fit.cas, testdata)
prediction = prediction.cas + prediction.reg
submit <- data.frame(datetime = testdata$datetime, count = prediction)
write.csv(submit, file = "regtree_combined.csv", row.names = FALSE)

#use forest
library(party)
set.seed(415)
fit <- cforest(count ~ hour + working + atemp + season + weather + humrange + windrange,
              data = train, controls=cforest_unbiased(ntree=2000, mtry=3))
prediction <- predict(fit, test, OOB=TRUE, type = "response")
rmsle(test$count, test$prediction)
#create submit file
prediction <- predict(fit, testdata, OOB=TRUE, type = "response")
submit <- data.frame(datetime = testdata$datetime, count = prediction)
write.csv(submit, file = "forest.csv", row.names = FALSE)

