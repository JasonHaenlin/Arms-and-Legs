using System;
using System.Text.RegularExpressions;

namespace Assembly
{
    public class TypeHandler
    {
        private static Regex offRegex = new Regex(@"offset", RegexOptions.IgnoreCase);
        private static Regex valueRegex = new Regex(@"(?<value>/[0-9]+/)", RegexOptions.IgnoreCase);

        private static int offset;
        private int offsetFactor;
        public readonly string name;
        public readonly Regex pattern;
        public readonly string[] replacements;

        public TypeHandler(string name, string pattern, int offsetFactor, string[] replacements)
        {
            this.name = name;
            this.pattern = new Regex(pattern, RegexOptions.IgnoreCase);
            this.offsetFactor = offsetFactor;
            this.replacements = replacements;
        }

        public string[] Translate(string line)
        {
            Match normalMatch = pattern.Match(line);
            if (!normalMatch.Success)
            {
                throw new FormatException(string.Format("Parsing error on line: {0}", line));
            }
            string[] result = new string[replacements.Length];
            for (int i = 0; i < replacements.Length; i++)
            {
                result[i] = replacements[i].Replace("offset", "#" + offset);
                Match valueMatch = valueRegex.Match(replacements[i]);
                if (valueMatch.Success)
                {
                    string toReplace = valueMatch.Groups["value"].Value;
                    int value = int.Parse(new Regex(@"(?<value>[0-9]+)").Match(line).Groups["value"].Value);
                    result[i] = result[i].Replace(toReplace, "#" + value);
                }
            }
            offset += offsetFactor;
            return result;
        }


    }
}
