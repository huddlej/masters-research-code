# Load libraries.
library(ggplot2)

# Load initial data.
data <- read.table("final_data.tab", header=T)

# Prepare calculated columns.
data <- data.frame(data, total_time=data$apple+data$snowberry+data$wall)
data <- data.frame(
    data,
    apple_proportion=data$apple/data$total_time,
    snowberry_proportion=data$snowberry/data$total_time,
    wall_proportion=data$wall/data$total_time
)

# Get rows for R. zephyria only.
rz_data <- data[data$species=="Z",]

# Plot distributions of time spent on different locations.
png("distribution_location_total_time.png", height=400, width=400)
boxplot(rz_data[,c("apple", "snowberry", "wall")], ylab="Total time spent on location (seconds)", xlab="Location")
dev.off()

png("distribution_location_behavior_time.png", height=600, width=600)
boxplot(rz_data[,c("apple_search", "snowberry_search", "apple_rest", "snowberry_rest")],
        ylab="Behavior time spent on location (seconds)", xlab="Location/Behavior")
dev.off()

# Plot means and standard deviations.
locations <- c("apple", "snowberry", "wall")
means <- c(mean(rz_data$apple), mean(rz_data$snowberry), mean(rz_data$wall))
sds <- c(sd(rz_data$apple), sd(rz_data$snowberry), sd(rz_data$wall))

se <- ggplot(times, aes(locations, means, ymin=means-sds, ymax=means+sds, colour=locations))

png("barplot_location_total_time.png", height=500, width=500)
se + geom_pointrange()
dev.off()

# Only count means and std devs for individuals that didn't feed off apple.
rz_nofed_data <- rz_data[rz_data$fed_on_apple=="N",]
locations <- c("apple", "snowberry", "wall")
means <- c(mean(rz_nofed_data$apple), mean(rz_nofed_data$snowberry), mean(rz_nofed_data$wall))
sds <- c(sd(rz_nofed_data$apple), sd(rz_nofed_data$snowberry), sd(rz_nofed_data$wall))
se <- ggplot(times, aes(locations, means, ymin=means-sds, ymax=means+sds, colour=locations))

png("barplot_location_total_time_without_apple_feeders.png", height=500, width=500)
se + geom_pointrange()
dev.off()

# Count fruit searches.
fruit_searches_names <- c("neither fruit", "apple only", "snowberry only", "both fruits")
fruit_searches <- c(
    sum(rz_data$searched_apple=="N" & rz_data$searched_snowberry=="N"),
    sum(rz_data$searched_apple=="Y" & rz_data$searched_snowberry=="N"),
    sum(rz_data$searched_apple=="N" & rz_data$searched_snowberry=="Y"),
    sum(rz_data$searched_apple=="Y" & rz_data$searched_snowberry=="Y")
)
png("fruit_searches.png", height=500, width=500)
qplot(fruit_searches_names, fruit_searches)
dev.off()

# Count individuals of either sex that fed off apple.
females_fed_on_apple <- sum(rz_data$sex=="F" & rz_data$fed_on_apple=="Y")
males_fed_on_apple <- sum(rz_data$sex=="M" & rz_data$fed_on_apple=="Y")
proportion_females_fed_on_apple <- females_fed_on_apple / sum(rz_data$sex=="F")
proportion_males_fed_on_apple <- males_fed_on_apple / sum(rz_data$sex=="M")

# Analysis of uncooperative flies.
uncooperative.matrix <- matrix(
    data=c(2, 11, 30, 38, 2, 8, 13, 17),
    ncol=2,
    dimnames=list(
        c("P.M", "P.F", "Z.M", "Z.F"),
        c("cooperative", "uncooperative")
    )
)
png("cooperative_vs_uncooperative.png")
par(mar=c(5, 4, 2, 2) + 0.1)
dotchart(uncooperative.matrix, xlab="Number of trials")
dev.off()
