import SwiftUI

@main
struct ImpulciferApp: App {
    @State private var measurementDir: String = ""
    @State private var resultOutput: String = ""
    @State private var isRunning: Bool = false

    var body: some Scene {
        WindowGroup {
            ContentView(
                measurementDir: $measurementDir,
                resultOutput: $resultOutput,
                isRunning: $isRunning,
                runAction: runProcessing
            )
            .frame(minWidth: 600, minHeight: 400)
            .padding()
        }
    }

    func runProcessing() {
        isRunning = true
        resultOutput = ""
        let process = Process()
        process.launchPath = "/usr/bin/env"
        process.arguments = ["python3", "../earprint.py", "--dir_path", measurementDir]

        let pipe = Pipe()
        process.standardOutput = pipe
        process.standardError = pipe

        process.launch()
        process.waitUntilExit()

        let data = pipe.fileHandleForReading.readDataToEndOfFile()
        if let output = String(data: data, encoding: .utf8) {
            resultOutput = output
        }
        isRunning = false
    }
}

struct ContentView: View {
    @Binding var measurementDir: String
    @Binding var resultOutput: String
    @Binding var isRunning: Bool
    var runAction: () -> Void

    var body: some View {
        VStack(alignment: .leading) {
            Text("Earprint Swift GUI").font(.title)
            TextField("Measurement directory", text: $measurementDir)
                .textFieldStyle(RoundedBorderTextFieldStyle())
            HStack {
                Button(action: runAction) {
                    Text(isRunning ? "Running..." : "Run")
                }
                .disabled(isRunning || measurementDir.isEmpty)
            }
            ScrollView {
                Text(resultOutput)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
            Spacer()
        }
    }
}