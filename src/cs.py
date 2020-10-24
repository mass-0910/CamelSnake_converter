import sys, os
import json

class Converter:

    def __init__(self, filepath: str):

        self.symbol = ["'", "\"", "%", ":", ";", "\\", "#", "@", ".", ",", "(", ")", "[", "]", "{", "}", "+", "-", "*", "/", "^", "=", "<", ">"]
        self.space = [' ', '\t', '\n', '\r']

        self.rule = None
        self.filepath = filepath
        with open(filepath) as fp:
            self.file = fp.readlines()
    
    def readRules(self):
        rule_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "setting.json")
        with open(rule_filepath) as fp:
            self.rule = json.load(fp)
    
    def convert(self):
        # self._backup()
        class_name = self._extractClass()
        var_name = self._extractVar()
        function_name = self._extractFunc()
        with open(self.filepath + ".conv", mode='w') as fp:
            for line in self.file:
                tokenized_line = self._splitPseudoToken(line)
                for token in tokenized_line:
                    out = token
                    if token in class_name:
                        rule_element = "class"
                    elif token in var_name:
                        rule_element = "var"
                    elif token in function_name:
                        rule_element = "func"
                    else:
                        rule_element = None

                    if rule_element:
                        if not self._isSystemToken(token):
                            if self.rule[rule_element] == "camel":
                                out = self._camel(token)
                            elif self.rule[rule_element] == "snake":
                                out = self._snake(token)
                            elif self.rule[rule_element] == "pascal":
                                out = self._pascal(token)
                    fp.write(out)
    
    def _isSystemToken(self, token: str):
        if len(token) > 4:
            if token[0:2] == "__" and token[-2:] == "__":
                return True
        return False

    # def _backup(self):
    #     backup_dir = os.path.join(os.path.dirname(self.filepath), ".cs_backup")
    #     filename = os.path.basename(self.filepath)
    #     file_backup_dir = os.path.join(backup_dir, filename) + "_backup"
    #     if not os.path.exists(file_backup_dir):
    #         os.makedirs(file_backup_dir)
    #     i = 0
    #     while os.path.exists(os.path.join(file_backup_dir, str(i))):
    #         i += 1
    #     backup_filename = os.path.join(file_backup_dir, str(i))
    #     with open(backup_filename, mode='w') as fp:
    #         for line in self.file:
    #             fp.write(line)
    
    def _extractClass(self):
        extracted_name = []
        for sentence in self.file:
            for candidate_token in self._extractNextToken(sentence, "class"):
                if not candidate_token in extracted_name:
                    extracted_name.append(candidate_token)
        return extracted_name
    
    def _extractVar(self):
        extracted_name = []
        for sentence in self.file:
            for candidate_token in self._extractBeforeToken(sentence, "="):
                if not candidate_token in self.symbol and not candidate_token in extracted_name:
                    extracted_name.append(candidate_token)
            for candidate_token in self._extractBeforeToken(sentence, "["):
                if not candidate_token in self.symbol and not candidate_token in extracted_name:
                    extracted_name.append(candidate_token)
            for token in self._splitToken(sentence):
                if token == "def":
                    argument_sentence = ""
                    bracket = 0
                    for char in sentence:
                        if char == "(":
                            bracket += 1
                            continue
                        elif char == ")":
                            bracket -= 1
                            continue
                        if bracket > 0:
                            argument_sentence += char
                    argument_tokens = self._extractNextToken(argument_sentence, ",")
                    if len(self._splitToken(argument_sentence)) > 0:
                        if not self._splitToken(argument_sentence)[0] == "self":
                            argument_tokens.append(self._splitToken(argument_sentence)[0])
                    for candidate_token in argument_tokens:
                        if not candidate_token in self.symbol and not candidate_token in extracted_name:
                            extracted_name.append(candidate_token)
        return extracted_name
    
    def _extractFunc(self):
        extracted_name = []
        for sentence in self.file:
            for candidate_token in self._extractNextToken(sentence, "def"):
                if not candidate_token in extracted_name:
                    extracted_name.append(candidate_token)
        return extracted_name
    
    def _extractNextToken(self, sentence: str, extract_token: str):
        tokenized_sentence = self._splitToken(sentence)
        extraced_tokens = []
        for i, token in enumerate(tokenized_sentence):
            if token == extract_token:
                if len(tokenized_sentence) > i + 1:
                    extraced_tokens.append(tokenized_sentence[i + 1])
        return extraced_tokens

    def _extractBeforeToken(self, sentence: str, extract_token: str):
        tokenized_sentence = self._splitToken(sentence)
        extraced_tokens = []
        for i, token in enumerate(tokenized_sentence):
            if token == extract_token:
                if 0 <= i - 1:
                    extraced_tokens.append(tokenized_sentence[i - 1])
        return extraced_tokens

    def _splitPseudoToken(self, sentence: str):
        retval = []
        buf = ""
        for char in sentence:
            if char.isalpha() or char == '_':
                buf += char
            else:
                if buf:
                    retval.append(buf)
                    buf = ""
                retval.append(char)
        return retval
    
    def _splitToken(self, sentence: str):
        retval = []
        buf = ""
        mode = 0
        escape = False
        for char in sentence:
            if mode == 0:
                if char in self.symbol:
                    if buf:
                        retval.append(buf)
                        buf = ""
                    if char == "\"":
                        buf += char
                        mode = 1
                    elif char == "#":
                        break
                    else:
                        retval.append(char)
                elif char in self.space:
                    if buf:
                        retval.append(buf)
                        buf = ""
                else:
                    buf += char
            elif mode == 1:
                buf += char
                if char == "\"" and not escape:
                    retval.append(buf)
                    buf = ""
                    mode = 0
                elif char == "\\" and not escape:
                    escape = True
                elif escape:
                    escape = False
        if buf:
            retval.append(buf)
            buf = ""
        return retval
    
    def _camel(self, token):
        elements = self._splitElements(token)
        converted_token = ""
        for i, elm in enumerate(elements):
            if i == 0:
                converted_token += elm
            else:
                converted_token += elm.capitalize()
        return converted_token
    
    def _snake(self, token):
        elements = self._splitElements(token)
        converted_token = ""
        for i, elm in enumerate(elements):
            if i == 0:
                converted_token += elm
            else:
                converted_token += "_" + elm
        return converted_token
    
    def _pascal(self, token):
        elements = self._splitElements(token)
        converted_token = ""
        for elm in elements:
            converted_token += elm.capitalize()
        return converted_token

    def _splitElements(self, token: str):
        retval = []
        buf = ""
        for char in token:
            if char.isupper():
                if buf:
                    retval.append(buf)
                    buf = ""
                buf += char.lower()
            elif char == "_":
                if buf:
                    retval.append(buf)
                    buf = ""
            else:
                buf += char
        if buf:
            retval.append(buf)
        return retval

def printUsage():
    print("Usage: cs command <options>")

def printConvertUsage():
    print("Usage: cs convert imput_file")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        printUsage()
        exit(-1)

    if sys.argv[1] == "convert":

        if len(sys.argv) <= 2:
            printConvertUsage()
            exit(-1)
        
        converter = Converter(sys.argv[2])
        converter.readRules()
        converter.convert()