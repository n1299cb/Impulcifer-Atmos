#ifndef HRIR_H
#define HRIR_H

#include <string>
#include <vector>

/** Simple HRIR loader used by the AAX plugin.
 *  Assumes HRIR WAV files store interleaved left/right pairs
 *  for each speaker. The number of channels must therefore
 *  be even.
 */
class HRIR {
public:
    // Loads the HRIR WAV from disk. Returns false on failure.
    bool loadFromWav(const std::string& path);

    const std::vector<std::vector<float>>& leftIRs() const { return leftIRs_; }
    const std::vector<std::vector<float>>& rightIRs() const { return rightIRs_; }

private:
    std::vector<std::vector<float>> leftIRs_;
    std::vector<std::vector<float>> rightIRs_;
};

#endif // HRIR_H