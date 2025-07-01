#include "TrueRoom.h"
#include "AAX.h"
#include <algorithm>
#include <cstring>

AAX_CEffectParameters* AAX_CALLBACK TrueRoom::Create() {
    return new TrueRoom();
}

TrueRoom::TrueRoom() = default;
TrueRoom::~TrueRoom() = default;

AAX_Result TrueRoom::EffectInit() {
    // Allocate plugin parameters here
    return AAX_SUCCESS;
}

AAX_Result TrueRoom::Initialize(double sampleRate, int32_t maxBlockSize) {
    sampleRate_ = sampleRate;
    blockSize_ = static_cast<size_t>(maxBlockSize);
    return AAX_SUCCESS;
}

AAX_Result TrueRoom::ResetFieldData(AAX_CFieldIndex, void* oFieldData) const {
    // Zero buffers between processing calls
    std::memset(oFieldData, 0, sizeof(float));
    return AAX_SUCCESS;
}

AAX_Result TrueRoom::LoadHRIR(const std::string& path) {
    // Load HRIR WAV and prepare RealTimeConvolver
    if (!hrir_.loadFromWav(path))
        return AAX_ERROR_NULL_POINTER;
    convolver_ = std::make_unique<RealTimeConvolver>(hrir_.leftIRs(), hrir_.rightIRs(), blockSize_);
    return AAX_SUCCESS;
}

AAX_Result TrueRoom::ProcessAudio(const float* const* inSamples, float* const* outSamples, int32_t inNumSamples) {
    if (!convolver_)
        return AAX_ERROR_NULL_POINTER;

    convolver_->setOrientation(currentYaw_);

    size_t nSpeakers = hrir_.leftIRs().size();
    if (nSpeakers == 0)
        return AAX_ERROR_NULL_POINTER;
    std::vector<std::vector<float>> block(nSpeakers, std::vector<float>(inNumSamples));
    // Use left input for now; a real implementation would map each speaker
    // to its corresponding input channel or an encoded stream.
    for (size_t i = 0; i < nSpeakers; ++i)
        std::memcpy(block[i].data(), inSamples[0], sizeof(float) * inNumSamples);

    std::vector<float> left(inNumSamples), right(inNumSamples);
    convolver_->processBlock(block, left, right);
    std::memcpy(outSamples[0], left.data(), sizeof(float) * inNumSamples);
    std::memcpy(outSamples[1], right.data(), sizeof(float) * inNumSamples);
    return AAX_SUCCESS;
}

// ----- RealTimeConvolver implementation -----

