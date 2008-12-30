<%@ Control Language="IronPython" CodeFile="MultiDocEditor.ascx.py" Inherits="CustomScriptUserControl" %>
<table>
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