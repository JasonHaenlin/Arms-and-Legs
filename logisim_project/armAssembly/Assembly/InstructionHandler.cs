using System;
using System.Text.RegularExpressions;

namespace Assembly
{
    public class InstructionHandler
    {
        public readonly static Regex numberRegex = new Regex("#(?<value>[0-9]+)", RegexOptions.IgnoreCase);

        public readonly string name;
        public readonly Regex pattern;
        public readonly Range[] range;

        public InstructionHandler(string name, string pattern, Range[] range)
        {
            this.name = name;
            this.pattern = new Regex(pattern, RegexOptions.IgnoreCase);
            this.range = range;
        }

        public int Translate(string line)
        {
            line = CleanLine(line);
            Match normalMatch = pattern.Match(line);
            if (!normalMatch.Success)
            {
                throw new FormatException(string.Format("Parsing error on line: {0}", line));
            }
            int result = 0;
            for (int i = 0; i < range.Length; i++)
            {
                Match specialMatch = numberRegex.Match(range[i].value);
                int value = 0;
                if (specialMatch.Success)
                {
                    string id = specialMatch.Groups["value"].Value;
                    value = int.Parse(normalMatch.Groups[id].Value);
                }
                else
                    value = int.Parse(range[i].value);
                result = ApplyValue(result, value, range[i].max, range[i].min);
            }
            return result;
        }

        private string CleanLine(string line)
        {
            Regex multipleSpace = new Regex("[ ]{2,}");
            Regex spaceAfterBracket = new Regex("\\x5B ");
            Regex spaceBeforeBracket = new Regex(" \\x5D");
            Regex spaceBeforeComma = new Regex(" ,");
            if (multipleSpace.IsMatch(line))
                line = multipleSpace.Replace(line, " ");
            if (spaceAfterBracket.IsMatch(line))
                line = spaceAfterBracket.Replace(line, "[");
            if (spaceBeforeBracket.IsMatch(line))
                line = spaceBeforeBracket.Replace(line, "]");
            if (spaceBeforeComma.IsMatch(line))
                line = spaceBeforeComma.Replace(line, ",");

            return line;
        }

        private int ApplyValue(int initial, int input, int max, int min)
        {
            int result = initial;
            int mask = input * 1 << min;
            for (int i = min; i <= max; i++)
            {
                bool a = (initial & (1 << i)) != 0;
                bool b = (mask & (1 << i)) != 0;
                if (b && !a)
                    result += (1 << i);
                else if (!b && a)
                    result -= (1 << i);
            }
            return result;
        }
    }

    public struct Range
    {
        public readonly int max;
        public readonly int min;
        public readonly string value;

        public Range(int max, int min, string value)
        {
            this.max = max;
            this.min = min;
            this.value = value;
        }
    }
}
