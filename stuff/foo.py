from PiStorms import PiStorms
psm = PiStorms()

psm.BAM1.runSecs(1, 100, True)
psm.BAM2.runSecs(1, 100, True)
while psm.BAM1.pos()<1990 and psm.BAM2.pos()<1990:
	psm.screen.termPrintln(str(psm.BAM1.pos()) + '  ' + psm.BAM2.pos())
	pass

