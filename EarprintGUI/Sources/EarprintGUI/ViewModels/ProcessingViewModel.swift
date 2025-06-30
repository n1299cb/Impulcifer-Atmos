import Foundation
#if canImport(SwiftUI)
import SwiftUI

@MainActor
final class ProcessingViewModel: ObservableObject {
    @Published var log: String = ""
    @Published var isRunning: Bool = false
    @Published var progress: Double? = nil

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
        progress = nil
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
                    if str.hasPrefix("PROGRESS") {
                        let comps = str.split(separator: " ")
                        if comps.count >= 2, let val = Double(comps[1]) {
                            self.progress = val
                        }
                    } else {
                        self.log += str
                    }
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
                self.progress = nil
                self.process = nil
            }
        }
    }

    func run(measurementDir: String,
             testSignal: String,
             channelBalance: String?,
             targetLevel: String?,
             playbackDevice: String?,
             recordingDevice: String?,
             outputChannels: [Int]?,
             inputChannels: [Int]?,
             enableCompensation: Bool,
             headphoneEqEnabled: Bool,
             headphoneFile: String?,
             compensationType: String?,
             diffuseField: Bool,
             xCurveAction: String,
             xCurveType: String?,
             xCurveInCapture: Bool) {
        var args = ["--dir_path", measurementDir, "--test_signal", testSignal]
        if let balance = channelBalance, !balance.isEmpty {
            args += ["--channel_balance", balance]
        }
        if let target = targetLevel, !target.isEmpty {
            args += ["--target_level", target]
        }
        if let p = playbackDevice { args += ["--playback_device", p] }
        if let r = recordingDevice { args += ["--recording_device", r] }
        if let outs = outputChannels, !outs.isEmpty {
            args += ["--output_channels", outs.map(String.init).joined(separator: ",")]
        }
        if let ins = inputChannels, !ins.isEmpty {
            args += ["--input_channels", ins.map(String.init).joined(separator: ",")]
        }
        if enableCompensation {
            args.append("--compensation")
            if headphoneEqEnabled {
                if let file = headphoneFile, !file.isEmpty { args += ["--headphones", file] }
            } else {
                args.append("--no_headphone_compensation")
            }
            if let cType = compensationType, !cType.isEmpty { args.append(cType) }
        }
        if diffuseField { args.append("--diffuse_field_compensation") }
        if xCurveAction == "Apply X-Curve" { args.append("--apply_x_curve") }
        if xCurveAction == "Remove X-Curve" { args.append("--remove_x_curve") }
        if xCurveAction != "None", let ct = xCurveType, !ct.isEmpty {
            args += ["--x_curve_type", ct]
        }
        if xCurveInCapture { args.append("--x_curve_in_capture") }
        startPython(script: scriptPath("earprint.py"), args: args)
    }

    func layoutWizard(layout: String, dir: String) {
        startPython(script: scriptPath("generate_layout.py"), args: ["--layout", layout, "--dir", dir])
    }

    func captureWizard(layout: String, dir: String) {
        startPython(script: scriptPath("capture_wizard.py"), args: ["--layout", layout, "--dir", dir, "--print_progress"])
    }

    func record(measurementDir: String, testSignal: String, playbackDevice: String, recordingDevice: String, outputFile: String?) {
        var args = [
            "--output_dir", measurementDir,
            "--test_signal", testSignal,
            "--playback_device", playbackDevice,
            "--recording_device", recordingDevice,
            "--print_progress"
        ]
        if let file = outputFile { args += ["--output_file", file] }
        startPython(script: scriptPath("recorder.py"), args: args)
    }

    func recordHeadphoneEQ(measurementDir: String, testSignal: String, playbackDevice: String, recordingDevice: String) {
        let file = URL(fileURLWithPath: measurementDir).appendingPathComponent("headphones.wav").path
        record(measurementDir: measurementDir,
               testSignal: testSignal,
               playbackDevice: playbackDevice,
               recordingDevice: recordingDevice,
               outputFile: file)
    }

    func recordRoomResponse(measurementDir: String, testSignal: String, playbackDevice: String, recordingDevice: String) {
        let file = URL(fileURLWithPath: measurementDir).appendingPathComponent("room.wav").path
        record(measurementDir: measurementDir,
               testSignal: testSignal,
               playbackDevice: playbackDevice,
               recordingDevice: recordingDevice,
               outputFile: file)
    }

    func exportHesuviPreset(measurementDir: String, destination: String) {
        let src = URL(fileURLWithPath: measurementDir).appendingPathComponent("hesuvi.wav")
        let dest = URL(fileURLWithPath: destination)
        do {
            try FileManager.default.copyItem(at: src, to: dest)
            log += "Exported to \(destination)\n"
        } catch {
            log += "Export failed: \(error)\n"
        }
    }

    func clearLog() {
        log = ""
    }

    func cancel() {
        process?.terminate()
        process = nil
        isRunning = false
        progress = nil
    }
}
#else
final class ProcessingViewModel {
    var log: String = ""
    var isRunning: Bool = false
    var progress: Double? = nil
    func run(measurementDir: String, testSignal: String, channelBalance: String?, targetLevel: String?, playbackDevice: String?, recordingDevice: String?, outputChannels: [Int]?, inputChannels: [Int]?) {}
    func layoutWizard(layout: String, dir: String) {}
    func captureWizard(layout: String, dir: String) {}
    func record(measurementDir: String, testSignal: String, playbackDevice: String, recordingDevice: String, outputFile: String?) {}
    func recordHeadphoneEQ(measurementDir: String, testSignal: String, playbackDevice: String, recordingDevice: String) {}
    func recordRoomResponse(measurementDir: String, testSignal: String, playbackDevice: String, recordingDevice: String) {}
    func exportHesuviPreset(measurementDir: String, destination: String) {}
    func clearLog() {}
    func cancel() {}
}
#endif