import os
import ntpath
import sys
from lxml import etree


class Swifty:
    @staticmethod
    def getAllStoryboardInRoot(root):
        return [(os.path.splitext(fn)[0], r + "/" + fn)
                for r, ds, fs in os.walk(root) if "Carthage" not in r
                for fn in fs if fn.endswith("storyboard")]

    @staticmethod
    def getStoryboardViewControllers(storyboardPath):
        parser = etree.XMLParser(recover=True)
        root = etree.parse(storyboardPath, parser=parser)
        return root.xpath("//viewController/@storyboardIdentifier | //tabBarController/@storyboardIdentifier | //navigationController/@storyboardIdentifier")

    @staticmethod
    def formatAsSwiftEnum(enumName, values):
        """:param enumName: the name of the enum that will be generated
        :param values: the types inside the enum, the actual meat
        :return a string which is a swift enum"""
        if len(values) == 0:
            values = ["none"]
        return '''\
    enum {}: String {{
    {}}}
        '''.format(enumName, "".join("      case {}\n".format(enumValue) for enumValue in values))

    @staticmethod
    def generatePostfix(storyboardName):
        return '''\
\npostfix func ^ (key: R.storyboard.{0}) -> UIViewController {{
    return UIStoryboard(name: "\(R.storyboard.{0}.self)", bundle: nil).instantiateViewController(withIdentifier: key.rawValue)
}}'''.format(storyboardName)

    @staticmethod
    def createFile(rootPath):
        storyboards = Swifty.getAllStoryboardInRoot(rootPath)

        resFile = '''\
import UIKit

extension R {{
    struct storyboard {{
        {}

    }}
}}

{}'''.format("".join(
            "       {}".format(
                Swifty.formatAsSwiftEnum(enumName=story[0], values=Swifty.getStoryboardViewControllers(story[1]))) for
            story in
            storyboards), "".join(Swifty.generatePostfix(storyboard[0]) for storyboard in storyboards))

        return resFile


# Get the input argument for the project root path {$PATHDIR}
inputArguments = len(sys.argv)
if inputArguments > 1:
    rootPath = sys.argv[1]

    if inputArguments > 2:
        outputDirPath = sys.argv[2]
    else:
        print("Using input dir as output.")
        outputDirPath = rootPath
else:
    print("Please supply the root directory of the project and output file location")
    print("USAGE: python ios-storyboards.py [inputDir] [outputDir]")
    sys.exit()

ntpath.basename(rootPath)

resultSwiftPage = Swifty.createFile(rootPath)
with open("{}/R+storyboards.swift".format(outputDirPath), "w+") as f:
    f.write(resultSwiftPage)

print("Created R storyboard support")
