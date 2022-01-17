# coding: utf-8
import xlrd
import sys

japanese_name_filePath = "PATH_TO_20210718_JAFList.xlsx"

WORKDIR = "PATH_TO_WORKDIR"

inputFileDirPath = WORKDIR + "/inputFiles/"
outputFileDirPath = WORKDIR + "/inputFiles_with_japanesename/"

def main():
    # SRRIDを取得
    ID = sys.argv[1]
    
    # Xlrdモジュールで和名が記載されたExcelファイルを開く
    fishname_wb = xlrd.open_workbook(japanese_name_filePath)
    
    # シートを取得
    fishname_sh = fishname_wb.sheet_by_index(0)
    
    # 学名のリストと和名のリストを取得
    academic_nameList = fishname_sh.col_values(4)
    japanese_namesList = fishname_sh.col_values(3)
    
    # Excelの長さを取得
    sh_len = len(academic_nameList)
    
    # Inputファイルを開く
    input_f = open(inputFileDirPath + ID + ".mitodb.input")
    
    # 各行をリストとして取得
    inputRowList = input_f.readlines()
    
    # 和名付きinputファイルのパスを指定
    output_f = open(outputFileDirPath + ID + ".mitodb.withJapaneseName.input", "w")
    
    # Headerを作成
    header = inputRowList[0].replace("\n", "")
    header = header + "\t" + "japaneseName" + "\n"
    
    # Headerを書き込み
    output_f.write(header)
    
    # inputファイルの各行に対して、和名を検索
    for row in inputRowList:
        # 種名を取得
        species = row.split("\t")[0]
        
        # 1行目を処理から除去
        if species == "id":
            continue
        
        # デフォルトの和名に.を割り当てる
        japanese_name = "."
        
        # 和名リストの各行に対して検索を行い、ヒットしたものに置換
        for i in range(sh_len):   
            academic_name = academic_nameList[i].split()[:2]
                
            # 学名にマッチするものを検索
            if academic_name[0] in species and academic_name[1] in species:
                
                # マッチした学名に対応する和名を取得
                japanese_name = japanese_namesList[i]
                break
        
        # 新しく書き込む列を作成
        new_row = row.replace("\n", "")
        new_row = new_row + "\t" + japanese_name + "\n"
        
        # 新しい列を和名付きInputファイルに書き込み
        output_f.write(new_row)
    
    # Inputファイルを閉じる
    input_f.close()
    
    # 和名付きInputファイルを閉じる
    output_f.close()

if __name__ == "__main__":
    main()