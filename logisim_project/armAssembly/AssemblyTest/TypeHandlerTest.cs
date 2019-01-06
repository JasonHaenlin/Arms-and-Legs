using NUnit.Framework;
using Assembly;

namespace AssemblyTest
{
    [TestFixture()]
    public class TypeHandlerTest
    {
        TypeHandler th;

        [Test()]
        public void Translate()
        {
            th = new TypeHandler("a", "a: (?<1>[0-9+])", 4, new string[] { "b /1/ offset", "c /1/ offset" });
            string[] a = th.Translate("a: 5");
            string[] b = th.Translate("a: 6");
            Assert.AreEqual(new string[] { "b #5 #0", "c #5 #0"}, a);
            Assert.AreEqual(new string[] { "b #6 #4", "c #6 #4" }, b);
        }
    }
}
