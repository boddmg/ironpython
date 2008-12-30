using System;
using System.Collections;
namespace PythonExtension
{

    public delegate int Callback(int input);


    public class PythonClass : IEnumerable
    {
        private int _value;
        private Callback _callback;
        public PythonClass(int value, Callback callback)
        {
            _value = value;
            _callback = callback;

        }

        public override string ToString()
        {
            return String.Format("PythonClass<{0}>", _value);
        }

        public IEnumerator GetEnumerator()
        {
            for (int i = _value; i > 0; i--)
            {
                if (i % 2 == 0)
                {
                    yield return _callback(i);
                }
            }
        }

        public static PythonClass operator +(PythonClass a, PythonClass b)
        {
            return new PythonClass(a._value + b._value, a._callback);
        }

        public Object this[Object index] {
            get { 
                Console.WriteLine("Indexed with {0}", index);
                return index;
            }
            set {
                Console.WriteLine("Index {0} set to {1}", index, value);
            }
        }
    }
}
