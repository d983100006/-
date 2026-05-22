Option Explicit

' ==========================================================
' Excel 輕量文獻倉庫：RIS / RefMan → Excel 索引 + PDF 超連結
' 需求：新加入的 RIS 一律新增到最後一列；即使重複也不要覆蓋舊列
' ==========================================================

Private Const SHEET_INDEX As String = "Paper_Index"
Private Const SHEET_DOWNLOAD As String = "Download_List"
Private Const RIS_FOLDER As String = "RIS"
Private Const PDF_FOLDER As String = "PDF"

Private Const HEADER_ROW As Long = 5
Private Const FIRST_DATA_ROW As Long = 6

Public Sub UpdatePaperIndexFromRIS()

    Dim basePath As String
    Dim risPath As String
    Dim pdfPath As String
    Dim fso As Object
    Dim folder As Object
    Dim file As Object
    Dim ws As Worksheet
    Dim wsDown As Worksheet
    Dim importedCount As Long
    Dim skippedCount As Long
    Dim msg As String

    On Error GoTo ErrHandler

    Application.ScreenUpdating = False
    Application.EnableEvents = False

    If Len(ThisWorkbook.Path) = 0 Then
        MsgBox "請先把這個 Excel 存檔成 .xlsm，再執行巨集。", vbExclamation
        GoTo CleanExit
    End If

    basePath = ThisWorkbook.Path
    risPath = basePath & Application.PathSeparator & RIS_FOLDER
    pdfPath = basePath & Application.PathSeparator & PDF_FOLDER

    Set fso = CreateObject("Scripting.FileSystemObject")

    If Not fso.FolderExists(risPath) Then fso.CreateFolder risPath
    If Not fso.FolderExists(pdfPath) Then fso.CreateFolder pdfPath

    Set ws = EnsureSheet(SHEET_INDEX)
    SetupIndexHeader ws

    Set folder = fso.GetFolder(risPath)

    For Each file In folder.Files
        If LCase(fso.GetExtensionName(file.Name)) = "ris" Then
            If ImportOneRISFile_AppendOnly(ws, file.Path, pdfPath) Then
                importedCount = importedCount + 1
            Else
                skippedCount = skippedCount + 1
            End If
        End If
    Next file

    Set wsDown = EnsureSheet(SHEET_DOWNLOAD)
    BuildDownloadList ws, wsDown

    FormatIndexSheet ws
    FormatDownloadSheet wsDown

    msg = "RIS 匯入完成。" & vbCrLf & vbCrLf
    msg = msg & "成功新增：" & importedCount & " 筆" & vbCrLf
    msg = msg & "略過：" & skippedCount & " 筆" & vbCrLf & vbCrLf
    msg = msg & "模式：Append-Only（不覆蓋舊列，重複也新增）"

    MsgBox msg, vbInformation

CleanExit:
    Application.EnableEvents = True
    Application.ScreenUpdating = True
    Exit Sub

ErrHandler:
    MsgBox "執行時發生錯誤：" & vbCrLf & Err.Description, vbCritical
    Resume CleanExit

End Sub

Private Function ImportOneRISFile_AppendOnly(ByVal ws As Worksheet, ByVal risFullPath As String, ByVal pdfFolder As String) As Boolean

    Dim fso As Object
    Dim risText As String
    Dim data As Object
    Dim serialNo As String
    Dim nextRow As Long
    Dim fileBase As String
    Dim pdfFullPath As String
    Dim title As String
    Dim doi As String
    Dim yearText As String
    Dim uniqueKey As String

    On Error GoTo ErrHandler

    Set fso = CreateObject("Scripting.FileSystemObject")

    fileBase = fso.GetBaseName(risFullPath)
    serialNo = ExtractSerialNo(fileBase)
    If Len(serialNo) = 0 Then serialNo = fileBase

    risText = ReadTextFileUTF8(risFullPath)
    If Len(Trim(risText)) = 0 Then
        ImportOneRISFile_AppendOnly = False
        Exit Function
    End If

    Set data = ParseRIS(risText)
    title = GetDictValue(data, "Title")
    doi = NormalizeDOI(GetDictValue(data, "DOI"))
    yearText = GetDictValue(data, "Year")

    If Len(title) = 0 And Len(doi) = 0 Then
        ImportOneRISFile_AppendOnly = False
        Exit Function
    End If

    uniqueKey = BuildUniqueKey(serialNo, doi, title, yearText)

    nextRow = ws.Cells(ws.Rows.Count, GetCol(ws, "No")).End(xlUp).Row + 1
    If nextRow < FIRST_DATA_ROW Then nextRow = FIRST_DATA_ROW

    pdfFullPath = FindPDFBySerial(pdfFolder, fileBase, serialNo)
    If Len(pdfFullPath) = 0 Then
        pdfFullPath = pdfFolder & Application.PathSeparator & fileBase & ".pdf"
    End If

    WriteIndexRow ws, nextRow, serialNo, fileBase, risFullPath, pdfFullPath, data, uniqueKey

    ImportOneRISFile_AppendOnly = True
    Exit Function

