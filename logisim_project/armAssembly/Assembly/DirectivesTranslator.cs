using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text.RegularExpressions;
using System.Xml;

namespace Assembly
{

    public class DirectivesTranslator
    {
        readonly List<string> ramLabels;
        readonly List<int> ramAdresses;

        readonly List<string> romLabels;
        readonly List<int> romAdresses;

        readonly Dictionary<string, int> types;

        public DirectivesTranslator(string xmlContent)
        {
            ramLabels = new List<string>();
            ramAdresses = new List<int>();
            romLabels = new List<string>();
            romAdresses = new List<int>();

            types = new Dictionary<string, int>();

            XmlDocument xml = new XmlDocument();
            xml.LoadXml(xmlContent);
            foreach (XmlNode node in xml.DocumentElement.ChildNodes)
            {
                if (node.NodeType == XmlNodeType.Comment)
                    continue;

                XmlNode nameNode = node.ChildNodes.Item(0);
                XmlNode sizeNode = node.ChildNodes.Item(1);

                string name = nameNode.InnerText;
                int size = int.Parse(sizeNode.InnerText);

                types.Add(name, size);
            }
        }

        string[] InitRam(string[] lines)
        {
            string replacement = "sub sp, #<size>\n" +
                                 "mov r<register>, #<value>\n" +
                                 "str r<register>, [sp, #<adress>]\n";

            List<string> result = new List<string>();

            string detectionNoValue = @"(?<label>[a-zA-Z.][0-9a-zA-Z_]+): .(?<type>[a-z]+)";
            string detectionWithValue = @"(?<label>[a-zA-Z.][0-9a-zA-Z_]+): .(?<type>[a-z]+) 0x(?<value>[0-9a-fA-F]+)";

            Regex noValueRegex = new Regex(detectionNoValue);
            Regex valueRegex = new Regex(detectionWithValue);
            int register = 0;
            int value = 0;
            int adress = 0;

            foreach (string line in lines)
            {
                Match noValueMatch = noValueRegex.Match(line);
                Match valueMatch = valueRegex.Match(line);

                if (noValueMatch.Success)
                {
                    string type = noValueMatch.Groups["type"].Value;
                    if (types.ContainsKey(type))
                    {
                        if (valueMatch.Success)
                            value = int.Parse(valueMatch.Groups["value"].Value, NumberStyles.HexNumber);
                        else
                            value = 0;

                        string tmp = replacement.Replace("<size>", types[type].ToString());
                        tmp = tmp.Replace("<register>", register.ToString());
                        tmp = tmp.Replace("<value>", value.ToString());
                        tmp = tmp.Replace("<adress>", adress.ToString());

                        ramLabels.Add(noValueMatch.Groups["label"].Value);
                        ramAdresses.Add(adress);

                        foreach (string tmpline in tmp.Split('\n'))
                            result.Add(tmpline);
                        adress+=types[type];
                    }
                }
                else
                {
                    result.Add(line);
                }
            }
            return result.ToArray();
        }

        string[] ParseLabels(string[] lines)
        {
            string label = @"^(?<label>[a-zA-Z\.][0-9a-zA-Z]*)([ \t:]*$)";
            Regex labelRegex = new Regex(label);

            int counter = 0;
            List<string> result = new List<string>();

            //getting all label declarations

            foreach (string line in lines)
            {
                Match match = labelRegex.Match(line);
                if (match.Success)
                {
                    string lbl = match.Groups["label"].Value;
                    romLabels.Add(lbl);
                    romAdresses.Add(counter);
                    counter--;
                }
                else
                {
                    counter++;
                    result.Add(line); 
                }
            }
            return result.ToArray();
        }

        string[] ReplaceLabels(string[] lines)
        {
            Regex[] labelsRegex = new Regex[ramLabels.Count + romLabels.Count];
            for(int i=0; i<labelsRegex.Length; i++)
            {
                string label = i < ramLabels.Count ? ramLabels[i] : romLabels[i - ramLabels.Count];
                labelsRegex[i] = new Regex("([ ,]*)(?<label>" + label+")");
            }

            List<string> result = new List<string>();

            foreach (string line in lines)
            {
                string newLine = line;
                foreach(Regex regex in labelsRegex)
                {
                    Match match = regex.Match(line);
                    if (match.Success)
                    {
                        string label = match.Groups["label"].Value;
                        if (romLabels.Contains(label))
                        {
                            int index = romLabels.IndexOf(label);
                            int adress = romAdresses[index];
                            newLine = newLine.Replace(label, adress.ToString());
                        }
                        else if (ramLabels.Contains(label))
                        {
                            int index = ramLabels.IndexOf(label);
                            int adress = ramAdresses[index];
                            newLine = newLine.Replace(label, "#" + adress.ToString());
                        }
                    }
                }
                result.Add(newLine);
            }
            return result.ToArray();
        }

        private string CleanLine(string line)
        {
            Regex tabs = new Regex("\t");
            if (tabs.IsMatch(line))
                line = tabs.Replace(line, " ");
            return line;
        }

        public string[] TranslateFile(string[] lines)
        {
            lines = InitRam(lines);
            lines = ParseLabels(lines);
            lines = ReplaceLabels(lines);
            return lines;
        }
    }
}
