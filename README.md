# compiler-friendly-storyboard-access
A simple build time script that scans all of the storyboards in your project, and builds a struct of each, each containing an enum of all available view controllers.

## Setup
1. Add the python script to your project root
2. Use the [ios-res-tool](https://github.com/SteveKChiu/ios-res-tool) script to generate the R.swift file (or grab the blank provided in this repo, though I highly recommend the former :wink:)
3. Add a run script in the project settings > Build Phases > plus button
4. In the script text, paste the following:
```
python "${SRCROOT}/ios-storyboards.py" "${SRCROOT}/"
```
5. The script generate a file named **R+storyboards.swift** in the root folder of the project, open Finder, and drag the file to the project navigator.

And you should be set to go! The R+storyboards file is recreated on every build, so if you remove/add/change id of storyboard, the compiler will let you know, rather then finding out on runtime :smile:

## Usage
1. in the storboard file, select the view controller you want to access
2. go to identity inspector, and add a unique name to the storyboard in the storyboard ID, under identity.
Remember that the way the script works is by allowing access to a every storyboard file, and on every file, allow access to every controller, which identified by the **Storyboard ID**
3. Now you can access it! Let's say the storyboard file is: Main.storyboard, and the controller we want has the id: helloworld1, you can generate the UIViewController with this simple line:
```
let vc: UIViewController = R.storyboard.Main.helloworld1^  // where the '^' character initialaze the controller
```