ErrHandler:
    ImportOneRISFile_AppendOnly = False

End Function

Private Sub WriteIndexRow(ByVal ws As Worksheet, ByVal rowNo As Long, ByVal serialNo As String, ByVal fileBase As String, ByVal risFullPath As String, ByVal pdfFullPath As String, ByVal data As Object, ByVal uniqueKey As String)

    Dim doi As String
    Dim url As String
    Dim doiUrl As String
    Dim fso As Object
    Dim pdfExists As Boolean
    Dim pdfFileName As String

    Set fso = CreateObject("Scripting.FileSystemObject")

    doi = NormalizeDOI(GetDictValue(data, "DOI"))
    url = GetDictValue(data, "URL")

    If Len(doi) > 0 Then
        doiUrl = "https://doi.org/" & doi
    Else
        doiUrl = ""
    End If

    pdfExists = fso.FileExists(pdfFullPath)
    pdfFileName = fso.GetFileName(pdfFullPath)

    On Error Resume Next
    ws.Cells(rowNo, GetCol(ws, "PDF_Link")).Hyperlinks.Delete
    ws.Cells(rowNo, GetCol(ws, "Source_Link")).Hyperlinks.Delete
    ws.Cells(rowNo, GetCol(ws, "DOI_Link")).Hyperlinks.Delete
    On Error GoTo 0

    SetCell ws, rowNo, "No", serialNo
    SetCell ws, rowNo, "RIS_File", fileBase & ".ris"
    SetCell ws, rowNo, "PDF_File", pdfFileName

    If pdfExists Then
        ws.Hyperlinks.Add ws.Cells(rowNo, GetCol(ws, "PDF_Link")), pdfFullPath, , , "開啟 PDF"
        SetCell ws, rowNo, "PDF_Status", "已找到 PDF"
    Else
        SetCell ws, rowNo, "PDF_Link", "尚未放入 PDF"
        SetCell ws, rowNo, "PDF_Status", "等待 PDF：" & pdfFileName
    End If

    If Len(url) > 0 Then
        ws.Hyperlinks.Add ws.Cells(rowNo, GetCol(ws, "Source_Link")), url, , , "來源網址"
    Else
        SetCell ws, rowNo, "Source_Link", ""
    End If

    If Len(doiUrl) > 0 Then
        ws.Hyperlinks.Add ws.Cells(rowNo, GetCol(ws, "DOI_Link")), doiUrl, , , "DOI"
    Else
        SetCell ws, rowNo, "DOI_Link", ""
    End If

    SetCell ws, rowNo, "Publication_Type", GetDictValue(data, "Type")
    SetCell ws, rowNo, "Authors", GetDictValue(data, "Authors")
    SetCell ws, rowNo, "Year", GetDictValue(data, "Year")
    SetCell ws, rowNo, "Title", GetDictValue(data, "Title")
    SetCell ws, rowNo, "Journal_or_Conference", GetDictValue(data, "Journal")
    SetCell ws, rowNo, "Volume", GetDictValue(data, "Volume")
    SetCell ws, rowNo, "Issue", GetDictValue(data, "Issue")
    SetCell ws, rowNo, "Start_Page", GetDictValue(data, "StartPage")
    SetCell ws, rowNo, "End_Page", GetDictValue(data, "EndPage")
    SetCell ws, rowNo, "Pages", GetDictValue(data, "Pages")
    SetCell ws, rowNo, "DOI", doi
    SetCell ws, rowNo, "URL", url
    SetCell ws, rowNo, "Publisher", GetDictValue(data, "Publisher")
    SetCell ws, rowNo, "Place", GetDictValue(data, "Place")
    SetCell ws, rowNo, "ISSN_ISBN", GetDictValue(data, "SN")
    SetCell ws, rowNo, "Keywords", GetDictValue(data, "Keywords")
    SetCell ws, rowNo, "Abstract", GetDictValue(data, "Abstract")
    SetCell ws, rowNo, "RIS_Path", risFullPath
    SetCell ws, rowNo, "PDF_Path", pdfFullPath
    SetCell ws, rowNo, "Unique_Key", uniqueKey
    SetCell ws, rowNo, "Last_Imported", Format(Now, "yyyy-mm-dd hh:nn:ss")

    PreserveManualCell ws, rowNo, "Method_Tag"
    PreserveManualCell ws, rowNo, "Material_Tag"
    PreserveManualCell ws, rowNo, "Reading_Status"
    PreserveManualCell ws, rowNo, "Downloaded_By"
    PreserveManualCell ws, rowNo, "AI_Notes"
    PreserveManualCell ws, rowNo, "User_Notes"

