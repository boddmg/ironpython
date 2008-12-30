<%@ Page Language="IronPython" CodeFile="Container.aspx.py" %>
<%@ register src="MultidocEditor.ascx" tagname="multidoceditor" tagprefix="ipia" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" >
<head runat="server">
    <title>Multidoc Viewer</title>
</head>
<body>
    <form id="form1" runat="server">
    <div>
        <ipia:multidoceditor id="editor" runat="server" Filename="doc.xml" />
    </div>
    </form>
</body>
</html>
