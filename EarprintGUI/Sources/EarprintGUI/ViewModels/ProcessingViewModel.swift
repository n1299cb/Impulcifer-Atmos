import Foundation
#if canImport(SwiftUI)
import SwiftUI

@MainActor
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
            guard let self else { return }
            let process = Process()
            process.executableURL = URL(fileURLWithPath: "/usr/bin/env")
            process.arguments = ["python3", script] + args
            let pipe = Pipe()
            process.standardOutput = pipe
            process.standardError = pipe
            pipe.fileHandleForReading.readabilityHandler = { [weak self] handle in
                guard let self else { return }
                let data = handle.availableData
                guard !data.isEmpty, let str = String(data: data, encoding: .utf8) else { return }
                Task { @MainActor in
                    self.log += str
                }
            }
            do {
                Task { @MainActor in self.process = process }
                try process.run()
                process.waitUntilExit()
            } catch {
                Task { @MainActor in
                    self.log += "\(error)\n"
                }
            }
            Task { @MainActor in
                pipe.fileHandleForReading.readabilityHandler = nil
                self.isRunning = false
                self.process = nil
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

    func clearLog() {
        log = ""
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
    func clearLog() {}
    func cancel() {}
}
#endif