End Sub

' ======= original helper functions kept =======
Private Function ParseRIS(ByVal risText As String) As Object
    Dim dict As Object, lines() As String, i As Long
    Dim lineText As String, tag As String, valueText As String, currentTag As String
    Set dict = CreateObject("Scripting.Dictionary")
    risText = Replace(Replace(risText, vbCrLf, vbLf), vbCr, vbLf)
    lines = Split(risText, vbLf)
    currentTag = ""
    For i = LBound(lines) To UBound(lines)
        lineText = RTrim(lines(i))
        If Len(lineText) >= 6 And Mid(lineText, 3, 3) = "  -" Then
            tag = UCase(Left(lineText, 2))
            valueText = Trim(Mid(lineText, 7))
            currentTag = tag
            AddRISTag dict, tag, valueText
        ElseIf Len(currentTag) > 0 And Len(Trim(lineText)) > 0 Then
            AddRISTag dict, currentTag, Trim(lineText)
        End If
    Next i
    NormalizeParsedRIS dict, risText
    Set ParseRIS = dict
End Function
Private Sub AddRISTag(ByVal dict As Object, ByVal tag As String, ByVal valueText As String)
    If Len(valueText) = 0 Then Exit Sub
    If dict.Exists(tag) Then dict(tag) = dict(tag) & " ; " & valueText Else dict.Add tag, valueText
End Sub
Private Sub NormalizeParsedRIS(ByVal raw As Object, ByVal risText As String)
    Dim authors As String, title As String, journal As String, yearText As String, doi As String
    Dim pages As String, startPage As String, endPage As String
    authors = FirstNonEmpty(raw, "AU,A1")
    title = FirstNonEmpty(raw, "TI,T1,CT")
    journal = FirstNonEmpty(raw, "JF,JO,JA,T2,BT")
    yearText = ExtractYear(FirstNonEmpty(raw, "PY,Y1,DA"))
    doi = NormalizeDOI(FirstNonEmpty(raw, "DO"))
    If Len(doi) = 0 Then doi = ExtractDOIFromText(risText)
    startPage = FirstNonEmpty(raw, "SP")
    endPage = FirstNonEmpty(raw, "EP")
    If Len(startPage) > 0 And Len(endPage) > 0 Then pages = startPage & "-" & endPage Else pages = FirstNonEmpty(raw, "PG")
    raw("Type") = FirstNonEmpty(raw, "TY"): raw("Authors") = authors: raw("Title") = title
    raw("Journal") = journal: raw("Year") = yearText: raw("DOI") = doi
    raw("Volume") = FirstNonEmpty(raw, "VL"): raw("Issue") = FirstNonEmpty(raw, "IS")
    raw("StartPage") = startPage: raw("EndPage") = endPage: raw("Pages") = pages
    raw("URL") = FirstNonEmpty(raw, "UR,L1,L2"): raw("Publisher") = FirstNonEmpty(raw, "PB")
    raw("Place") = FirstNonEmpty(raw, "CY,PP"): raw("SN") = FirstNonEmpty(raw, "SN")
    raw("Keywords") = FirstNonEmpty(raw, "KW"): raw("Abstract") = FirstNonEmpty(raw, "AB,N2")
