#if canImport(SwiftUI)
import SwiftUI
import AppKit

struct SetupView: View {
    @ObservedObject var viewModel: ProcessingViewModel
    @Binding var measurementDir: String
    @Binding var testSignal: String
    @Binding var channelBalance: String
    @Binding var targetLevel: String
    @Binding var selectedLayout: String
    @Binding var playbackDevice: String
    @Binding var recordingDevice: String
    @Binding var channelMapping: [String: [Int]]

    struct AudioDevice: Identifiable {
        let id: Int
        let name: String
        let maxOutput: Int
        let maxInput: Int
    }

    @State private var playbackDevices: [AudioDevice] = []
    @State private var recordingDevices: [AudioDevice] = []
    @State private var showMapping = false
    @State private var measurementDirValid: Bool = true
    @State private var testSignalValid: Bool = true
    @State private var inputLevel: Double = 0
    @State private var outputLevel: Double = 0
    @State private var isMonitoring: Bool = false
    @State private var inputProcess: Process? = nil
    @State private var outputProcess: Process? = nil
    @State private var inputPipe: Pipe? = nil
    @State private var outputPipe: Pipe? = nil

    @State private var layouts: [String] = []

    var body: some View {
        VStack(alignment: .leading) {
            Form {
                HStack {
                    TextField("Measurement directory", text: $measurementDir)
                        .overlay(RoundedRectangle(cornerRadius: 4)
                            .stroke(measurementDirValid ? Color.green : Color.red))
                        .onChange(of: measurementDir) { _ in validatePaths() }
                Button("Browse") {
                    if let path = openPanel(directory: true, startPath: measurementDir) {
                        measurementDir = path
                    }
                }
            }
            HStack {
                TextField("Test signal", text: $testSignal)
                    .overlay(RoundedRectangle(cornerRadius: 4)
                        .stroke(testSignalValid ? Color.green : Color.red))
                    .onChange(of: testSignal) { _ in validatePaths() }
                Button("Browse") {
                    if let path = openPanel(directory: false, startPath: testSignal) {
                        testSignal = path
                    }
                }
            }
            Picker("Playback Device", selection: $playbackDevice) {
                ForEach(playbackDevices) { dev in
                    Text("\(dev.id): \(dev.name)").tag(String(dev.id))
                }
            }
            Picker("Recording Device", selection: $recordingDevice) {
                ForEach(recordingDevices) { dev in
                    Text("\(dev.id): \(dev.name)").tag(String(dev.id))
                }
            }
            Picker("Layout", selection: $selectedLayout) {
                ForEach(layouts, id: \.self) { Text($0) }
            }
            HStack {
                Spacer()
                Button("Refresh Devices") { loadDevices() }
            }
            TextField("Channel Balance", text: $channelBalance)
            TextField("Target Level", text: $targetLevel)
            HStack {
                Button("Layout Wizard") {
                    viewModel.layoutWizard(layout: selectedLayout, dir: measurementDir)
                }
                Button("Capture Wizard") {
                    viewModel.captureWizard(layout: selectedLayout, dir: measurementDir)
                }
                Button("Map Channels") { showMapping = true }
                Button("Auto Map") { autoMapChannels() }
            }
            HStack {
                Text("Input Level")
                ProgressView(value: inputLevel)
                    .progressViewStyle(.linear)
                    .frame(maxWidth: .infinity)
                Button(isMonitoring ? "Stop Monitor" : "Start Monitor") {
                    isMonitoring ? stopMonitor() : startMonitor()
                }
            }
            HStack {
                Text("Output Level")
                ProgressView(value: outputLevel)
                    .progressViewStyle(.linear)
                    .frame(maxWidth: .infinity)
            }
            if viewModel.isRunning {
                if let progress = viewModel.progress {
                    ProgressView(value: progress)
                } else {
                    ProgressView()
                        .progressViewStyle(.linear)
                }
            }
            if !viewModel.log.isEmpty {
                ScrollView {
                    Text(viewModel.log)
                        .frame(maxWidth: .infinity, alignment: .leading)
                }
            }
        }
        .padding()
        .onAppear(perform: loadLayouts)
        .onAppear(perform: loadDevices)
        .onAppear(perform: validatePaths)
        .sheet(isPresented: $showMapping) {
            mappingSheet
        }
    }
    }


