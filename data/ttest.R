
for (filename in c("MFCz", "NFCz", "RFCz", "MFz", "NFz", "RFz")){
	print(filename)
	#http://stackoverflow.com/questions/14420936/error-in-filefile-rt-invalid-description-argument-in-complete-cases-pro
	path<-paste("C:", "/", filename, ".csv", sep="")
	df<-read.csv(path, header= TRUE)
	ttest<-t.test(df['DZ'], df['HC'])
	print(ttest)
}