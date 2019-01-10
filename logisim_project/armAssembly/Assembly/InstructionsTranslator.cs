using System;
using System.Collections.Generic;
using System.Xml;
namespace Assembly
{
    public class InstructionsTranslator
    {
        public InstructionHandler[] Handlers { get; }

        public InstructionsTranslator(string xmlContent)
        {
            XmlDocument xml = new XmlDocument();
            xml.LoadXml(xmlContent);
            List<InstructionHandler> handlerList = new List<InstructionHandler>();
            foreach (XmlNode node in xml.DocumentElement.ChildNodes)
            {
                if (node.NodeType == XmlNodeType.Comment)
                    continue;

                XmlNode nameNode = node.ChildNodes.Item(0);
                XmlNode patternNode = node.ChildNodes.Item(1);
                XmlNode rangesNode = node.ChildNodes.Item(2);

                string name = nameNode.InnerText;
                string pattern = patternNode.InnerText;

                List<Range> commandRanges = new List<Range>();
                foreach (XmlNode n in rangesNode.ChildNodes)
                {
                    int max = int.Parse(n.Attributes.Item(0).InnerXml);
                    int min = int.Parse(n.Attributes.Item(1).InnerXml);
                    string value = n.Attributes.Item(2).InnerXml;

                    commandRanges.Add(new Range(max, min, value));
                }
                handlerList.Add(new InstructionHandler(name, pattern, commandRanges.ToArray()));
            }
            Handlers = handlerList.ToArray();
        }

        public string Translate(string line)
        {
            foreach (InstructionHandler handler in Handlers)
            {
                try
                {
                    return handler.Translate(line).ToString("x4");
                }
                catch (FormatException)
                {
                    continue;
                }
            }
            return "0000";
        }

        public string[] TranslateFile(string[] lines)
        {
            List<string> newLines = new List<string>
            {
                "raw v2.0"
            };
            foreach (string line in lines)
            {
                if (line != "")
                newLines.Add(Translate(line));
            }
            return newLines.ToArray();
        }
    }
}