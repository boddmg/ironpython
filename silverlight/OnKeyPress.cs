using System;
using System.Windows.Browser;
    

namespace OnKeyPress
{

    [ScriptableType]
    public class OnKeyPress
    {
        [ScriptableMember]
        public string method(int start, int end, string keyChar)
        {
            return this._method(start, end, keyChar);
        }

        public virtual string _method(int start, int end, string keyChar)
        {
            // Override this method
            return "string";
        }
    }
}