    func validatePaths() {
        var isDir: ObjCBool = false
        measurementDirValid = FileManager.default.fileExists(atPath: measurementDir, isDirectory: &isDir) && isDir.boolValue
        testSignalValid = FileManager.default.fileExists(atPath: testSignal)
    }

    func openPanel(directory: Bool, startPath: String) -> String? {
        let panel = NSOpenPanel()
        panel.canChooseFiles = !directory
        panel.canChooseDirectories = directory
        panel.allowsMultipleSelection = false
        if !startPath.isEmpty {
            let base = directory ? startPath : (startPath as NSString).deletingLastPathComponent
            var isDir: ObjCBool = false
            if FileManager.default.fileExists(atPath: base, isDirectory: &isDir), isDir.boolValue {
                panel.directoryURL = URL(fileURLWithPath: base)
            } else {
                panel.directoryURL = FileManager.default.homeDirectoryForCurrentUser
            }
        }
        return panel.runModal() == .OK ? panel.url?.path : nil
    }

    func scriptPath(_ name: String) -> String {
        let fm = FileManager.default
        let cwd = URL(fileURLWithPath: fm.currentDirectoryPath)
        let direct = cwd.appendingPathComponent(name).path
        if fm.fileExists(atPath: direct) { return direct }
        let parent = cwd.deletingLastPathComponent().appendingPathComponent(name).path
        if fm.fileExists(atPath: parent) { return parent }
        return name
    }

    func startMonitor() {
        stopMonitor()
        isMonitoring = true

        if !recordingDevice.isEmpty {
            let proc = Process()
            proc.executableURL = URL(fileURLWithPath: "/usr/bin/env")
            proc.arguments = ["python3", scriptPath("level_meter.py"), "--device", recordingDevice]
            let pipe = Pipe()
            proc.standardOutput = pipe
            proc.standardError = pipe
            pipe.fileHandleForReading.readabilityHandler = { handle in
                let data = handle.availableData
                guard !data.isEmpty, let str = String(data: data, encoding: .utf8) else { return }
                let vals = str.split(separator: "\n")
                if let last = vals.last, let db = Double(last) {
                    let value = max(0, min(1, (db + 60) / 60))
                    DispatchQueue.main.async { self.inputLevel = value }
                }
            }
            inputProcess = proc
            inputPipe = pipe
            try? proc.run()
        }

        if !playbackDevice.isEmpty {
            let proc = Process()
            proc.executableURL = URL(fileURLWithPath: "/usr/bin/env")
            proc.arguments = ["python3", scriptPath("level_meter.py"), "--device", playbackDevice, "--loopback"]
            let pipe = Pipe()
            proc.standardOutput = pipe
            proc.standardError = pipe
            pipe.fileHandleForReading.readabilityHandler = { handle in
                let data = handle.availableData
                guard !data.isEmpty, let str = String(data: data, encoding: .utf8) else { return }
                let vals = str.split(separator: "\n")
                if let last = vals.last, let db = Double(last) {
                    let value = max(0, min(1, (db + 60) / 60))
                    DispatchQueue.main.async { self.outputLevel = value }
                }
            }
            outputProcess = proc
            outputPipe = pipe
            try? proc.run()
        }
    }

    func stopMonitor() {
        isMonitoring = false
        inputProcess?.terminate()
        outputProcess?.terminate()
        inputProcess = nil
        outputProcess = nil
        inputPipe?.fileHandleForReading.readabilityHandler = nil
        outputPipe?.fileHandleForReading.readabilityHandler = nil
        inputPipe = nil
        outputPipe = nil
        inputLevel = 0
        outputLevel = 0
    }

