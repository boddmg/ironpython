<%@ Page Language="IronPython" CodeFile="viewer.aspx.py" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" >
<head runat="server">
    <title>Multidoc Viewer</title>
</head>
<body>
    <form id="form1" runat="server">
        <table cellspacing="10">
            <tr valign="top">
                <td>
                    <b>Pages:</b><br />
                    <asp:repeater id="pageRepeater" runat="server">
                        <itemtemplate>
                            <asp:linkbutton id="pageLink" runat="server" onclick="pageLink_Click" text="<%# title %>" enabled="<%# currentPage != title %>"/><br />
                        </itemtemplate>
                    </asp:repeater>
                </td>
                <td>
                    <b>Current page</b><br />
                    <h2><asp:label id="pageTitle" runat="server" /></h2>
                    <asp:label id="pageContent" runat="server" /><br />
                </td>
            </tr>
        </table>
    </form>
</body>
</html>