End Sub
Private Sub BuildDownloadList(ByVal wsIndex As Worksheet, ByVal wsDown As Worksheet)
    Dim lastRow As Long, r As Long, outRow As Long, noValue As String
    wsDown.Cells.Clear
    wsDown.Cells(1, 1).Value = "No": wsDown.Cells(1, 2).Value = "建議PDF檔名": wsDown.Cells(1, 3).Value = "題名"
    wsDown.Cells(1, 4).Value = "年份": wsDown.Cells(1, 5).Value = "作者": wsDown.Cells(1, 6).Value = "DOI"
    wsDown.Cells(1, 7).Value = "來源網址": wsDown.Cells(1, 8).Value = "給同學的下載說明"
    lastRow = wsIndex.Cells(wsIndex.Rows.Count, GetCol(wsIndex, "No")).End(xlUp).Row
    outRow = 2
    For r = FIRST_DATA_ROW To lastRow
        noValue = Trim(CStr(wsIndex.Cells(r, GetCol(wsIndex, "No")).Value))
        If Len(noValue) > 0 Then
            wsDown.Cells(outRow, 1).Value = noValue
            wsDown.Cells(outRow, 2).Value = noValue & ".pdf"
            wsDown.Cells(outRow, 3).Value = CStr(wsIndex.Cells(r, GetCol(wsIndex, "Title")).Value)
            wsDown.Cells(outRow, 4).Value = CStr(wsIndex.Cells(r, GetCol(wsIndex, "Year")).Value)
            wsDown.Cells(outRow, 5).Value = CStr(wsIndex.Cells(r, GetCol(wsIndex, "Authors")).Value)
            wsDown.Cells(outRow, 6).Value = CStr(wsIndex.Cells(r, GetCol(wsIndex, "DOI")).Value)
            wsDown.Cells(outRow, 7).Value = CStr(wsIndex.Cells(r, GetCol(wsIndex, "URL")).Value)
            wsDown.Cells(outRow, 8).Value = "請從 DOI 或來源網址進入學校訂閱資料庫下載全文 PDF，下載後命名為：" & noValue & ".pdf"
            outRow = outRow + 1
        End If
    Next r
End Sub
Private Sub SetupIndexHeader(ByVal ws As Worksheet)
    Dim headers As Variant, i As Long
    headers = Split("No|RIS_File|PDF_File|PDF_Link|PDF_Status|Source_Link|DOI_Link|Publication_Type|Authors|Year|Title|Journal_or_Conference|Volume|Issue|Start_Page|End_Page|Pages|DOI|URL|Publisher|Place|ISSN_ISBN|Keywords|Abstract|Method_Tag|Material_Tag|Reading_Status|Downloaded_By|AI_Notes|User_Notes|RIS_Path|PDF_Path|Unique_Key|Last_Imported", "|")
    If Len(ws.Cells(1, 1).Value) = 0 Then ws.Cells(1, 1).Value = "文獻倉庫控制區"
    For i = LBound(headers) To UBound(headers)
        If Len(ws.Cells(HEADER_ROW, i + 1).Value) = 0 Then ws.Cells(HEADER_ROW, i + 1).Value = headers(i)
    Next i
End Sub
Private Function FindPDFBySerial(ByVal pdfFolder As String, ByVal fileBase As String, ByVal serialNo As String) As String
    Dim fso As Object, candidate As String, pattern As String, found As String
    Set fso = CreateObject("Scripting.FileSystemObject")
    candidate = pdfFolder & Application.PathSeparator & fileBase & ".pdf": If fso.FileExists(candidate) Then FindPDFBySerial = candidate: Exit Function
    candidate = pdfFolder & Application.PathSeparator & serialNo & ".pdf": If fso.FileExists(candidate) Then FindPDFBySerial = candidate: Exit Function
    pattern = pdfFolder & Application.PathSeparator & serialNo & "*.pdf": found = Dir(pattern)
    If Len(found) > 0 Then FindPDFBySerial = pdfFolder & Application.PathSeparator & found Else FindPDFBySerial = ""
End Function
Private Function ReadTextFileUTF8(ByVal fullPath As String) As String
    Dim stream As Object, fso As Object, ts As Object
    On Error GoTo Fallback
    Set stream = CreateObject("ADODB.Stream")
    stream.Type = 2: stream.Charset = "utf-8": stream.Open: stream.LoadFromFile fullPath
    ReadTextFileUTF8 = stream.ReadText: stream.Close: Exit Function
Fallback:
    Set fso = CreateObject("Scripting.FileSystemObject")
    Set ts = fso.OpenTextFile(fullPath, 1, False)
    ReadTextFileUTF8 = ts.ReadAll: ts.Close
End Function
Private Function EnsureSheet(ByVal sheetName As String) As Worksheet
    Dim ws As Worksheet
    On Error Resume Next: Set ws = ThisWorkbook.Worksheets(sheetName): On Error GoTo 0
    If ws Is Nothing Then Set ws = ThisWorkbook.Worksheets.Add(After:=ThisWorkbook.Worksheets(ThisWorkbook.Worksheets.Count)): ws.Name = sheetName
    Set EnsureSheet = ws
End Function
Private Function GetCol(ByVal ws As Worksheet, ByVal headerName As String) As Long
    Dim lastCol As Long, c As Long
    lastCol = ws.Cells(HEADER_ROW, ws.Columns.Count).End(xlToLeft).Column
    For c = 1 To lastCol
        If CStr(ws.Cells(HEADER_ROW, c).Value) = headerName Then GetCol = c: Exit Function
    Next c
    lastCol = lastCol + 1: ws.Cells(HEADER_ROW, lastCol).Value = headerName: GetCol = lastCol
