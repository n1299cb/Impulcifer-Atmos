import Foundation
import SwiftUI

final class ProcessingViewModel: ObservableObject {
    @Published var log: String = ""
    @Published var isRunning: Bool = false

    func run(measurementDir: String, testSignal: String) {
        isRunning = true
        log = ""
        DispatchQueue.global(qos: .userInitiated).async {
            let process = Process()
            process.launchPath = "/usr/bin/env"
            process.arguments = [
                "python3",
                "../earprint.py",
                "--dir_path", measurementDir,
                "--input", testSignal
            ]
            let pipe = Pipe()
            process.standardOutput = pipe
            process.standardError = pipe
            process.launch()
            process.waitUntilExit()
            let data = pipe.fileHandleForReading.readDataToEndOfFile()
            let output = String(data: data, encoding: .utf8) ?? ""
            DispatchQueue.main.async {
                self.log = output
                self.isRunning = false
            }
        }
    }
}