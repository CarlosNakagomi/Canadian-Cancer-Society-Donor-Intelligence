# PBIP Portability Notes

The original working PBIP used a local Windows path to the Power BI staging workbook. In this publication copy, personal absolute paths were removed from text-based PBIP/TMDL files.

The copied staging workbook is located at:

```text
powerbi/data/PowerBI_Data.xlsx
```

Power BI Desktop requires `File.Contents` paths to be absolute at runtime. The copied semantic model therefore defines a Power Query text parameter:

```text
PowerBIWorkbookPath
```

All workbook-loading queries call:

```powerquery
File.Contents(PowerBIWorkbookPath)
```

After cloning the repository, open the PBIP and set `PowerBIWorkbookPath` through **Transform data** > **Edit parameters** to the absolute local path of:

```text
<repo-root>\powerbi\data\PowerBI_Data.xlsx
```

This does not change analytical values; it only reconnects the imported aggregate tables. Avoid committing a personal absolute path after setting the parameter locally.

The original working project was not modified.
