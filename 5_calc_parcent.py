import sys

WORKDIR = "PATH_TO_WORKDIR"
inputFileDirPath = WORKDIR + "/inputFiles_withjapanesename_removeMinor/"
outputFileDirPath = WORKDIR + "/inputFiles_withjapanesename_removeMinor_percent/"

def main():
    #inputFileを読み込み(カタカナ和名付与済、100read未満のサンプルは除去、1%未満の魚種は除去)
    argv = sys.argv
    try:
        inputFile = open(inputFileDirPath + argv[1] + ".mitodb.withJapaneseName.removeMinor.input")
        rowList = inputFile.readlines()
        
        #リード数合計を算出
        total = 0
        for i, row in enumerate(rowList):
            if i == 0:
                continue
            row = row.split("\t")
            if row[0] == "":
                continue
            try:
                total += int(row[1])
            except:
                pass
            
        print(argv[1],total)
        
        #出力ファイルのPath
        outputFile = open(outputFileDirPath + argv[1] + ".mitodb.withJapaneseName.removeMinor.percent.input", "w")
        
        #ファイル書き込み
        for i, row in enumerate(rowList):
            #Headerを書き込み
            if i == 0:
                outputFile.write(row)
            else:
                # リード割合を計算し、書き込み
                rowSplit = row.split("\t")
                
                if rowSplit[0] == "":
                    continue    
                
                fishName = rowSplit[0]
                readNum = int(rowSplit[1].replace("\n","")) * 100
                
                #リード割合
                readRatio = readNum / total
                
                # 新しい列データの作成
                new_row = rowSplit[0] + "\t" + str(readRatio) + "\n"
                
                outputFile.write(new_row)
        
        outputFile.close()
                
    except:
        return
    
    
if __name__ == '__main__':
    main()
    