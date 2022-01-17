import sys
import subprocess

WORKDIR = "PATH_TO_WORKDIR"

inputFileDirPath = WORKDIR + "/inputFiles_withjapanesename_removeMinor_percent/"
outputFileDirPath = WORKDIR + "/inputFiles_withjapanesename_removeMinor_percent_withdate/"

sampleDataFilePath = WORKDIR + "/lat-long-date.txt"

def main():
    # 割合に変換済みのInputファイルを読み込み
    sampleID = sys.argv[1]
    try:
        inputFile = open(inputFileDirPath + sampleID + ".mitodb.withJapaneseName.removeMinor.percent.input")
        rowList = inputFile.readlines()
        
        # sample情報が格納されたファイルをからサンプル情報をgrep
        sampleData = subprocess.check_output(["grep", sampleID, sampleDataFilePath])
        sampleDate = sampleData.decode().split("\t")[2].replace("\n","")
        
        # 出力ファイル
        outputFile = open(outputFileDirPath + sampleID + ".mitodb.withJapaneseName.removeMinor.percent.withdate.input", "w")
            
        for i,row in enumerate(rowList):
            if i == 0:
                row = row.replace("id", sampleDate)
                outputFile.write(row)
            else:
                outputFile.write(row)
        
        inputFile.close()
        outputFile.close()
    
    except:
        pass
        
if __name__ == '__main__':
    main()
