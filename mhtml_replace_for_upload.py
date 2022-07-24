import os

#ここをあらかじめ指定する
os.chdir("C:\\Users\\hogehoge\\Downloads") #パス
filename = "hogehoge" #拡張子を含まないファイル名
extension = ".mhtml"
pageend = 6 #掲示板の最後のページ番号（６以上にすること）
dlmonth = "7" #ダウンロードした月
dldate = "23" #ダウンロードした日

#ファイルを開く
with open(filename + extension, "r+") as f:
    #改行を削除
    alltxt = ""
    for i,line in enumerate(f):
        if len(line)>73 and line[-2] == "=":
            addtxt = line[:-2]
        else:
            addtxt = line
        alltxt += addtxt

        if i%10000 == 0:
            print("proceeding " + str(i) + " rows...")

    #別ファイルに出力
    mid_file = filename + "_mid" + extension
    g = open(mid_file, "w")
    g.write(alltxt)
    g.close()  
    print("export reshaped file")
f.close()

with open(mid_file) as f:
    alltxt = f.read()

    #広告を削除
    while True:
        loc_start = alltxt.find('  <center><div style=3D"margin: 10px 0px 10px 0px;">')
        if loc_start == -1:
            break
        loc_end = alltxt.find('</center><div class=3D"spacer"></div>', loc_start) + 37
        alltxt = alltxt[:loc_start] + alltxt[loc_end:]
    print("ad deleted")

    #ページ内リンク用タグつけ
    while True:
        loc_start = alltxt.find('<p class=3D"autopagerize_page_info">')
        if loc_start == -1:
            break
        loc_beforepagenum = alltxt.find('&amp;">', loc_start) + 6
        loc_afterpagenum = alltxt.find('</a>', loc_start)
        loc_end = alltxt.find('</p>', loc_start) + 4
        pagenum = alltxt[loc_beforepagenum + 1:loc_afterpagenum]
        alltxt = alltxt[:loc_start] + '<div id="page' + pagenum + '">page:' + pagenum + '</div>' + alltxt[loc_end:]
    print("link tagging complete")

    #ページ番号へのリンクをつくる
    pagestart = 5
    loc = alltxt.find(' <td align=3D"CENTER" valign=3D"bottom" width=3D"80%">&nbsp;</td>')
    loc = alltxt.find('&nbsp;', loc)
    formertxt = alltxt[:loc] + '=E2=80=BB=E3=81=93=E3=81=AE=E3=83=95=E3=82=A1=E3=82=A4=E3=83=AB=E3=81=AF2022=2F' + dlmonth + '=2F' + dldate + '=E3=81=ABteacup=E6=8E=B2=E7=A4=BA=E6=9D=BF=E3=81=8B=E3=82=89=E3=82=B5=E3=83=AB=E3=83=99=E3=83=BC=E3=82=B8=E3=81=95=E3=82=8C=E3=81=9F=E3=82=82=E3=81=AE=E3=81=A7=E3=81=99=E3=80=82<br>'
    for i in range(pagestart, pageend, 5):
        formertxt = formertxt + '<a href="#page' + str(i) + '">page:' + str(i) + '</a>  '
        if i%50 == 0:
            formertxt = formertxt + '<br>'
    alltxt = formertxt + alltxt[loc:]

    #リンクを有効にするために元のページURL情報を消す
    loc_start = alltxt.find('Snapshot-Content-Location:') + 25
    loc_end = alltxt.find('\n', loc_start)
    alltxt = alltxt[:loc_start] + alltxt[loc_end:]
    loc_start = alltxt.find('Content-Location:') + 16
    loc_end = alltxt.find('\n', loc_start)
    alltxt = alltxt[:loc_start] + alltxt[loc_end:]
    print("link modified")

    #別ファイルに出力
    out_file = filename + "_out" + extension
    g = open(out_file, "w")
    g.write(alltxt)
    g.close()  
f.close()

