using System;
using System.Collections.Generic;
using System.Text;
using System.Runtime.CompilerServices;

namespace DynamicObject
{
    public class DynamicObject
    {
        private Dictionary<string, object> _instance_dict = new Dictionary<string, object>();

        public Dictionary<string, object> container
        {
            get { return _instance_dict; }
        }

        [SpecialName]
        public object GetBoundMember(string name)
        {
            if (!_instance_dict.ContainsKey(name))
            {
                string msg = String.Format("'DynamicObject' has no attribute '{0}'", name);
                throw new System.MissingMemberException(msg);
            } 
            return _instance_dict[name];
        }

        [SpecialName]
        public void SetMemberAfter(string name, object o)
        {
            _instance_dict.Add(name, o);
        }

        [SpecialName]
        public void DeleteMember(string name)
        {
            if (!_instance_dict.ContainsKey(name))
            {
                string msg = String.Format("'DynamicObject' has no attribute '{0}'", name);
                throw new System.MissingMemberException(msg);
            }
            _instance_dict.Remove(name);
        }
    }
}
