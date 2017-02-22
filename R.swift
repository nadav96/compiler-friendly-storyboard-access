import Foundation

struct R {
    // Blank
}

postfix operator ^

postfix func ^ (key: R.string) -> String {
    return NSLocalizedString(key.rawValue, comment: "")
}

postfix func ^ (key: R.array) -> [String] {
    return R.arrays[key.rawValue]! as! [String]
}

