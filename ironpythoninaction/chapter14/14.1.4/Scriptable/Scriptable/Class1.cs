using System;
using System.Windows.Browser;

namespace Scriptable
{
    [ScriptableType]
    public class Scriptable
    {
        [ScriptableMember]
        public string method(string value)
        { return this.real(value); }

        public virtual string real(string value)
        { return "override me"; }
    }
}