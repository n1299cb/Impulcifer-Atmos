#include "RealTimeConvolver.h"
#include <algorithm>
#include <cstring>

RealTimeConvolver::RealTimeConvolver(
    const std::vector<std::vector<float>>& leftIRs,
    const std::vector<std::vector<float>>& rightIRs,
    size_t maxBlockSize)
    : maxBlockSize_(maxBlockSize),
      fftSize_(0)
{
    nSpeakers_ = leftIRs.size();
    irLeft_ = leftIRs;
    irRight_ = rightIRs;
    maxIrLen_ = 0;
    for (size_t i = 0; i < nSpeakers_; ++i) {
        maxIrLen_ = std::max(maxIrLen_, (size_t)leftIRs[i].size());
        maxIrLen_ = std::max(maxIrLen_, (size_t)rightIRs[i].size());
    }
    fftSize_ = nextPow2(maxBlockSize_ + maxIrLen_ - 1);
    prepareIRFFT(fftSize_);
    overlapL_.assign(fftSize_ - maxBlockSize_, 0.f);
    overlapR_.assign(fftSize_ - maxBlockSize_, 0.f);
}

RealTimeConvolver::~RealTimeConvolver() {}

size_t RealTimeConvolver::nextPow2(size_t x) const {
    size_t p = 1;
    while (p < x) p <<= 1;
    return p;
}

void RealTimeConvolver::prepareIRFFT(size_t fftSize) {
    size_t fftLen = fftSize / 2 + 1;
    irFFTLeft_.assign(nSpeakers_, std::vector<fftwf_complex>(fftLen));
    irFFTRight_.assign(nSpeakers_, std::vector<fftwf_complex>(fftLen));
    std::vector<float> tmp(fftSize);
    for (size_t i = 0; i < nSpeakers_; ++i) {
        std::fill(tmp.begin(), tmp.end(), 0.f);
        std::copy(irLeft_[i].begin(), irLeft_[i].end(), tmp.begin());
        fftwf_plan p = fftwf_plan_dft_r2c_1d(fftSize, tmp.data(), irFFTLeft_[i].data(), FFTW_ESTIMATE);
        fftwf_execute(p);
        fftwf_destroy_plan(p);

        std::fill(tmp.begin(), tmp.end(), 0.f);
        std::copy(irRight_[i].begin(), irRight_[i].end(), tmp.begin());
        p = fftwf_plan_dft_r2c_1d(fftSize, tmp.data(), irFFTRight_[i].data(), FFTW_ESTIMATE);
        fftwf_execute(p);
        fftwf_destroy_plan(p);
    }
}

void RealTimeConvolver::processBlock(const std::vector<std::vector<float>>& input,
                                     std::vector<float>& outLeft,
                                     std::vector<float>& outRight)
{
    size_t nSamples = input[0].size();
    size_t neededFft = nextPow2(nSamples + maxIrLen_ - 1);
    if (neededFft != fftSize_) {
        fftSize_ = neededFft;
        prepareIRFFT(fftSize_);
        overlapL_.assign(fftSize_ - nSamples, 0.f);
        overlapR_.assign(fftSize_ - nSamples, 0.f);
    }

    size_t fftLen = fftSize_ / 2 + 1;
    std::vector<float> tmpTime(fftSize_);
    std::vector<fftwf_complex> tmpFreq(fftLen);
    std::vector<fftwf_complex> outFreqL(fftLen);
    std::vector<fftwf_complex> outFreqR(fftLen);
    std::fill(outFreqL.begin(), outFreqL.end(), fftwf_complex{0.f,0.f});
    std::fill(outFreqR.begin(), outFreqR.end(), fftwf_complex{0.f,0.f});

    for (size_t i = 0; i < nSpeakers_; ++i) {
        std::fill(tmpTime.begin(), tmpTime.end(), 0.f);
        std::copy(input[i].begin(), input[i].end(), tmpTime.begin());
        fftwf_plan fwd = fftwf_plan_dft_r2c_1d(fftSize_, tmpTime.data(), tmpFreq.data(), FFTW_ESTIMATE);
        fftwf_execute(fwd);
        fftwf_destroy_plan(fwd);
        for (size_t j = 0; j < fftLen; ++j) {
            float a = tmpFreq[j][0];
            float b = tmpFreq[j][1];
            outFreqL[j][0] += a * irFFTLeft_[i][j][0] - b * irFFTLeft_[i][j][1];
            outFreqL[j][1] += a * irFFTLeft_[i][j][1] + b * irFFTLeft_[i][j][0];
            outFreqR[j][0] += a * irFFTRight_[i][j][0] - b * irFFTRight_[i][j][1];
            outFreqR[j][1] += a * irFFTRight_[i][j][1] + b * irFFTRight_[i][j][0];
        }
    }

    outLeft.assign(fftSize_, 0.f);
    outRight.assign(fftSize_, 0.f);
    fftwf_plan invL = fftwf_plan_dft_c2r_1d(fftSize_, outFreqL.data(), outLeft.data(), FFTW_ESTIMATE);
    fftwf_plan invR = fftwf_plan_dft_c2r_1d(fftSize_, outFreqR.data(), outRight.data(), FFTW_ESTIMATE);
    fftwf_execute(invL);
    fftwf_execute(invR);
    fftwf_destroy_plan(invL);
    fftwf_destroy_plan(invR);

    for (float &v : outLeft) v /= fftSize_;
    for (float &v : outRight) v /= fftSize_;

    size_t overlapSize = fftSize_ - nSamples;
    if (overlapL_.size() != overlapSize) {
        overlapL_.assign(overlapSize, 0.f);
        overlapR_.assign(overlapSize, 0.f);
    }
    for (size_t i = 0; i < overlapSize; ++i) {
        outLeft[i] += overlapL_[i];
        outRight[i] += overlapR_[i];
    }
    for (size_t i = 0; i < overlapSize; ++i) {
        overlapL_[i] = outLeft[nSamples + i];
        overlapR_[i] = outRight[nSamples + i];
    }
    outLeft.resize(nSamples);
    outRight.resize(nSamples);
}