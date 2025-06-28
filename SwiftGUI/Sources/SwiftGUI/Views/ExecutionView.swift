import SwiftUI

struct ExecutionView: View {
    @ObservedObject var viewModel: ProcessingViewModel
    var measurementDir: String
    var testSignal: String

    var body: some View {
        VStack(alignment: .leading) {
            Button(action: {
                viewModel.run(measurementDir: measurementDir, testSignal: testSignal)
            }) {
                Text(viewModel.isRunning ? "Running..." : "Run Processing")
            }
            .disabled(viewModel.isRunning || measurementDir.isEmpty || testSignal.isEmpty)

            ScrollView {
                Text(viewModel.log)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
        }
        .padding()
    }
}