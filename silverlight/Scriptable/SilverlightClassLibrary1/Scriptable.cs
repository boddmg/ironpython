using System;
using System.Windows;
using System.Windows.Browser;

namespace Scriptable
{
    [ScriptableTypeAttribute]
    public class ScriptableForString
    {
        [ScriptableMemberAttribute]
        public string method(string value)
        {
            return this._method(value);
        }

        public virtual string _method(string value)
        {
            return "hello";
        }
    }

    [ScriptableTypeAttribute]
    public class Scriptable
    {
        [ScriptableMemberAttribute]
        public string method()
        {
            return this._method();
        }

        public virtual string _method()
        {
            return "";
        }
    }

    [ScriptableTypeAttribute]
    public class ScriptableEvent
    {
        [ScriptableMemberAttribute]
        public event EventHandler Event;

        public virtual void OnEvent(ScriptableEventArgs e)
        {
            Event(this, e);
        }
    }


    [ScriptableTypeAttribute]
    public class ScriptableEventArgs : EventArgs
    {
        private string _code;

        [ScriptableMemberAttribute]
        public string code
        {
            get
            {
                return _code;
            }
            set
            {
                _code = value;
            }
        }
    }

}