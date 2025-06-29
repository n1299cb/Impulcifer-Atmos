#if canImport(SwiftUI)
import SwiftUI
EarprintApp.main()
#else
import Foundation
print("SwiftGUI requires macOS with SwiftUI.\n")
#endif