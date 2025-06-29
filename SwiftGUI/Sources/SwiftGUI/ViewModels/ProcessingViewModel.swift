import Foundation
#if canImport(SwiftUI)
import SwiftUI

final class ProcessingViewModel: ObservableObject {
    @Published var log: String = ""
    @Published var isRunning: Bool = false

    private var process: Process?

    private func scriptPath(_ name: String) -> String {
        let fm = FileManager.default
        let cwd = URL(fileURLWithPath: fm.currentDirectoryPath)
        let direct = cwd.appendingPathComponent(name).path
        if fm.fileExists(atPath: direct) { return direct }
        let parent = cwd.deletingLastPathComponent().appendingPathComponent(name).path
        if fm.fileExists(atPath: parent) { return parent }
        return name
    }

    private func startPython(script: String, args: [String]) {
        isRunning = true
        log = ""
        DispatchQueue.global(qos: .userInitiated).async { [weak self] in
            let process = Process()
            process.executableURL = URL(fileURLWithPath: "/usr/bin/env")
            process.arguments = ["python3", script] + args
            let pipe = Pipe()
            process.standardOutput = pipe
            process.standardError = pipe
            pipe.fileHandleForReading.readabilityHandler = { handle in
                let data = handle.availableData
                guard !data.isEmpty, let str = String(data: data, encoding: .utf8) else { return }
                DispatchQueue.main.async {
                    self?.log += str
                }
            }
            do {
                self?.process = process
                try process.run()
                process.waitUntilExit()
            } catch {
                DispatchQueue.main.async {
                    self?.log += "\(error)\n"
                }
            }
            DispatchQueue.main.async {
                pipe.fileHandleForReading.readabilityHandler = nil
                self?.isRunning = false
                self?.process = nil
            }
        }
    }

    func run(measurementDir: String, testSignal: String, channelBalance: String?, targetLevel: String?) {
        var args = ["--dir_path", measurementDir, "--test_signal", testSignal]
        if let balance = channelBalance, !balance.isEmpty {
            args += ["--channel_balance", balance]
        }
        if let target = targetLevel, !target.isEmpty {
            args += ["--target_level", target]
        }
        startPython(script: scriptPath("earprint.py"), args: args)
    }

    func layoutWizard(layout: String, dir: String) {
        startPython(script: scriptPath("generate_layout.py"), args: ["--layout", layout, "--dir", dir])
    }

    func captureWizard(layout: String, dir: String) {
        startPython(script: scriptPath("capture_wizard.py"), args: ["--layout", layout, "--dir", dir])
    }

    func cancel() {
        process?.terminate()
        process = nil
        isRunning = false
    }
}
#else
final class ProcessingViewModel {
    var log: String = ""
    var isRunning: Bool = false
    func run(measurementDir: String, testSignal: String, channelBalance: String?, targetLevel: String?) {}
    func layoutWizard(layout: String, dir: String) {}
    func captureWizard(layout: String, dir: String) {}
    func cancel() {}
}
#endif