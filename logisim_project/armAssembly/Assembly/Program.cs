using System;
using System.Collections.Generic;
using System.IO;

namespace Assembly
{
    class MainClass
    {
        public static void Main(string[] args)
        {
            //if (!CheckProgramArgs(args)) return;
            string typesXml = "", instructionsXml = "";
            try
            {
                typesXml = File.ReadAllText("TypeSet.xml");
                instructionsXml = File.ReadAllText("InstructionSet.xml");
            }
            catch (FileNotFoundException)
            {
                foreach (string f in Directory.GetFiles(Directory.GetCurrentDirectory()))
                    Console.WriteLine(f);
                Console.WriteLine("Resource files not found (" + Directory.GetCurrentDirectory() + "/TypeSet.xml, " + Directory.GetCurrentDirectory() + "/InstructionSet.xml");
                return;
            }
            DirectivesTranslator directivesTranslator = new DirectivesTranslator(typesXml);
            InstructionsTranslator instructionsTranslator = new InstructionsTranslator(instructionsXml);

            string[] rawFile = File.ReadAllLines(args[0]);
            string[] instructions = directivesTranslator.TranslateFile(rawFile);
            string[] data = instructionsTranslator.TranslateFile(instructions);
            File.WriteAllLines(args[1], data);
        }

        private static bool CheckProgramArgs(string[] args)
        {
            if (args.Length != 2)
            {
                Console.WriteLine("This program takes 2 arguments");
                return false;
            }
            if (!File.Exists(args[0]))
            {
                Console.WriteLine("File " + args[0] + " does not exist.");
                return false;
            }
            return true;
        }

        private static string RemoveComments(string line, char character)
        {
            return line.Split(character)[0];
        }
    }
}
