#if canImport(SwiftUI)
import SwiftUI

struct EarprintApp: App {
    @State private var measurementDir: String = ""
    @State private var testSignal: String = ""
    @State private var channelBalance: String = ""
    @State private var targetLevel: String = ""
    @State private var selectedLayout: String = "7.1"
    @StateObject private var processingVM = ProcessingViewModel()

    var body: some Scene {
        WindowGroup {
            TabView {
                SetupView(viewModel: processingVM,
                          measurementDir: $measurementDir,
                          testSignal: $testSignal,
                          channelBalance: $channelBalance,
                          targetLevel: $targetLevel,
                          selectedLayout: $selectedLayout)
                    .tabItem { Text("Setup") }
                ExecutionView(viewModel: processingVM,
                              measurementDir: measurementDir,
                              testSignal: testSignal,
                              channelBalance: channelBalance,
                              targetLevel: targetLevel)
                    .tabItem { Text("Execution") }
                VisualizationView(measurementDir: measurementDir)
                    .tabItem { Text("Visualization") }
            }
            .frame(minWidth: 600, minHeight: 400)
        }
    }
}
#endif