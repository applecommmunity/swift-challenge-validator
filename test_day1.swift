import Foundation

func runTests() {
    let expectedOutput = "Hello, World!"
    
    if let fileContent = try? String(contentsOfFile: "submission.swift", encoding: .utf8) {
        if fileContent.contains(expectedOutput) {
            print("Test Passed")
        } else {
            print("Test Failed")
        }
    } else {
        print("Test Failed: File not found")
    }
}

runTests()

