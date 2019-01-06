using NUnit.Framework;
using Assembly;

namespace AssemblyTest
{
    [TestFixture()]
    public class InstructionTranslatorTest
    {
        InstructionsTranslator it;
        InstructionHandler[] handlers;
        string xmlContent;

        [Test()]
        public void TestCase()
        {
            xmlContent =
                "<?xml version='1.0' encoding='UTF-8'?>\n" +
                "<instructions>\n" +
                "    <command>\n" +
                "        <name>a</name>\n" +
                "        <pattern>a</pattern>\n" +
                "        <ranges>\n" +
                "            <range max='0' min='0' value='0'></range>\n" +
                "        </ranges>\n" +
                "    </command>\n" +
                "    <command>\n" +
                "        <name>b</name>\n" +
                "        <pattern>b</pattern>\n" +
                "        <ranges>\n" +
                "            <range max='1' min='1' value='1'></range>\n" +
                "        </ranges>\n" +
                "    </command>\n" +
                "</instructions>";

            handlers = new InstructionHandler[] {
                new InstructionHandler("a", "a", new Range[]{new Range(0, 0, "0")}),
                new InstructionHandler("b", "b", new Range[]{new Range(1, 1, "1")})
                };

            it = new InstructionsTranslator(xmlContent);
            Assert.AreEqual(handlers[0].name, it.Handlers[0].name);
            Assert.AreEqual(handlers[0].pattern.ToString(), it.Handlers[0].pattern.ToString());
            Assert.AreEqual(handlers[0].range, it.Handlers[0].range);
            Assert.AreEqual(handlers[1].name, it.Handlers[1].name);
            Assert.AreEqual(handlers[1].pattern.ToString(), it.Handlers[1].pattern.ToString());
            Assert.AreEqual(handlers[1].range, it.Handlers[1].range);
            //Assert.AreSame(handlers, it.Handlers);
        }
    }
}
