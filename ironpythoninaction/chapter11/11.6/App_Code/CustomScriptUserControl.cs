using Microsoft.Web.Scripting.UI;
using Microsoft.Web.Scripting.Util;

public class CustomScriptUserControl: ScriptUserControl {
    protected override void LoadViewState(object savedState) {
        ScriptTemplateControl stc = (this as IScriptTemplateControl).ScriptTemplateControl;
        DynamicFunction f = stc.GetFunction("ScriptLoadViewState");
        if (f == null) {
            base.LoadViewState(savedState);
        } else {
            object baseState = stc.CallFunction(f, savedState);
            base.LoadViewState(baseState);
        }
    }

    protected override object SaveViewState() {
        ScriptTemplateControl stc = (this as IScriptTemplateControl).ScriptTemplateControl;
        DynamicFunction f = stc.GetFunction("ScriptSaveViewState");
        if (f == null) {
            return base.SaveViewState();
        } else {
            object baseState = base.SaveViewState();
            return stc.CallFunction(f, baseState);
        }
    }
}