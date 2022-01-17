# coding: utf-8
import sys
import os

WORKDIR = "PATH_TO_WORKDIR"
INPUTFILEDIR = WORKDIR + "/inputFiles_withjapanesename_removeMinor_percent_withdate"
OUTPUTFILEDIR = WORKDIR + "/inputFiles_withjapanesename_removeMinor_percent_withdate_duplicationRemoved"
sampleID = sys.argv[1]

def main():
    inputFilePath = INPUTFILEDIR + "/" + sampleID + ".mitodb.withJapaneseName.removeMinor.percent.withdate.input"
    
    # ファイルが存在しない場合は例外処理
    if not os.path.exists(inputFilePath):
        print("Not Exists")
        return
    
    inputFile = open(inputFilePath)
    inputFileRowList = inputFile.readlines()
    
    fishList = []
    
    outputFilePath = OUTPUTFILEDIR + "/" + sampleID + ".mitodb.withJapaneseName.removeMinor.percent.withdate.removeDupdication.input"
    outputFile = open(outputFilePath, "w")
    
    # 重複魚種は組成量を統合
    for i,row in enumerate(inputFileRowList):
        if i == 0:
            new_row = row
        else:
            fishName = row.split("\t")[0]
            if fishName in fishList:
                continue
            new_row = row
            fishList.append(fishName)
        
        outputFile.write(new_row)
    
    inputFile.close()
    outputFile.close()
    
if __name__ == '__main__':
    main()
    