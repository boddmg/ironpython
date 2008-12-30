using Microsoft.Web.Scripting.UI;
using Microsoft.Web.Scripting.Util;

public class CustomScriptPage: ScriptPage {

    protected override void LoadViewState(object savedState) {
        DynamicFunction f = this.ScriptTemplateControl.GetFunction("ScriptLoadViewState");
        if (f == null) {
            base.LoadViewState(savedState);
        } else {
            object baseState = this.ScriptTemplateControl.CallFunction(f, savedState);
            base.LoadViewState(baseState);
        }
    }

    protected override object SaveViewState() {
        DynamicFunction f = this.ScriptTemplateControl.GetFunction("ScriptSaveViewState");
        if (f == null) {
            return base.SaveViewState();
        } else {
            object baseState = base.SaveViewState();
            return this.ScriptTemplateControl.CallFunction(f, baseState);
        }
    }
}