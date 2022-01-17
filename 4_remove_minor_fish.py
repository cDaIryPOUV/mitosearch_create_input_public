# coding: utf-8
import sys

WORKDIR = "PATH_TO_WORKDIR"
inputFileDirPath = WORKDIR + "/inputFiles_with_japanesename/"
outputFileDirPath = WORKDIR + "/inputFiles_withjapanesename_removeMinor/"

def main():
    argv = sys.argv
    inputFile = open(inputFileDirPath + argv[1] + ".mitodb.withJapaneseName.input")

    rowList = inputFile.readlines()
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
    
    # 組成全体で100リード未満のサンプルはノイズの影響を大きく受けると考えて除去した
    print(argv[1], total)
    if total < 100:
        print("finish")
        return
    
    outputFile = open(outputFileDirPath + argv[1] + ".mitodb.withJapaneseName.removeMinor.input", "w")
    
    for i, row in enumerate(rowList):
        if i == 0:
            row = row.replace("\tjapaneseName","")
            outputFile.write(row)
            # print(row)
        else:
            rowSplit = row.split("\t")
            if rowSplit[0] == "":
                continue
            
            # 組成で占める割合が1%未満の魚種はノイズである可能性を考慮して除去した。
            if int(rowSplit[1]) / total > 0.01:
                scientificName = rowSplit[0]
                scientificName = scientificName.split("|")[2]
                scientificName = scientificName.split("(")[0]
                if rowSplit[2] != ".\n":
                    japaneseName = rowSplit[2].replace("\n","")
                    new_row = japaneseName + ":" + scientificName + "\t" + rowSplit[1] + "\n"
                    outputFile.write(new_row)
                    # print(new_row)
                else:
                    new_row = scientificName + "\t" + rowSplit[1] + "\n"
                    outputFile.write(new_row)
                    # print(new_row)

    
    outputFile.close()
    
    inputFile.close()


if __name__ == "__main__":
    main()