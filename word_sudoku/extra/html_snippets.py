HtmlPage = '''
<!DOCTYPE html>
<html>
   <head>
      <style>
        body {
            font-family: Calibri, sans-serif;
        }
        table {
            border-collapse: collapse;
            font-family: Calibri, sans-serif;
        }

        colgroup, tbody {
            border: solid medium;
        }

        td {
            border: solid thin;
            height: 1.4em;
            width: 1.4em;
            text-align: center;
            padding: 0;
        }

        .arrange-vertical {
            display: flex;
            align-items: center;
            align-self: stretch;
            flex-direction: row;
            column-gap: 30px;
        }

        .arrange-horizontal {
            display: flex;
            align-items: center;
            align-self: stretch;
            flex-direction: column;
            row-gap: 30px;
        }
    </style>
   </head>
   <body leftmargin="50">
      {body-placeholder}
   </body>
</html>
'''

HtmlSudokuTable = '''
    <table>
       <p>{caption}</p>
       <colgroup>
          <col>
          <col>
       </colgroup>
       <colgroup>
          <col>
          <col>
       </colgroup>
       <tbody>
          <tr>
             <td style="background-color:{bg-color-0-0}; color:{color-0-0};">{cell-0-0}</td>
             <td style="background-color:{bg-color-0-1}; color:{color-0-1};">{cell-0-1}</td>
             <td style="background-color:{bg-color-0-2}; color:{color-0-2};">{cell-0-2}</td>
             <td style="background-color:{bg-color-0-3}; color:{color-0-3};">{cell-0-3}</td>
          </tr>
          <tr>
             <td style="background-color:{bg-color-1-0}; color:{color-1-0};">{cell-1-0}</td>
             <td style="background-color:{bg-color-1-1}; color:{color-1-1};">{cell-1-1}</td>
             <td style="background-color:{bg-color-1-2}; color:{color-1-2};">{cell-1-2}</td>
             <td style="background-color:{bg-color-1-3}; color:{color-1-3};">{cell-1-3}</td>
          </tr>
       </tbody>
       <tbody>
          <tr>
             <td style="background-color:{bg-color-2-0}; color:{color-2-0};">{cell-2-0}</td>
             <td style="background-color:{bg-color-2-1}; color:{color-2-1};">{cell-2-1}</td>
             <td style="background-color:{bg-color-2-2}; color:{color-2-2};">{cell-2-2}</td>
             <td style="background-color:{bg-color-2-3}; color:{color-2-3};">{cell-2-3}</td>
          </tr>
          <tr>
             <td style="background-color:{bg-color-3-0}; color:{color-3-0};">{cell-3-0}</td>
             <td style="background-color:{bg-color-3-1}; color:{color-3-1};">{cell-3-1}</td>
             <td style="background-color:{bg-color-3-2}; color:{color-3-2};">{cell-3-2}</td>
             <td style="background-color:{bg-color-3-3}; color:{color-3-3};">{cell-3-3}</td>
          </tr>
       </tbody>
    </table>
'''

ColorPaletteRed = ["#FEBCBC", "#FFC1DC", "#FF6363", "#C70039"]

ColorPaletteBlue = ["#DCFAFF", "#DCE0FF", "#B1DDFF", "#61CFFF"]

ColorPaletteGreen = ["#BAFFC3", "#E1FFA9", "#7BFFAB", "#90C292"]

ColorPaletteBlack = ["#E7E7E7", "#D1D1D1", "#BBCBC2", "#CBBBC7"]

ColorPaletteYellow = ["#FFFF91", "#FFC764", "#FFA175", "#FFB991"]

DarkBlack = "#000000"
DarkRed = "#9E0404"
DarkGreen = "#007053"
White = "#FFFFFF"



