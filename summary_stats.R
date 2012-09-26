# Load libraries.
library(ggplot2)

# Define functions.
total.time.distribution <- function (data) {
    return(boxplot(data[,c("apple", "snowberry", "wall")],
                   ylab="Total time spent on location (seconds)",
                   xlab="Location"))
}

behavior.time.distribution <- function (data) {
    return(boxplot(data[,c("apple.search", "snowberry.search", "apple.rest", "snowberry.rest")],
                   ylab="Behavior time spent on location (seconds)",
                   xlab="Location/Behavior"))
}

calculate.means <- function (data) {
    return(c(mean(data$apple), mean(data$snowberry), mean(data$wall)))
}

calculate.stddevs <- function (data) {
    return(c(sd(data$apple), sd(data$snowberry), sd(data$wall)))
}

count.fruit.searches <- function (data) {
    return(c(
        sum(data$searched.apple=="N" & data$searched.snowberry=="N"),
        sum(data$searched.apple=="Y" & data$searched.snowberry=="N"),
        sum(data$searched.apple=="N" & data$searched.snowberry=="Y"),
        sum(data$searched.apple=="Y" & data$searched.snowberry=="Y")
    ))
}

count.apple.feeders <- function (data) {
    females.fed.on.apple <- sum(data$sex=="F" & data$fed.on.apple=="Y")
    males.fed.on.apple <- sum(data$sex=="M" & data$fed.on.apple=="Y")

    return(list(
        female=females.fed.on.apple,
        male=males.fed.on.apple,
        proportion.female=(females.fed.on.apple / sum(data$sex=="F")),
        proportion.male=(males.fed.on.apple / sum(data$sex=="M"))
    ))
}

plot.logFC <- function (data) {
    return(ggplot(data, aes(x=logFC.total.time, fill=sex)))
}

# Load initial data.
data <- read.table("final_data.tab", header=T)

# Prepare calculated columns.
data <- data.frame(data, total.time=data$apple+data$snowberry+data$wall)
data <- data.frame(
    data,
    apple.proportion=data$apple/data$total.time,
    snowberry.proportion=data$snowberry/data$total.time,
    wall.proportion=data$wall/data$total.time,
    logFC.total.time=log((data$apple + 1) / (data$snowberry + 1))
)

# Get rows for R. zephyria only.
rz.data <- data[data$species=="Z",]

# Plot distributions of time spent on different locations.
png("figures/distribution_location_total_time.png", height=400, width=400)
total.time.distribution(rz.data)
dev.off()

png("figures/distribution_location_behavior_time.png", height=600, width=600)
behavior.time.distribution(rz.data)
dev.off()

# Plot means and standard deviations.
locations <- c("apple", "snowberry", "wall")
means <- calculate.means(rz.data)
sds <- calculate.stddevs(rz.data)
times <- data.frame(location=locations, mean=means, sd=sds)

png("figures/barplot_location_total_time.png", height=500, width=500)
se <- ggplot(times, aes(locations, means, ymin=means-sds, ymax=means+sds, colour=locations))
se + geom_pointrange()
dev.off()

# Only count means and std devs for individuals that didn't feed off apple.
means <- calculate.means(rz.data[rz.data$fed.on.apple=="N",])
sds <- calculate.stddevs(rz.data[rz.data$fed.on.apple=="N",])

png("figures/barplot_location_total_time_without_apple_feeders.png", height=500, width=500)
se <- ggplot(times, aes(locations, means, ymin=means-sds, ymax=means+sds, colour=locations))
se + geom_pointrange()
dev.off()

# Count fruit searches.
fruit.searches.names <- c("neither fruit", "apple only", "snowberry only", "both fruits")
fruit.searches <- count.fruit.searches(rz.data)

png("figures/fruit_searches.png", height=500, width=500)
qplot(fruit.searches.names, fruit.searches)
dev.off()

# Count individuals of either sex that fed off apple.
apple.feeders <- count.apple.feeders(data)
females.fed.on.apple <- apple.feeders$female
males.fed.on.apple <- apple.feeders$male
proportion.females.fed.on.apple <- apple.feeders$proportion.female
proportion.males.fed.on.apple <- apple.feeders$proportion.male

# Analysis of uncooperative flies.
uncooperative.matrix <- matrix(
    data=c(2, 11, 30, 38, 2, 8, 13, 17),
    ncol=2,
    dimnames=list(
        c("P.M", "P.F", "Z.M", "Z.F"),
        c("cooperative", "uncooperative")
    )
)
png("figures/cooperative_vs_uncooperative.png")
par(mar=c(5, 4, 2, 2) + 0.1)
dotchart(uncooperative.matrix, xlab="Number of trials")
dev.off()

png("figures/distribution_of_total_time_logFC.png")
qplot(data$logFC.total.time, geom="histogram", binwidth=0.5)
dev.off()

png("figures/distribution_of_total_time_logFC_by_sex.png")
hist.time <- plot.logFC(rz.data)
hist.time + geom_bar(position="dodge", binwidth=0.5)
dev.off()
