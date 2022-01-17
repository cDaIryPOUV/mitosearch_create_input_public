#!/bin/bash

prefix=$1

#change below Path
tmpdir=${PATH_TO_TMPDIR}
edna_sequence_filedir=${PAHT_TO_SEQUENCEFILEDIR}
blastdb=${PATH_TO_complete_partial_mitogenomes.fa}
outputdir=${WORKDIR}/inputFiles


#create tmp dir
mkdir -p ${tmpdir}/${prefix}

if [ -e ${edna_sequence_filedir}/${prefix}_1.fastq.gz -a -e ${edna_sequence_filedir}/${prefix}_2.fastq.gz ]; then
    #ファイルをコピー(Flashが上手く行かなかった時に使うシーケンスデータ)
    cp ${edna_sequence_filedir}/${prefix}_1.fastq.gz ${tmpdir}/${prefix}

    #解凍(Flashが上手く行かなかった時に使うシーケンスデータ)
    gunzip ${tmpdir}/${prefix}/${prefix}_1.fastq.gz

    #ペアエンドのfastqのセットをシングルエンドのfastqに変換。もしエラー(リード数がペアエンド間で異なるなど)の場合は1側のリードを使う。
    flash ${edna_sequence_filedir}/${prefix}_1.fastq.gz ${edna_sequence_filedir}/${prefix}_2.fastq.gz -d ${tmpdir}/${prefix} -M 300 || mv ${tmpdir}/${prefix}/${prefix}_1.fastq ${tmpdir}/${prefix}/out.extendedFrags.fastq

    #fastqファイルをfastaファイルに変換。
    awk '(NR - 1) % 4 < 2' ${tmpdir}/${prefix}/out.extendedFrags.fastq | sed 's/@/>/' > ${tmpdir}/${prefix}/out.extendedFrags.fasta

    #mitoFishデータベースにBlast検索を行う。
    blastn -num_threads 8 -db ${blastdb} -query ${tmpdir}/${prefix}/out.extendedFrags.fasta -outfmt "6 qseqid sseqid qlen slen pident length mismatch gapopen qstart qend sstart send evalue bitscore staxids stitle" -max_target_seqs 1 -out ${tmpdir}/${prefix}/blast.mitodb.result

    #Inputファイルのヘッダを書き込み(MitoFishデータベースとntデータベースで２つ作成。)
    echo -e "id\t${prefix}.fastq" > ${outputdir}/${prefix}.mitodb.input

    #Inputファイル書き込み
    cat ${tmpdir}/${prefix}/blast.mitodb.result| awk '$3 > 100'|awk '$5 > 90'|awk '$6 / $3 > 0.9'|cut -f 16 |sort |uniq -c |sort -r -n |awk 'BEGIN{OFS="\t"} {c="";for(i=2;i<=NF;i++) c=c $i" "; print c, $1}' >> ${outputdir}/${prefix}.mitodb.input

else
    if [ -e ${edna_sequence_filedir}/${prefix}_1.fastq.gz ]; then

        #ファイルをコピー
        cp ${edna_sequence_filedir}/${prefix}_1.fastq.gz ${tmpdir}/${prefix}

        #解凍
        gunzip ${tmpdir}/${prefix}/${prefix}_1.fastq.gz

        #fastqファイルをfastaファイルに変換。
        awk '(NR - 1) % 4 < 2' ${tmpdir}/${prefix}/${prefix}_1.fastq | sed 's/@/>/' > ${tmpdir}/${prefix}/out.extendedFrags.fasta

        #mitoFishデータベースにBlast検索を行う。
        blastn -num_threads 8 -db ${blastdb} -query ${tmpdir}/${prefix}/out.extendedFrags.fasta -outfmt "6 qseqid sseqid qlen slen pident length mismatch gapopen qstart qend sstart send evalue bitscore staxids stitle" -max_target_seqs 1 -out ${tmpdir}/${prefix}/blast.mitodb.result

        #Inputファイルのヘッダを書き込み(MitoFishデータベースとntデータベースで２つ作成。)
        echo -e "id\t${prefix}.fastq" > ${outputdir}/${prefix}.mitodb.input

        #Inputファイル書き込み
        cat ${tmpdir}/${prefix}/blast.mitodb.result| awk '$3 > 100'|awk '$5 > 90'|awk '$6 / $3 > 0.9'|cut -f 16 |sort |uniq -c |sort -r -n |awk 'BEGIN{OFS="\t"} {c="";for(i=2;i<=NF;i++) c=c $i" "; print c, $1}' >> ${outputdir}/${prefix}.mitodb.input
        
    fi

    if [ -e ${edna_sequence_filedir}/${prefix}_2.fastq.gz ]; then

        #ファイルをコピー
        cp ${edna_sequence_filedir}/${prefix}_2.fastq.gz ${tmpdir}/${prefix}

        #解凍
        gunzip ${tmpdir}/${prefix}/${prefix}_2.fastq.gz

        #fastqファイルをfastaファイルに変換。
        awk '(NR - 1) % 4 < 2' ${tmpdir}/${prefix}/${prefix}_2.fastq | sed 's/@/>/' > ${tmpdir}/${prefix}/out.extendedFrags.fasta

        #mitoFishデータベースにBlast検索を行う。
        blastn -num_threads 8 -db ${blastdb} -query ${tmpdir}/${prefix}/out.extendedFrags.fasta -outfmt "6 qseqid sseqid qlen slen pident length mismatch gapopen qstart qend sstart send evalue bitscore staxids stitle" -max_target_seqs 1 -out ${tmpdir}/${prefix}/blast.mitodb.result

        #Inputファイルのヘッダを書き込み(MitoFishデータベースとntデータベースで２つ作成。)
        echo -e "id\t${prefix}.fastq" > ${outputdir}/${prefix}.mitodb.input

        #Inputファイル書き込み
        cat ${tmpdir}/${prefix}/blast.mitodb.result| awk '$3 > 100'|awk '$5 > 90'|awk '$6 / $3 > 0.9'|cut -f 16 |sort |uniq -c |sort -r -n |awk 'BEGIN{OFS="\t"} {c="";for(i=2;i<=NF;i++) c=c $i" "; print c, $1}' >> ${outputdir}/${prefix}.mitodb.input

    fi

rm -r ${tmpdir}/${prefix}

fi   