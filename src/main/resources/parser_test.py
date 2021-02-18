#!/usr/bin/env python3

import sys,os
import ast
import json
import asttokens
import astroid
import argparse


jsonData = list()

parser = argparse.ArgumentParser(description='RefDiff parser for Python programming language')
parser.add_argument('-f', '--file', help='input file with path', type=str, required=True)
parser.add_argument('-p', '--pretty', help='output json in pretty format', action='store_true')
args = parser.parse_args()
print(args)

def get_tokenz(node): #pass a node and it will return the tokens
    tokens = []
    if isinstance(node, ast.Module):
        isStart = True
        line = 0
        a = atok.get_tokens(node,include_extra=True)
        for i in a:
            if isStart:
                line = i.start[0]
                isStart = False
            tokens.append("{}-{}".format(i.startpos,i.endpos))
        jsonData.append({
            "type" : "File",
            "start" : tokens[0].split('-')[0],
            "end": tokens[-1].split('-')[1],
            "line": line,
            "name": file_name[1],
            "parent": "null",
            "tokens": [t for t in tokens]
        })
    else:
        a = atok.get_tokens(node,include_extra=True)
        isStart = True
        startToken = endToken = line = 0
        tokens.append(node.name)
        for i in a:
            if isStart:
                startToken = i.startpos
                line = i.start[0]
                isStart = False
            endToken = i.endpos
        tokens.append(startToken)
        tokens.append(endToken)
        tokens.append(line)
        for i in jsonData:
            if i["name"] == node.name:
                i["start"] = tokens[1]
                i["end"] = tokens[2]



def getFunctionParent(node):
    stack = list()
    stack.append(node)
    functionNodes = dict()
    test_counter = 0
    callsList = list()
    while(stack):
        currentNode = stack.pop()
        for child in currentNode.get_children():
            test_counter+=1
            stack.append(child)
            has_body = "True"
            try:
                if(child.body):
                    pass
                """
                Remove comments if you consider a function with just pass had no body
                if isinstance(child.body[0], astroid.node_classes.Pass): 
                    has_body="False"
                """

            except:
                has_body = "False"
            if isinstance(child,astroid.FunctionDef):
                callsList = [child.name]
                functionNodes[child.name] = child.parent.name
                jsonData.append({
                    "type": "Function",
                    "parent": child.parent.name,
                    "name": child.name,
                    "parameters": [a.name for a in child.args.args],
                    "line": child.lineno,
                    "has_body" : has_body,
                    "calls": "none"
                })
            if isinstance(child, astroid.ClassDef):
                callsList = list()
                jsonData.append({
                    "type": "Class",
                    "parent": child.parent.name,
                    "name": child.name,
                    "parameters": 'None',
                    "line": child.lineno,
                    "has_body": has_body
                })


            if isinstance(child, astroid.Call):
                callsList.append(child.func.name)
                if len(callsList)>1:
                    for i in jsonData:
                        if i['name'] == callsList[0]:
                            i['calls'] = callsList[1:]

    return functionNodes

file_name = os.path.split(args.file)#file_name[0] = path to file name, file_name[1] = file name
path = os.path.split(file_name[0]) ##path[1] = namespace

with open(args.file, "r") as file:
    code = file.read()

parsedCode = astroid.parse(code, file_name[1])
getFunctionParent(parsedCode)


atok = asttokens.ASTTokens(code, parse=True)

[get_tokenz(n) for n in ast.walk(atok.tree) if isinstance(n, ast.Module)]#gets tokens for module
[get_tokenz(n) for n in ast.walk(atok.tree) if isinstance(n, ast.FunctionDef)]#gets tokens for functions
[get_tokenz(n) for n in ast.walk(atok.tree) if isinstance(n, ast.ClassDef)]#gets tokens for functions

ident = 2 if args.pretty else None
print(json.dumps(jsonData, indent=ident))