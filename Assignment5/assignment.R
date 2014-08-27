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
df <- input
bound <- floor((nrow(df)/2)*1)         #define % of training and test set

df <- df[sample(nrow(df)), ]           #sample rows 
train <- df[1:bound, ]              #get training set
test <- df[(bound+1):nrow(df), ] 

mean(train$time)

#Q4 nano-pico
library(ggplot2)
ggplot(input, aes(y=pe,x=chl_small))+ geom_line(aes(group=pop, color=pop),size=2,alpha=0.5)

#Q5 crypto
#Q6 5004
#Q7 pe chl_small
library(rpart)
fol <- pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small
model <- rpart(fol, method="class", data=train)
print(model)
#library(rattle)
#fancyRpartPlot(model)

#Q8 0.8532014
predictions <- predict(model, newdata=test, type="class")
#head(predictions)
res = predictions == test$pop
sum(res) / nrow(test)
predictions_rpart <- predictions

#Q9 0.919634
model <- randomForest(fol, data=train)
predictions <- predict(model, newdata=test, type="class")
#View(predictions)
#head(predictions)
res = predictions == test$pop
sum(res) / nrow(test)
predictions_rforest <- predictions

#Q10 pe chl_small yes
importance(model)

#Q11 0.9182517
library(e1071)
model <- svm(fol, data=train)
predictions <- predict(model, newdata=test, type="class")
#head(predictions)
res = predictions == test$pop
svm_res = sum(res) / nrow(test)
svm_res
predictions_svm <- predictions

#Q12 ultra is mistaken for pico
table(pred = predictions_rpart, true = test$pop)
table(pred = predictions_rforest, true = test$pop)
table(pred = predictions_svm, true = test$pop)

#Q13 fsc_big
plot(df$fsc_big)
#plot(df$fsc_small)
#plot(df$chl_big)
#plot(df$fsc_perp)
#plot(df$pe)
#plot(df$chl_small)

#Q14 0.0009776823 (wrong)
df <- input[!(train$file_id == 208),]
bound <- floor((nrow(df)/2)*1)         #define % of training and test set

df <- df[sample(nrow(df)), ]           #sample rows 
train <- df[1:bound, ]              #get training set
test <- df[(bound+1):nrow(df), ] 
 
model <- svm(fol, data=train)
predictions <- predict(model, newdata=test, type="class")
#head(predictions)
res = predictions == test$pop
svm_res2 = sum(res) / nrow(test)
(svm_res2 - svm_res)

