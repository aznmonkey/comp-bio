
for (filename in c("MFCz", "NFCz", "RFCz", "MFz", "NFz", "RFz", "MT7", "MT8", "NT7", "NT8", "RT7", "RT8")){
	print(filename)
	#http://stackoverflow.com/questions/14420936/error-in-filefile-rt-invalid-description-argument-in-complete-cases-pro
	path<-paste("C:", "/", filename, ".csv", sep="")
	df<-read.csv(path, header= TRUE)
	ttest<-t.test(df['DZ'], df['HC'])
	print(ttest)
}