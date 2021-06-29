# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 11:14:41 2021

@author: VTCS1783261
"""

#C:\Users\vtcs1783261\Desktop\Modified_Perl\perlang_tokenizer.py

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 11:38:45 2021

@author: VTCS1783261
"""

import re
import unicodedata
from collections import namedtuple
import tokenize
import six
import preprocessing.src.perlang_tokenizer as javalang_tok
import random

# JAVA_TOKEN2CHAR = {'STOKEN0': "#",
#                    'STOKEN1': "/*",
#                    'STOKEN2': "*/",
#                    'STOKEN3': "/**",
#                    'STOKEN4': "**/",
#                    'STOKEN5': '"""',
#                    'STOKEN6': '\\n'
#                    }
# JAVA_CHAR2TOKEN = {'#': ' STOKEN0 ',
#                    "/*": ' STOKEN1 ',
#                    "*/": ' STOKEN2 ',
#                    "/**": ' STOKEN3 ',
#                    "**/": ' STOKEN4 ',
#                    '"""': ' STOKEN5 ',
#                    '\\n': ' STOKEN6 '
                   # }
JAVA_TOKEN2CHAR = {'STOKEN0': '#',
                     'STOKEN1': "\\n",
                     'STOKEN2': '"""',
                     'STOKEN3': "'''"
                     }

JAVA_CHAR2TOKEN = {'#': ' STOKEN0 ',
                     "\\n": ' STOKEN1 ',
                     '"""': ' STOKEN2 ',
                     "'''": ' STOKEN3 '
                     }


TESTS = []

TESTS.append((
    r"""
public class HelloWorld
{
 	public void main(String[] args) {
		System.out.println("Hello \n World!");
 	}
}""",
    ['public', 'class', 'HelloWorld', '{',
        'public', 'void', 'main', '(', 'String', '[', ']', 'args', ')', '{',
        'System', '.', 'out', '.', 'println', '(', '" Hello ▁ \\n ▁ World ! "', ')', ';', '}', '}']
))
TESTS.append((r"""
overload((byte)1);
overload(1L);
overload(1.0f);""",
              ['overload', '(', '(', 'byte', ')', '1', ')', ';',
                'overload', '(', '1L', ')', ';',
                'overload', '(', '1.0f', ')', ';']
              ))

TESTS.append((r"""Runnable r = ()-> System.out.print("Run method");""",
              ['Runnable', 'r', '=', '(', ')', '->',
               'System', '.', 'out', '.', 'print', '(', '" Run ▁ method "', ')', ';']))

def process_string(tok, char2tok, tok2char, is_comment):
    if is_comment:
        tok = re.sub(' +', ' ', tok)
        tok = re.sub(r"(.)\1\1\1\1+", r"\1\1\1\1\1", tok)
        if len(re.sub(r'\W', '', tok)) < 2:
            return ''
    tok = tok.replace(' ', ' ▁ ')
    for char, special_token in char2tok.items():
        #print(char)
        #print(special_token)
        tok = tok.replace(char, special_token)
    if tok.startswith(' STOKEN0'):
        if tok.endswith('\n'):
            tok = tok[:-1]
        tok += ' ENDCOM'
    tok = tok.replace('\n', ' STRNEWLINE ')
    tok = tok.replace('\t', ' TABSYMBOL ')
    tok = re.sub(' +', ' ', tok)
    tok = re.sub(' +', ' ', tok)
    for special_token, char in tok2char.items():
        tok = tok.replace(special_token, char)
    tok = tok.replace('\r', '')
    #
    #print(tok)
    return tok


def test_java_tokenizer_discarding_comments():
    for i, (x, y) in enumerate(TESTS):
        y_ = tokenize_java(x)
        if y_ != y:
            line_diff = [j for j, (line, line_) in enumerate(
                zip(y, y_)) if line != line_]
            line_diff = line_diff[-1] if len(line_diff) > 0 else -1
            raise Exception(
                f"Difference at {line_diff}\nExpected:\n==========\n{y}\nbut found:\n==========\n{y_}")

def tokenize_java(s, keep_comments=False):
    
    tokens = []
    assert isinstance(s, str)
    #print (s)
    s = s.replace(r'\r', '')
    #print(s)
    #print (s)
    tokens_generator = javalang_tok.tokenize(s, keep_comments=keep_comments)
    #print(tokens_generator)
    for token in tokens_generator:
          #print(token)
          if isinstance(token, javalang_tok.String):
              tokens.append(process_string(
              token.value, JAVA_CHAR2TOKEN, JAVA_TOKEN2CHAR, False))
          elif isinstance(token, javalang_tok.Comment):
              com = process_string(
              token.value, JAVA_CHAR2TOKEN, JAVA_TOKEN2CHAR, True)
              if len(com) > 0:
                  tokens.append(com)
              else:
                  tokens.append(token.value)
    print(tokens)
    #return tokens