TrueRoom::RealTimeConvolver::RealTimeConvolver(
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

TrueRoom::RealTimeConvolver::RealTimeConvolver(
    const std::map<float, std::pair<std::vector<float>, std::vector<float>>>& brirs,
    size_t maxBlockSize)
    : maxBlockSize_(maxBlockSize),
      fftSize_(0)
{
    usingBrir_ = true;
    nSpeakers_ = 2;
    maxIrLen_ = 0;
    for (const auto& kv : brirs) {
        brirAngles_.push_back(kv.first);
        maxIrLen_ = std::max({maxIrLen_, kv.second.first.size(), kv.second.second.size()});
    }
    fftSize_ = nextPow2(maxBlockSize_ + maxIrLen_ - 1);
    size_t fftLen = fftSize_ / 2 + 1;
    brirFFTLeft_.assign(brirAngles_.size(), std::vector<fftwf_complex>(fftLen));
    brirFFTRight_.assign(brirAngles_.size(), std::vector<fftwf_complex>(fftLen));
    std::vector<float> tmp(fftSize_);
    size_t idx = 0;
    for (const auto& kv : brirs) {
        std::fill(tmp.begin(), tmp.end(), 0.f);
        std::copy(kv.second.first.begin(), kv.second.first.end(), tmp.begin());
        fftwf_plan p = fftwf_plan_dft_r2c_1d(fftSize_, tmp.data(), brirFFTLeft_[idx].data(), FFTW_ESTIMATE);
        fftwf_execute(p);
        fftwf_destroy_plan(p);

        std::fill(tmp.begin(), tmp.end(), 0.f);
        std::copy(kv.second.second.begin(), kv.second.second.end(), tmp.begin());
        p = fftwf_plan_dft_r2c_1d(fftSize_, tmp.data(), brirFFTRight_[idx].data(), FFTW_ESTIMATE);
        fftwf_execute(p);
        fftwf_destroy_plan(p);
        ++idx;
    }
    overlapL_.assign(fftSize_ - maxBlockSize_, 0.f);
    overlapR_.assign(fftSize_ - maxBlockSize_, 0.f);
}

TrueRoom::RealTimeConvolver::~RealTimeConvolver() {}

size_t TrueRoom::RealTimeConvolver::nextPow2(size_t x) const {
    size_t p = 1;
    while (p < x) p <<= 1;
    return p;
}

void TrueRoom::RealTimeConvolver::prepareIRFFT(size_t fftSize) {
    size_t fftLen = fftSize / 2 + 1;
    irFFTLeft_.assign(nSpeakers_, std::vector<fftwf_complex>(fftLen));
    irFFTRight_.assign(nSpeakers_, std::vector<fftwf_complex>(fftLen));
    std::vector<float> tmp(fftSize);
    if (usingBrir_) {
        std::vector<float> dists(brirAngles_.size());
        for (size_t i = 0; i < brirAngles_.size(); ++i) {
            float diff = std::fabs(fmodf(std::fabs(brirAngles_[i] - yaw_), 360.f));
            dists[i] = std::min(diff, 360.f - diff);
        }
        std::vector<float> weights(brirAngles_.size(), 0.f);
        bool exact = false;
        for (float d : dists) if (d == 0.f) { exact = true; break; }
        if (exact) {
            for (size_t i = 0; i < dists.size(); ++i) weights[i] = dists[i] == 0.f ? 1.f : 0.f;
        } else {
            float sum = 0.f;
            for (float d : dists) sum += 1.f / d;
            for (size_t i = 0; i < dists.size(); ++i) weights[i] = (1.f / dists[i]) / sum;
        }

        std::vector<fftwf_complex> inL(fftLen); 
        std::vector<fftwf_complex> inR(fftLen); 

        std::fill(tmpTime.begin(), tmpTime.end(), 0.f);
        std::copy(input[0].begin(), input[0].end(), tmpTime.begin());
        fftwf_plan fwd = fftwf_plan_dft_r2c_1d(fftSize_, tmpTime.data(), inL.data(), FFTW_ESTIMATE);
        fftwf_execute(fwd);
        fftwf_destroy_plan(fwd);

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

void TrueRoom::RealTimeConvolver::processBlock(const std::vector<std::vector<float>>& input,
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
        std::copy(input[1].begin(), input[1].end(), tmpTime.begin());
        fwd = fftwf_plan_dft_r2c_1d(fftSize_, tmpTime.data(), inR.data(), FFTW_ESTIMATE);
        fftwf_execute(fwd);
        fftwf_destroy_plan(fwd);

        std::vector<fftwf_complex> irL(fftLen); 
        std::vector<fftwf_complex> irR(fftLen);
        for (size_t j = 0; j < fftLen; ++j) {
            irL[j][0] = irL[j][1] = 0.f;
            irR[j][0] = irR[j][1] = 0.f;
        }
        for (size_t i = 0; i < brirAngles_.size(); ++i) {
            for (size_t j = 0; j < fftLen; ++j) {
                irL[j][0] += weights[i] * brirFFTLeft_[i][j][0];
                irL[j][1] += weights[i] * brirFFTLeft_[i][j][1];
                irR[j][0] += weights[i] * brirFFTRight_[i][j][0];
                irR[j][1] += weights[i] * brirFFTRight_[i][j][1];
            }
        }

        for (size_t j = 0; j < fftLen; ++j) {
            float a = inL[j][0];
            float b = inL[j][1];
            outFreqL[j][0] = a * irL[j][0] - b * irL[j][1];
            outFreqL[j][1] = a * irL[j][1] + b * irL[j][0];

            a = inR[j][0];
            b = inR[j][1];
            outFreqR[j][0] = a * irR[j][0] - b * irR[j][1];
            outFreqR[j][1] = a * irR[j][1] + b * irR[j][0];
        }
    } else {
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

void TrueRoom::RealTimeConvolver::setOrientation(float yaw) {
    yaw_ = yaw;
}

AAX_Result TrueRoom::SetYaw(float yaw) {
    currentYaw_ = yaw;
    return AAX_SUCCESS;
}

