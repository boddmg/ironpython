<%@ Page Language="IronPython" CodeFile="editor.aspx.py" Inherits="CustomScriptPage" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" >
<head runat="server">
    <title>Multidoc Editor</title>
</head>
<body>
    <form id="form1" runat="server">
    <div>
        <table cellspacing="10">
            <tr valign="top">
                <td>
                    <b>Pages:</b><br />
                    <asp:repeater id="pageRepeater" runat="server">
                        <itemtemplate>
                            <asp:linkbutton id="pageLink" runat="server" onclick="pageLink_Click" text="<%# title %>" enabled="<%# self.currentPage != title %>"/><br />
                        </itemtemplate>
                    </asp:repeater>
                </td>
                <td>
                    <b>Current page</b><br />
                    <asp:panel id="viewPanel" runat="server" visible="false">
                        <h2><asp:label id="pageTitle" runat="server" /></h2>
                        <asp:label id="pageContent" runat="server" /><br />
                        <asp:button id="editButton" runat="server" text="Edit this page" onclick="editButton_Click" />
                    </asp:panel>
                    <asp:panel id="editPanel" runat="server" visible="false">
                        <asp:textbox id="pageTitleTextBox" runat="server" columns="40" ontextchanged="pageTitleTextBox_TextChanged" /><br />
                        <asp:textbox id="pageContentTextBox" runat="server" textmode="multiline" columns="40" height="100" ontextchanged="pageContentTextBox_TextChanged" /><br />
                        <asp:button id="cancelButton" runat="server" text="Cancel" onclick="cancelButton_Click" />
                        <asp:button id="saveButton" runat="server" text="Save" onclick="saveButton_Click" />
                    </asp:panel>
                </td>
            </tr>
        </table>
    </div>
    <asp:Label ID="output" runat="server" />
    </form>
</body>
</html>
