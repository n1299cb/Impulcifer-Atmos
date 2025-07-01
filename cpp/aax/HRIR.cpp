#include "HRIR.h"
#include <sndfile.h>

bool HRIR::loadFromWav(const std::string& path) {
    SF_INFO info{};
    SNDFILE* sf = sf_open(path.c_str(), SFM_READ, &info);
    if (!sf) {
        return false;
    }
    std::vector<float> buffer(info.frames * info.channels);
    sf_readf_float(sf, buffer.data(), info.frames);
    sf_close(sf);

    if (info.channels % 2 != 0) {
        return false; // Expect interleaved L/R pairs
    }
    size_t pairs = info.channels / 2;
    leftIRs_.assign(pairs, std::vector<float>(info.frames));
    rightIRs_.assign(pairs, std::vector<float>(info.frames));
    for (size_t p = 0; p < pairs; ++p) {
        for (sf_count_t n = 0; n < info.frames; ++n) {
            leftIRs_[p][n] = buffer[n * info.channels + 2 * p];
            rightIRs_[p][n] = buffer[n * info.channels + 2 * p + 1];
        }
    }
    return true;
}