    func loadDevices() {
        DispatchQueue.global(qos: .userInitiated).async {
            let process = Process()
            process.executableURL = URL(fileURLWithPath: "/usr/bin/env")
            process.arguments = [
                "python3",
                "-c",
                "import json, sounddevice as sd, sys; json.dump({'devices': sd.query_devices(), 'default': list(sd.default.device)}, sys.stdout)"
            ]
            let pipe = Pipe()
            process.standardOutput = pipe
            try? process.run()
            process.waitUntilExit()
            let data = pipe.fileHandleForReading.readDataToEndOfFile()
            guard
                let obj = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                let devs = obj["devices"] as? [[String: Any]]
            else {
                DispatchQueue.main.async {
                    self.viewModel.log += String(data: data, encoding: .utf8) ?? "Failed to load audio devices\n"
                }
                return
            }
            let defaults = (obj["default"] as? [Int]) ?? [-1, -1]
            let all = devs.enumerated().map { idx, d in
                AudioDevice(
                    id: idx,
                    name: (d["name"] as? String) ?? "Unknown",
                    maxOutput: d["max_output_channels"] as? Int ?? 0,
                    maxInput: d["max_input_channels"] as? Int ?? 0
                )
            }
            DispatchQueue.main.async {
                self.playbackDevices = all.filter { $0.maxOutput > 0 }
                self.recordingDevices = all.filter { $0.maxInput > 0 }
                if self.playbackDevice.isEmpty, defaults[1] >= 0,
                   let dev = self.playbackDevices.first(where: { $0.id == defaults[1] }) {
                    self.playbackDevice = String(dev.id)
                }
                if self.recordingDevice.isEmpty, defaults[0] >= 0,
                   let dev = self.recordingDevices.first(where: { $0.id == defaults[0] }) {
                    self.recordingDevice = String(dev.id)
                }
            }
        }
    }

    func loadLayouts() {
        DispatchQueue.global(qos: .userInitiated).async {
            let process = Process()
            process.executableURL = URL(fileURLWithPath: "/usr/bin/env")
            process.arguments = [
                "python3",
                "-c",
                "import json,constants,sys; json.dump(sorted(constants.SPEAKER_LAYOUTS.keys()), sys.stdout)"
            ]
            let pipe = Pipe()
            process.standardOutput = pipe
            try? process.run()
            process.waitUntilExit()
            let data = pipe.fileHandleForReading.readDataToEndOfFile()
            if let arr = try? JSONSerialization.jsonObject(with: data) as? [String] {
                DispatchQueue.main.async {
                    self.layouts = arr
                    if self.selectedLayout.isEmpty, let first = arr.first {
                        self.selectedLayout = first
                    }
                }
            } else {
                DispatchQueue.main.async {
                    self.viewModel.log += String(data: data, encoding: .utf8) ?? "Failed to load layouts\n"
                }
            }
        }
    }


    func autoMapChannels() {
        guard
            let pDev = playbackDevices.first(where: { String($0.id) == playbackDevice }),
            let rDev = recordingDevices.first(where: { String($0.id) == recordingDevice })
        else { return }
        let spkCount = fetchSpeakerLabels(layout: selectedLayout).count
        channelMapping["output_channels"] = Array(0..<min(pDev.maxOutput, spkCount))
        channelMapping["input_channels"] = Array(0..<min(rDev.maxInput, 2))
    }

    var mappingSheet: some View {
        let pChannels = playbackDevices.first(where: { String($0.id) == playbackDevice })?.maxOutput ?? 2
        let rChannels = recordingDevices.first(where: { String($0.id) == recordingDevice })?.maxInput ?? 2
        let labels = fetchSpeakerLabels(layout: selectedLayout)
        return ChannelMappingView(
            playbackChannels: pChannels,
            recordingChannels: rChannels,
            speakerLabels: labels,
            channelMapping: $channelMapping,
            onSave: { showMapping = false }
        )
        .frame(minWidth: 300, minHeight: 200)
    }

    func fetchSpeakerLabels(layout: String) -> [String] {
        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/env")
        process.arguments = [
            "python3",
            "-c",
            "import json,constants,sys; print(json.dumps([c for g in constants.SPEAKER_LAYOUTS.get('" + layout + "', []) for c in g]))"
        ]
        let pipe = Pipe()
        process.standardOutput = pipe
        try? process.run()
        process.waitUntilExit()
        let data = pipe.fileHandleForReading.readDataToEndOfFile()
        if let arr = try? JSONSerialization.jsonObject(with: data) as? [String] {
            return arr
        }
        return []
    }
}
#endif