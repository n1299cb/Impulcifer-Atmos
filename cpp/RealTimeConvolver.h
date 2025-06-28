#ifndef REALTIME_CONVOLVER_H
#define REALTIME_CONVOLVER_H

#include <vector>
#include <fftw3.h>

class RealTimeConvolver {
public:
    RealTimeConvolver(const std::vector<std::vector<float>>& leftIRs,
                      const std::vector<std::vector<float>>& rightIRs,
                      size_t maxBlockSize);
    ~RealTimeConvolver();

    void processBlock(const std::vector<std::vector<float>>& input,
                      std::vector<float>& outLeft,
                      std::vector<float>& outRight);

private:
    size_t nextPow2(size_t x) const;
    void prepareIRFFT(size_t fftSize);

    size_t maxBlockSize_;
    size_t maxIrLen_;
    size_t fftSize_;
    size_t nSpeakers_;

    std::vector<std::vector<float>> irLeft_;
    std::vector<std::vector<float>> irRight_;
    std::vector<std::vector<fftwf_complex>> irFFTLeft_;
    std::vector<std::vector<fftwf_complex>> irFFTRight_;

    std::vector<float> overlapL_;
    std::vector<float> overlapR_;
};

#endif // REALTIME_CONVOLVER_H