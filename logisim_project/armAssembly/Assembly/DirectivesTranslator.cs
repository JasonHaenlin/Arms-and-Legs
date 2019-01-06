using System;
using System.Collections.Generic;
using System.Text;
using System.Text.RegularExpressions;
using System.Xml;

namespace Assembly
{

    public class DirectivesTranslator
    {
        readonly Dictionary<string, int> adresses;
        readonly TypeHandler[] handlers;

        private readonly Regex declarationRegex = new Regex(@"(?<name>[0-9a-zA-Z]+):", RegexOptions.IgnoreCase);
        private readonly Regex labelRegex = new Regex(@"(?<name>[0-9a-zA-Z]+)\n", RegexOptions.IgnoreCase);
        private readonly Regex varRegex = new Regex(@"(?<name>[0-9a-zA-Z]+): (?<a>[.0-9a-zA-Z]+)", RegexOptions.IgnoreCase);

        public DirectivesTranslator(string xmlContent)
        {
            adresses = new Dictionary<string, int>();

            XmlDocument xml = new XmlDocument();
            xml.LoadXml(xmlContent);
            List<TypeHandler> handlerList = new List<TypeHandler>();
            foreach (XmlNode node in xml.DocumentElement.ChildNodes)
            {
                if (node.NodeType == XmlNodeType.Comment)
                    continue;

                XmlNode nameNode = node.ChildNodes.Item(0);
                XmlNode patternNode = node.ChildNodes.Item(1);
                XmlNode offsetNode = node.ChildNodes.Item(2);
                XmlNode replacementsNode = node.ChildNodes.Item(3);

                string name = nameNode.InnerText;
                string pattern = patternNode.InnerText;
                int offsetFactor = int.Parse(offsetNode.InnerText);
                List<string> replacements = new List<string>();
                foreach (XmlNode n in replacementsNode.ChildNodes)
                {
                    string replacement = n.InnerXml;
                    replacements.Add(replacement);
                }
                handlerList.Add(new TypeHandler(name, pattern, offsetFactor, replacements.ToArray()));
            }
            handlers = handlerList.ToArray();
        }

        string[] ParseLabels(string[] lines)
        {
            List<string> newLines = new List<string>();

            int counter = -1; // stating at -1 since we have to increment at the beginning of each loop
            foreach(string line in lines)
            {
                counter++;
                Match labelMatch = declarationRegex.Match(line);
                if (labelMatch.Success)
                {
                    string key = labelMatch.Groups["name"].Value;
                    if (adresses.ContainsKey(key))
                        Console.WriteLine("probably caught an error on line '{0}': duplicate label declaration", line);
                    adresses.Add(key, counter);
                    counter--; // this line will either be removed or replaced
                    continue;
                }
            }
            foreach (string line in lines)
            {
                string l = CleanLine(line);
                foreach (KeyValuePair<string, int> adress in adresses)
                {
                    if (Regex.Match(line, " " + adress.Key + ":").Success)
                    {
                        l = line.Replace(adress.Key, adress.Value.ToString());
                        break;
                    }
                    else if (Regex.Match(line, " " + adress.Key + " ").Success)
                    {
                        l = line.Replace(adress.Key, adress.Value.ToString());
                        break;
                    }
                }
                newLines.Add(l);
            }
            return newLines.ToArray();
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
            lines = ParseLabels(lines);
            List<string> newLines = new List<string>();
            foreach (string line in lines)
            {
                Console.WriteLine(line);
                if (!labelRegex.IsMatch(line) && !varRegex.IsMatch(line))
                    newLines.Add(line); // it's not a declaration
                else if (varRegex.IsMatch(line))
                {
                    foreach (TypeHandler handler in handlers)
                    {
                        try
                        {
                            string[] translation = handler.Translate(line);
                            newLines.AddRange(translation);
                            break;
                        }
                        catch (FormatException)
                        {
                            continue;
                        }
                    }
                }
                else
                {
                    newLines.Add(line);
                }
            }
            return newLines.ToArray(); 
        }
    }
}
