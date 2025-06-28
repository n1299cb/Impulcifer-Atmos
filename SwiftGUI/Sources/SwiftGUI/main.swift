import SwiftUI

@main
struct ImpulciferApp: App {
    @State private var measurementDir: String = ""
    @State private var testSignal: String = ""
    @StateObject private var processingVM = ProcessingViewModel()

    var body: some Scene {
        WindowGroup {
            TabView {
                SetupView(measurementDir: $measurementDir, testSignal: $testSignal)
                    .tabItem { Text("Setup") }
                ExecutionView(viewModel: processingVM,
                              measurementDir: measurementDir,
                              testSignal: testSignal)
                    .tabItem { Text("Execution") }
                VisualizationView(measurementDir: measurementDir)
                    .tabItem { Text("Visualization") }
            }
            .frame(minWidth: 600, minHeight: 400)
        }
    }
}