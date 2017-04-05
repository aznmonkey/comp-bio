sink("rand.txt", append=FALSE, split=FALSE)

library("igraph")
for (task in c("M", "R", "N")){
	for (subject in c("HC", "DZ")){
		path <- paste(task, subject, sep="")
		df<-read.csv(paste("C:/", path, ".csv", sep=""))

		#http://stackoverflow.com/questions/13706188/importing-csv-file-into-r-numeric-values-read-as-characters

		num_data<-data.frame(data.matrix(df))
		numeric_columns <- sapply(num_data,function(x){as.numeric(x)})

		#http://stackoverflow.com/questions/7615450/getting-a-row-from-a-data-frame-as-a-vector-in-r

		print(path)
		for(i in 1:ncol(numeric_columns)){
			for (j in 1:ncol(numeric_columns)){
				if (i != j){
					print(compare(as.numeric(numeric_columns[,i]), as.numeric(numeric_columns[,j]), method="rand"))
				}
			}
		}
	}
}
