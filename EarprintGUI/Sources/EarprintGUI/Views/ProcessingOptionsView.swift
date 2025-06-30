#if canImport(SwiftUI)
import SwiftUI

struct ProcessingOptionsView: View {
    @Binding var channelBalance: String
    @Binding var targetLevel: String

    var body: some View {
        Form {
            TextField("Channel Balance", text: $channelBalance)
            TextField("Target Level", text: $targetLevel)
        }
        .padding()
    }
}
#endif