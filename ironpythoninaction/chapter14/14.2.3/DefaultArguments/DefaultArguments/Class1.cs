using System;
using System.Runtime.InteropServices;

namespace DefaultArguments
{
    public class Example
    {
        public static void DefaultValues(string string1, [DefaultParameterValue("default")] string string2,
                                         [DefaultParameterValue("another")] string string3)
        {
            Console.WriteLine("First argument = " + string1);
            Console.WriteLine("Second argument = " + string2);
            Console.WriteLine("Third argument = " + string3);
        }

        public static void OptionalIntegers(int value1, [Optional] int? value2, [Optional] int? value3)
        {
            if (!value2.HasValue) // Could also use value2 = value2 ?? 100
            {
                value2 = 100;
            }
            Console.WriteLine("First argument = {0}", value1);
            Console.WriteLine("Second argument = {0}", value2);
            Console.WriteLine("Third argument = {0}", value3);
        }

        public static void MultipleArguments(params object[] args)
        {
            int len = args.Length;
            Console.WriteLine("You passed in {0} arguments", len);
            for (int i = 0; i < len; i++)
            {
                object arg = args[i];
                Console.WriteLine("Argument {0} is {1}", i, arg);
            }
        }
    }
}
