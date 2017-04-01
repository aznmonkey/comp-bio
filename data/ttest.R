sink("ttests.txt", append=FALSE, split=FALSE)
for (channel in c("FCz", "Fz", "T7", "T8", "FC2", "FC6", "Iz", "P7")){
	for (task in c("M", "R", "N")){ 
		print(paste(task, channel, sep=""))
		#http://stackoverflow.com/questions/14420936/error-in-filefile-rt-invalid-description-argument-in-complete-cases-pro
		path<-paste("C:", "/", task, channel, ".csv", sep="")
		df<-read.csv(path, header= TRUE)
		ttest<-t.test(df['DZ'], df['HC'])
		print(ttest)
	}
}

for (task in c("M", "R", "N")){ 
	print(paste(task, "AvgClustCoeffTTest", sep=""))
	path<-paste("C:", "/", task, "AvgClustCoefficiency", ".csv", sep="")
	df<-read.csv(path, header= TRUE)
	ttest<-t.test(df['DZ'], df['HC'])
	print(ttest)
}
