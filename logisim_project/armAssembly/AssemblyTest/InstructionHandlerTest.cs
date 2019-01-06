using NUnit.Framework;
using Assembly;
using System;


namespace AssemblyTest
{

    [TestFixture()]
    public class InstructionHandlerTest
    {
        InstructionHandler ih;
        Range[] ranges;
        [Test()]
        public void Translate()
        {
            Range r1 = new Range(5, 4, "3");
            Range r2 = new Range(3, 2, "#1");
            Range r3 = new Range(1, 0, "#2");
            ranges = new Range[] { r1, r2, r3 };

            ih = new InstructionHandler("test", "test (?<1>[0-9]+) (?<2>[0-9]+)", ranges);

            string line = "test 2 3";

            Assert.AreEqual(0b111011, ih.Translate(line));
        }
    }
}
