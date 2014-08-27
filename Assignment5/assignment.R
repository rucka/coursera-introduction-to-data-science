#install.packages("caret")
#install.packages("rpart")
#install.packages("tree")
#install.packages("randomForest")
#install.packages("e1071")
#install.packages("ggplot2")

setwd("~/Google Drive/Projects/coursera-introduction-to-data-science/Assignment5")
input <- read.csv("seaflow_21min.csv", header=TRUE, stringsAsFactors=FALSE)
input$pop <- as.factor(input$pop)
summary(input)
#Q1 18146
pop <- input$cell_id[input$pop == "synecho"]

#Q2 39180
summary(input$fsc_small)

#Q3 342.1947
#split data in train and test
splitdata <- function(data)
{
  df <- input
  bound <- floor((nrow(df)/2)*1)         #define % of training and test set
  
  df <- df[sample(nrow(df)), ]           #sample rows 
  train <- df[1:bound, ]              #get training set
  test <- df[(bound+1):nrow(df), ] 
  return (list("train" = train,"test" = test))
}
df <- splitdata(input)
train <- df$train
test <- df$test

mean(train$time)

#Q4 nano-pico
library(ggplot2)
ggplot(input, aes(y=pe,x=chl_small))+ geom_line(aes(group=pop, color=pop),size=2,alpha=0.5)

library(rpart)
library(e1071)
library(randomForest)

prediction <- function(train, test)
{
  fol <- pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small
  
  model <- rpart(fol, method="class", data=train) 
  predictions <- predict(model, newdata=test, type="class")
  res = predictions == test$pop
  err <- sum(res) / nrow(test)
  rpart_list <- list("model" = model, "predictions" = predictions, "result" = res, "err" = err)
  
  model <- randomForest(fol, data=train)
  predictions <- predict(model, newdata=test, type="class")
  res = predictions == test$pop
  err <- sum(res) / nrow(test)
  rforest_list <- list("model" = model, "predictions" = predictions, "result" = res, "err" = err)
  
  model <- svm(fol, data=train)
  predictions <- predict(model, newdata=test, type="class")
  res = predictions == test$pop
  err <- sum(res) / nrow(test)
  svm_list <- list("model" = model, "predictions" = predictions, "result" = res, "err" = err)
  
  return (list("rpart" = rpart_list, "rforest" = rforest_list, "svm" = svm_list))
}
result <- prediction(train, test)

#Q5 crypto
#Q6 5004
#Q7 pe chl_small
print(result$rpart$model)

#Q8 0.8532014
print(result$rpart$err)

#Q9 0.919634
#View(result$rforest$predictions)
print(result$rforest$err)

#Q10 pe chl_small
importance(result$rforest$model)

#Q11 0.9182517
print(result$svm$err)

#Q12 ultra is mistaken for pico
table(pred = result$rpart$predictions, true = test$pop)
table(pred = result$rforest$predictions, true = test$pop)
table(pred = result$svm$predictions, true = test$pop)

#Q13 fsc_big
plot(input$fsc_big)
#plot(input$fsc_small)
#plot(input$chl_big)
#plot(input$fsc_perp)
#plot(input$pe)
#plot(input$chl_small)

#Q14 0.05247578
#cleaned_train <- train[!(train$file_id == 208),]
#cleaned_result <- prediction(cleaned_train, test)

#gain <- cleaned_result$svm$err - result$svm$err 
#print(gain)

#df <- splitdata(input[!(input$file_id == 208),])
train <- train[!(train$file_id == 208),]
test <- test[!(test$file_id == 208),]
cleaned_result <- prediction(train, test)

gain <- cleaned_result$svm$err - result$svm$err 
print(gain)