def main():
	#test_java_tokenizer_discarding_comments()
    
    #s="package com.nostra13.universalimageloader.cache.memory.impl;\r\n\r\nimport java.util.Collection;\r\nimport java.util.Collections;\r\nimport java.util.HashMap;\r\nimport java.util.Map;\r\n\r\nimport com.nostra13.universalimageloader.cache.memory.MemoryCacheAware;\r\n\r\n/**\r\n * Decorator for {@link MemoryCacheAware}. Provides special feature for cache: if some cached object age exceeds defined\r\n * value then this object will be removed from cache.\r\n * \r\n * @author Sergey Tarasevich (nostra13[at]gmail[dot]com)\r\n * @see MemoryCacheAware\r\n */\r\npublic class LimitedAgeMemoryCache\u003cK, V\u003e implements MemoryCacheAware\u003cK, V\u003e {\r\n\r\n\tprivate final MemoryCacheAware\u003cK, V\u003e cache;\r\n\r\n\tprivate final long maxAge;\r\n\tprivate final Map\u003cK, Long\u003e loadingDates = Collections.synchronizedMap(new HashMap\u003cK, Long\u003e());\r\n\r\n\t/**\r\n\t * @param cache\r\n\t *            Wrapped memory cache\r\n\t * @param maxAge\r\n\t *            Max object age \u003cb\u003e(in seconds)\u003c/b\u003e. If object age will exceed this value then it'll be removed from\r\n\t *            cache on next treatment (and therefore be reloaded).\r\n\t */\r\n\tpublic LimitedAgeMemoryCache(MemoryCacheAware\u003cK, V\u003e cache, long maxAge) {\r\n\t\tthis.cache = cache;\r\n\t\tthis.maxAge = maxAge * 1000; // to milliseconds\r\n\t}\r\n\r\n\t@Override\r\n\tpublic boolean put(K key, V value) {\r\n\t\tboolean putSuccesfully = cache.put(key, value);\r\n\t\tif (putSuccesfully) {\r\n\t\t\tloadingDates.put(key, System.currentTimeMillis());\r\n\t\t}\r\n\t\treturn putSuccesfully;\r\n\t}\r\n\r\n\t@Override\r\n\tpublic V get(K key) {\r\n\t\tLong loadingDate = loadingDates.get(key);\r\n\t\tif (loadingDate != null \u0026\u0026 System.currentTimeMillis() - loadingDate \u003e maxAge) {\r\n\t\t\tcache.remove(key);\r\n\t\t\tloadingDates.remove(key);\r\n\t\t}\r\n\r\n\t\treturn cache.get(key);\r\n\t}\r\n\r\n\t@Override\r\n\tpublic void remove(K key) {\r\n\t\tcache.remove(key);\r\n\t\tloadingDates.remove(key);\r\n\t}\r\n\r\n\t@Override\r\n\tpublic Collection\u003cK\u003e keys() {\r\n\t\treturn cache.keys();\r\n\t}\r\n\r\n\t@Override\r\n\tpublic void clear() {\r\n\t\tcache.clear();\r\n\t\tloadingDates.clear();\r\n\t}\r\n}\r\n"
    s="#hello world\nsub readCard()\n{\nwhile(<CARD>)\n{\n$line1=$_;\nnext if($line1=~/^@/);\npush @array, $_;\nforeach my $item(@array)\n{\nmy ($lho,$edms)=split(/\|/,$item);\n$hash{$lho}=$edms;\n}\nforeach $key(keys %hash)\n{\n$value=$hash{$key};\n#print('$key-----------$value');\nprint('inside  print');\nopen(FH,'<','/content/cfsdf')\n}\n}\n}"
    #s="/**\n * Licensed to the Apache Software Foundation (ASF) under one or more\n * contributor license agreements. See the NOTICE file distributed with this\n * work for additional information regarding copyright ownership. The ASF\n * licenses this file to you under the Apache License, Version 2.0 (the\n * \"License\"); you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n * \n * http://www.apache.org/licenses/LICENSE-2.0\n * \n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS, WITHOUT\n * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the\n * License for the specific language governing permissions and limitations under\n * the License.\n */\npackage org.apache.hadoop.io.file.tfile;\n\nimport java.io.IOException;\nimport java.text.DateFormat;\nimport java.text.SimpleDateFormat;\n\n/**\n * this class is a time class to \n * measure to measure the time \n * taken for some event.\n */\npublic  class Timer {\n  long startTimeEpoch;\n  long finishTimeEpoch;\n  private DateFormat formatter = new SimpleDateFormat(\"yyyy-MM-dd HH:mm:ss\");\n  \n  public void startTime() throws IOException {\n      startTimeEpoch = System.currentTimeMillis();\n    }\n\n    public void stopTime() throws IOException {\n      finishTimeEpoch = System.currentTimeMillis();\n    }\n\n    public long getIntervalMillis() throws IOException {\n      return finishTimeEpoch - startTimeEpoch;\n    }\n  \n    public void printlnWithTimestamp(String message) throws IOException {\n      System.out.println(formatCurrentTime() + \"  \" + message);\n  }\n  \n    public String formatTime(long millis) {\n      return formatter.format(millis);\n    }\n    \n    public String getIntervalString() throws IOException {\n      long time = getIntervalMillis();\n      return formatTime(time);\n    }\n    \n    public String formatCurrentTime() {\n      return formatTime(System.currentTimeMillis());\n    }\n\n}\n\n"
    tokenize_java(s,True)
    #hash = str(random.getrandbits(8))
    #print(hash)
    #parsed_code = idx.parse(
        #hash + '_tmp.cpp', args=['-std=c++11'], unsaved_files=[(hash + '_tmp.cpp', s)], options=0)
    #print(parsed_code)
main()
