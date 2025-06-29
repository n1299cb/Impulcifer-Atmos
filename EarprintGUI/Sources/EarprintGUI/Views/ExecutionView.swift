#if canImport(SwiftUI)
import SwiftUI

struct ExecutionView: View {
    @ObservedObject var viewModel: ProcessingViewModel
    var measurementDir: String
    var testSignal: String
    var channelBalance: String
    var targetLevel: String

    var body: some View {
        VStack(alignment: .leading) {
            HStack {
                Button(action: {
                    viewModel.run(measurementDir: measurementDir,
                                   testSignal: testSignal,
                                   channelBalance: channelBalance,
                                   targetLevel: targetLevel)
                }) {
                    Text(viewModel.isRunning ? "Running..." : "Run Processing")
                }
                .disabled(viewModel.isRunning || measurementDir.isEmpty || testSignal.isEmpty)

                Button("Cancel") { viewModel.cancel() }
                    .disabled(!viewModel.isRunning)
            
                Button("Clear Log") { viewModel.clearLog() }
                    .disabled(viewModel.log.isEmpty)
            }

            ScrollView {
                Text(viewModel.log)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
        }
        .padding()
    }
}
#endif