End Function
Private Sub SetCell(ByVal ws As Worksheet, ByVal rowNo As Long, ByVal headerName As String, ByVal valueText As String)
    ws.Cells(rowNo, GetCol(ws, headerName)).Value = valueText
End Sub
Private Sub PreserveManualCell(ByVal ws As Worksheet, ByVal rowNo As Long, ByVal headerName As String)
    Dim colNo As Long: colNo = GetCol(ws, headerName)
    If Len(ws.Cells(rowNo, colNo).Value) = 0 Then ws.Cells(rowNo, colNo).Value = ""
End Sub
Private Function GetDictValue(ByVal dict As Object, ByVal key As String) As String
    If dict.Exists(key) Then GetDictValue = CStr(dict(key)) Else GetDictValue = ""
End Function
Private Function FirstNonEmpty(ByVal dict As Object, ByVal keyList As String) As String
    Dim keys As Variant, i As Long, k As String
    keys = Split(keyList, ",")
    For i = LBound(keys) To UBound(keys)
        k = Trim(CStr(keys(i)))
        If dict.Exists(k) Then If Len(Trim(CStr(dict(k)))) > 0 Then FirstNonEmpty = Trim(CStr(dict(k))): Exit Function
    Next i
    FirstNonEmpty = ""
End Function
Private Function ExtractSerialNo(ByVal fileBase As String) As String
    Dim i As Long, ch As String, result As String
    For i = 1 To Len(fileBase)
        ch = Mid(fileBase, i, 1)
        If ch Like "[0-9]" Then result = result & ch Else Exit For
    Next i
    ExtractSerialNo = result
End Function
Private Function ExtractYear(ByVal textValue As String) As String
    Dim i As Long, fourChars As String
    For i = 1 To Len(textValue) - 3
        fourChars = Mid(textValue, i, 4)
        If fourChars Like "####" Then If CLng(fourChars) >= 1800 And CLng(fourChars) <= 2200 Then ExtractYear = fourChars: Exit Function
    Next i
    ExtractYear = ""
End Function
Private Function NormalizeDOI(ByVal doiText As String) As String
    Dim x As String
    x = Trim(doiText)
    x = Replace(x, "https://doi.org/", "", , , vbTextCompare)
    x = Replace(x, "http://doi.org/", "", , , vbTextCompare)
    x = Replace(x, "doi:", "", , , vbTextCompare)
    x = Replace(x, "DOI:", "", , , vbTextCompare)
    x = Trim(x)
    Do While Len(x) > 0 And (Right(x, 1) = "." Or Right(x, 1) = "," Or Right(x, 1) = ";")
        x = Left(x, Len(x) - 1)
    Loop
    NormalizeDOI = x
End Function
Private Function ExtractDOIFromText(ByVal textValue As String) As String
    Dim re As Object, matches As Object
    On Error GoTo NoRegex
    Set re = CreateObject("VBScript.RegExp")
    re.pattern = "10\.[0-9]{4,9}/[-._;()/:A-Z0-9]+": re.IgnoreCase = True: re.Global = False
    If re.Test(textValue) Then Set matches = re.Execute(textValue): ExtractDOIFromText = NormalizeDOI(matches(0).Value): Exit Function
NoRegex:
    ExtractDOIFromText = ""
End Function
Private Function NormalizeTitle(ByVal titleText As String) As String
    Dim x As String
    x = LCase(Trim(titleText)): x = Replace(x, vbTab, " "): x = Replace(x, ":", "")
    x = Replace(x, ".", ""): x = Replace(x, ",", ""): x = Replace(x, "-", " ")
    Do While InStr(x, "  ") > 0: x = Replace(x, "  ", " "): Loop
    NormalizeTitle = x
End Function
Private Function BuildUniqueKey(ByVal serialNo As String, ByVal doi As String, ByVal title As String, ByVal yearText As String) As String
    If Len(doi) > 0 Then BuildUniqueKey = "DOI:" & LCase(doi) ElseIf Len(title) > 0 Then BuildUniqueKey = "TITLE_YEAR:" & NormalizeTitle(title) & "_" & yearText Else BuildUniqueKey = "NO:" & serialNo
End Function
Private Sub FormatIndexSheet(ByVal ws As Worksheet)
End Sub
Private Sub FormatDownloadSheet(ByVal ws As Worksheet)
End Sub
