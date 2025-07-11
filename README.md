# Earprint
#
# This file is part of a modified fork of Impulcifer by Jaakko Pasanen.
# Modifications © 2025 Blaring Sound LLC, licensed under the MIT License.

Built off of jaakkopasanen's Impulcifer project.
Modified and expanded to include 9.1.6 speaker formats.

This project is a fork of Impulcifer by Jaakko Pasanen.
Modifications © 2025 Blaring Sound LLC. Licensed under the MIT License.
File headers referencing this fork have been consolidated into NOTICE.md.

Earprint is a tool for creating binaural room impulse responses (BRIR) for speaker virtualization on headphones.

Normally headphones sound inside your head which is a clear disadvantage for games and movies but also for music
because basically all material has been created for speakers. Virtual surround technologies for headphones have existed
for a some time by now but almost all of them fail to fulfill expectations of out of head sound localization and the
naturalness of speakers. This is because your brains have learned to localize sounds only with your ears and head and
not with anyone else's. Surround sound on headphones can only be convincing when the surround virtualization technology
has been tailored for your ears. BRIR is the tailored model for supreme virtual speaker surround on headphones. When
done right virtualized speakers can be indistinguishable from real speakers.

Watch these videos to get an idea what good BRIRs can do. The method used by Smyth Realizer and Creative Super X-Fi
demos is the same what Earprint uses.

- [Realiser A16 Smyth Research (Kickstarter project)](https://www.youtube.com/watch?v=3mZhN3OG-tc)
- [a16 realiser](https://www.youtube.com/watch?v=RtY9QIkRJxA)
- [Creative Super X-Fi 3D Immersive Headphone Technology at CES 2018](https://www.youtube.com/watch?v=mAidEm9_JYM)

These demos are trying to make headphones sound as much as possible like the speakers they have in the demo room for a
good [wow](https://www.youtube.com/watch?v=KlLMlJ2tDkg) effect. Earprint actually takes this even further because
Earprint can do measurements with only one speaker so you don't need access to surround speaker setup and can do room
acoustic corrections which are normally not possible in real rooms with DSP.

## License

This project is a fork of [Impulcifer](https://github.com/jaakkopasanen/Impulcifer) by Jaakko Pasanen, originally licensed under the MIT License.

All original code by Jaakko Pasanen remains under the MIT License.  
Modifications and additions © 2025 Blaring Sound LLC are also licensed under the MIT License.

See the `LICENSE` file for full details.

## Architecture

The codebase is organized using a lightweight **Model–View–ViewModel** (MVVM) pattern.
View classes like `gui.py` interact with `viewmodel` classes that expose user
commands and validation logic. Domain data is encapsulated in simple models under
the `models` package. This separation keeps the GUI free of processing logic and
makes core functionality testable without a running interface.
For more details see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Configuration

Processing options such as headphone EQ or room correction are controlled
via the `config.py` module. The `settings` object holds the default values
which can be tweaked programmatically before calling any processing
functions. Command line tools read these defaults as well, so adjusting
`settings` allows changing behaviour without editing multiple scripts.

## Installing
Earprint is used from a command line and requires some prerequisites. These installation instructions will guide you
through installing everything that is needed to run Earprint on you own PC.

- Download and install Git: https://git-scm.com/downloads. When installing Git on Windows, use Windows SSL verification
instead of Open SSL or you might run into problems when installing project dependencies.
 - Download and install 64-bit [Python 3.8–3.11](https://www.python.org/getit/). Make sure to check *Add Python to PATH*.
- You may need to install libsndfile if you're having problems with `soundfile` when installing `requirements.txt`.
- Install the PortAudio library if `sounddevice` reports "PortAudio library not found" (for example `brew install portaudio` on macOS).
- On Linux you may need to install Python dev packages
```bash
sudo apt install python3-dev python3-pip python3-venv
```
- On Linux you may need to install [pip](https://pip.pypa.io/en/stable/installing/)
- On Windows you may need to install
[Microsoft Visual C++ Redistributable for Visual Studio 2015, 2017, or 2019](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads)

Rest will be done in terminal / command prompt. On Windows you'll find it by searching `cmd` in Start menu.
You should be able to simply copy and paste in these commands. 

- Git clone Earprint. This will create a folder in your home folder called `Earprint`. See [Updating](#updating)
for other versions than the latest.  
```bash
git clone https://github.com/n1299cb/Earprint
```
- Go to Earprint folder.  
```bash
cd Earprint
```
- Create virtual environment for the project.  
```bash
python -m venv venv
```
- Activate virtualenv.  
```bash
# On Windows
venv\Scripts\activate
# On Mac and Linux
. venv/bin/activate
```
- Update pip and setuptools
```bash
python -m pip install -U pip
```
- Install required packages.  
```bash
pip install -U -r requirements.txt
```
- Install the package itself so the scripts are available on your PATH.
```bash
pip install .
```
- Verify installation. You should see help printed if everything went well.
```bash
python earprint.py --help
```

When coming back at a later time you'll only need to activate virtual environment again before using Earprint.
```bash
cd Earprint
# On Windows
venv\Scripts\activate
# On Mac and Linux
. venv/bin/activate
```

### Updating
Earprint is under active development and updates quite frequently. Take a look at the [Changelog](./CHANGELOG.md) to
see what has changed.

Versions in Changelog have Git tags with which you can switch to another version than the latest one:
```bash
# Check available versions
git tag
# Update to a specific version
git checkout 1.0.0
```

You can update your own copy to the latest versions by running:
```bash
git checkout master
git pull
```

required packages change quite rarely but sometimes they do and then it's necessary to upgrade them
```bash
python -m pip install -U -r requirements.txt
```
You can always invoke the update for required packages, it does no harm when nothing has changed.

### Running the Python GUI

Launch the graphical interface with:
```bash
python gui.py
```
If PySide6 can't find its Qt platform plugins you may get an error like:
```
qt.qpa.plugin: Could not find the Qt platform plugin "cocoa" in ""
```
On macOS set `QT_QPA_PLATFORM_PLUGIN_PATH` to the plugins shipped with PySide6.
You won't see any output from the command, so you can verify the value after
running it:
```bash
export QT_QPA_PLATFORM_PLUGIN_PATH=$(python3 - <<'EOF'
import PySide6, pathlib
print(pathlib.Path(PySide6.__file__).resolve().parent / "Qt" / "plugins")
EOF
)
echo "Using Qt plugins from: $QT_QPA_PLATFORM_PLUGIN_PATH"
```
Once this variable is configured, run `python gui.py` again.

### Running the Swift GUI

The repository also ships with a native macOS interface written in SwiftUI.
Build and launch it with:
```bash
cd EarprintGUI
swift run
```
The Swift app mirrors the tabs of the Python GUI and executes the same
Python scripts under the hood. A recent Xcode or the Swift toolchain for
macOS 12+ is required.

### Troubleshooting the Swift GUI

If device lists remain empty or the app logs `PortAudio library not found`, the
`sounddevice` module couldn't access the PortAudio backend. On macOS install it
with Homebrew and then reinstall the Python requirements:

```bash
brew install portaudio
pip install -U -r requirements.txt
```
You can verify device enumeration works with:

```bash
python3 -c "import sounddevice, json; print(json.dumps(sounddevice.query_devices()))"
```

## Development
For contributor setup and test instructions see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).
To build a Pro Tools plug‑in see [docs/AAX_PLUGIN.md](docs/AAX_PLUGIN.md).


## Demo
The actual BRIR measurements require a little investment in measurement gear and the chances are that you're here before
you have acquired them. There is a demo available for testing out Earprint without having to do the actual
measurements. `data/demo` folder contains five measurement files which are needed for running Earprint.
`headphones.wav` has the sine sweep recordings done with headphones and all the rest files are recordings done with
stereo speakers in multiple stages.

You can try out what Earprint does by running:
```bash
python earprint.py --test_signal=data/sweep-6.15s-48000Hz-32bit-2.93Hz-24000Hz.pkl --dir_path=data/demo 
```
Earprint will now process the measurements and produce `hrir.wav` and `hesuvi.wav` which can be used with headphone
speaker virtualization software such as [HeSuVi](https://sourceforge.net/projects/hesuvi/) to make headphones sound like
speakers in a room. When testing with HeSuVi copy `hesuvi.wav` into `C:\Program Files\Equalizer APO\config\Hesuvi\hrir`,
(re)start HeSuVi and select `hesuvi.wav` from the Common HRIRs list on Virtualization tab.

## Repository Assets
Sample measurement data lives under the `data/` directory and reference
images used in the documentation are stored in `img/`. These assets are
kept in the repository for convenience as they are required when running
the demo or the unit tests. Local helper files such as `atmos_brir for
EQAPO.txt` or `webcam.html` have been removed and are ignored via
`.gitignore` to avoid cluttering the version history.

## Measurement
BRIR measurements are done with binaural microphones which are also called ear canal blocking microphones or in-ear
microphones. Exponential sine sweep test signal is played on speakers and the sound is recorded with the microphones at
ear canal openings. This setup ensures that the sound measured by the microphones is affected by the room, your body,
head and ears just like it is when listening to music playing on speakers. Earprint will then transform these
recordings into impulse responses, one per each speaker-ear pair.

Earprint ships with ready-made sweep files at
`data/sweep-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav` and
`data/sweep-6.15s-48000Hz-32bit-2.93Hz-24000Hz.pkl` along with a sample
capture set in `data/demo`. When launching the GUI these paths are filled in automatically, but you can point the
interface to your own sweep or capture directory at any time.

Guide for doing the measurements yourself and comments about the gear needed to do it can be found in
[measurements](https://github.com/jaakkopasanen/Impulcifer/wiki/Measurements) page of Impulcifer wiki. The whole process
is really quite simple and doesn't take more than couple of minutes. Reading through the measurement guide is most
strongly recommended when doing measurements the first time or using a different speaker configuration the first time.

You can automate the setup with the helper scripts. Run `python generate_layout.py --layout=7.1 --dir=data/my_hrir` (or another layout) to create the expected folder structure and then start `python capture_wizard.py --layout=7.1 --dir=data/my_hrir` to record each group interactively.

Following is a quick reference for running the measurements once you're familiar with the process. If you always use
`my_hrir` as the temporary folder and rename it after the processing has been done, you don't have to change the
following commands at all and you can simply copy-paste them for super quick process.

### 7.1 Speaker Setup
Steps and commands for doing measurements with 7.1 surround system:

| Setup | Command |
|-------|---------|
| Put microphones in ears, put headphones on | `python recorder.py --play="data/sweep-seg-FL,FR-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/headphones.wav"` |
| Take heaphones off, look forward | `python recorder.py --play="data/sweep-seg-FL,FC,FR,SR,BR,BL,SL-7.1-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/FL,FC,FR,SR,BR,BL,SL.wav"` |

After each capture a report file `<record>_report.txt` is written next to the WAV file with peak level, headroom and noise floor details.

### 7.1.4 Speaker Setup
SMPTE channel order: `FL, FR, FC, LFE, SL, SR, BL, BR, TFL, TFR, TBL, TBR`

Example sweep generation:
```bash
python impulse_response_estimator.py --dir_path=data \
    --fs=48000 --speakers=FL,FC,FR,SL,SR,BL,BR,TFL,TFR,TBL,TBR --tracks=7.1.4
```

Steps and commands for doing measurements with 7.1.4 surround system:

| Setup | Command |
|-------|---------|
| Put microphones in ears, put headphones on | `python recorder.py --play="data/sweep-seg-FL,FR-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/headphones.wav"` |
| Take heaphones off, look forward | `python recorder.py --play="data/sweep-seg-FL,FC,FR,SL,SR,BL,BR,TFL,TFR,TBL,TBR-7.1.4-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/FL,FC,FR,SL,SR,BL,BR,TFL,TFR,TBL,TBR.wav"` |

### 9.1.6 Speaker Setup
SMPTE channel order: `FL, FR, FC, LFE, SL, SR, BL, BR, WL, WR, TFL, TFR, TSL, TSR, TBL, TBR`

Example sweep generation:
```bash
python impulse_response_estimator.py --dir_path=data \
    --fs=48000 --speakers=FL,FC,FR,SL,SR,BL,BR,WL,WR,TFL,TFR,TSL,TSR,TBL,TBR --tracks=9.1.6
```

Steps and commands for doing measurements with 9.1.6 speaker layout:

| Setup | Command |
|-------|---------|
| Put microphones in ears, put headphones on | `python recorder.py --play="data/sweep-seg-FL,FR-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/headphones.wav"` |
| Take heaphones off, look forward | `python recorder.py --play="data/sweep-seg-FL,FC,FR,SL,SR,BL,BR,WL,WR,TFL,TFR,TSL,TSR,TBL,TBR-9.1.6-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/FL,FC,FR,SL,SR,BL,BR,WL,WR,TFL,TFR,TSL,TSR,TBL,TBR.wav"` |


### Stereo Speaker Setup
Steps and commands for doing measurements with two speakers in four stages:

| Setup | Command |
|-------|---------|
| Put microphones in ears, put on headphones | `python recorder.py --play="data/sweep-seg-FL,FR-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/headphones.wav"` |
| Take heaphones off, look forward | `python recorder.py --play="data/sweep-seg-FL,FR-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/FL,FR.wav"` |
| Look 120 degrees left (left speaker should be on your right) | `python recorder.py --play="data/sweep-seg-FL,FR-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/SR,BR.wav"` |
| Look 120 degrees right (right speaker should be on your left) | `python recorder.py --play="data/sweep-seg-FL,FR-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/BL,SL.wav"` |
| Look directly at the left speaker OR... | `python recorder.py --play="data/sweep-seg-FL-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/FC.wav"` |
| ...Look directly at the right speaker | `python recorder.py --play="data/sweep-seg-FR-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/FC.wav"` |

### Single Speaker
Steps and command for doing measurements with just a single speaker in 7 steps. All speaker measurements use either
`sweep-seg-FL-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav` or
`sweep-seg-FR-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav` depending if the speaker is connected to left or right
cable terminals in the amplifier. These commands assume the speaker is connected to left speaker terminals.

| Setup | Command |
|-------|---------|
| Put microphones in ears, put on headphones | `python recorder.py --play="data/sweep-seg-FL,FR-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/headphones.wav"` |
| Look 30 degrees right of the speaker (speaker on your front left) | `python recorder.py --play="data/sweep-seg-FL-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/FL.wav"` |
| Look directly at the speaker | `python recorder.py --play="data/sweep-seg-FL-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/FC.wav"` |
| Look 30 degrees left of the speaker (speaker on you front right) | `python recorder.py --play="data/sweep-seg-FL-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/FR.wav"` |
| Look 90 degrees left of the speaker (speaker on your right) | `python recorder.py --play="data/sweep-seg-FL-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/SR.wav"` |
| Look 150 degrees left of the speaker (speaker on your back right) | `python recorder.py --play="data/sweep-seg-FL-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/BR.wav"` |
| Look 150 degrees right of the speaker (speaker on you back left) | `python recorder.py --play="data/sweep-seg-FL-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/BL.wav"` |
| Look 90 degrees right of the speaker (speaker on your left) | `python recorder.py --play="data/sweep-seg-FL-stereo-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav" --record="data/my_hrir/SL.wav"` |

## Processing
Once you have obtained the sine sweep recordings, you can turn them into a BRIR file with Earprint. All the processing
is done by running a single command on command line. The command below assumes you have made a speaker recordings and
a headphones recording and saved the recording files into `data/my_hrir` folder. Start command prompt, jump to
Earprint folder and activate the virtual environment as described in the installation instructions if you don't have
command prompt open yet. Sine sweep recordings are processed by running `earprint.py` with Python as shown below.
```bash
python earprint.py --test_signal="data/sweep-6.15s-48000Hz-32bit-2.93Hz-24000Hz.pkl" \
    --dir_path="data/my_hrir" --delay-file=delays.json --plot
```

The optional `--delay-file` argument loads per-speaker timing offsets from a JSON or CSV table.

You should have several WAV files and graphs in the folder. `hesuvi.wav` can now be used with HeSuVi to make your
headphones sound like speakers.

`--dir_path=data/my_hrir` tells Earprint that the recordings can be found in a folder called `my_hrir` under `data`.
Earprint will also write all the output files into this folder.

Earprint always needs to know which sine sweep signal was used during recording process. Test signal can be either a
WAV (`.wav`) file or a Pickle (`.pkl`) file. Test signal is read from a file called `test.wav` or `test.pkl`.
`impulse_response_estimator.py` produces both but using a Pickle file is a bit faster. Pickle files cannot be
played back directly with `recorder.py` or the GUI. Use the WAV version when capturing measurements.
An alternative way of passing the test signal is with a command line argument `--test_signal` which takes
the path to the file, for example `--test_signal="data/sweep-6.15s-48000Hz-32bit-2.93Hz-24000Hz.wav"`.

Sine sweep recordings are read from WAV files which have speaker names separated with commas and `.wav` extension eg.
`FL,FR.wav`. The individual speakers in the given file must be recorded in the order of the speaker names in the file
name. There can be multiple files if the recording was done with multiple steps as is the case when recording 7.1 setup
with two speakers. In that case there should be `FL,FR.wav`, `SR,BR.wav`, `BL,SL.wav` and `FC.wav` files in the folder.

#### Room Correction
Similar pattern is used for room acoustics measurements. The idea is to measure room response with a calibrated
measurement microphone in the exact same spot where the binaural microphones were. Room measurement files have file name
format of `room-<SPEAKERS>-<left|right>.wav`, where `<SPEAKERS>` is the comma separated list of speaker names and
`<left|right>` is either "left" or "right". This tells if the measurement microphone is measuring at the left or right
ear position. File name could be for example `room-FL,FR-left.wav`. Earprint does not support stereo measurement
microphones because vast majority of measurement microphones are mono. Room recording files need to be single track
only. Some measurement microphones like MiniDSP UMIK-1 are seen as stereo microphones by Windows and will for that
reason record a stereo file. `recorder.py` can force the capture to be one channel by setting `--channels=1`.

Generic room measurements can be done for speakers with which it's hard to position the measurement microphone
correctly. Earprint reads these measurements from `room.wav` file which can contain any number of tracks and any
number of sweeps per track. All the sweeps are being read and their frequency responses are combined. The combined
frequency response is used for room correction with the speakers that don't have specific measurements
(`room-FL,FR-left.wav` etc...).

There are two methods for combining the frequency responses: `"average"` and `"conservative"`. Average method takes the
average frequency response of all the measurements and builds the room correction equalization with that. Conservative
method takes the absolute minimum error for each frequency and only if all the measurements are on the same side of 0
level at the given frequency. This ensures that there will never be room correction adjustments that would make the
frequency response of any of the measurements worse. These methods are available with `--fr_combination_method=average`
and `--fr_combination_method=conservative`.

Upper frequency limit for room measurements can be adjusted with parameters `--specific_limit` and `--generic_limit`.
These will limit the room correction equalization to 0 dB above that frequency. This can be useful for avoiding pitfalls
of room correction in high frequencies. `--specific_limit` applies to room measurements which specify the ear and
`--generic_limit` to room measurements which don't. Typically room dominates the frequency response below 300 or 400 Hz
and speakers dominate above 700 Hz. Speaker's problems cannot be fixed based on in-room measurements and therefore the
limits should usually be placed at 700 Hz. The octave leading up to the limit (eg. 350 to 700 Hz) will be sloped down
from full EQ effect (at 350 Hz) to 0 dB at the limit (700 Hz). Other, higher, values can be tried out and they can
improve the sound but there are not guarantees about that.

Generic room measurements are not expected to be in the same location as the binaural microphones were so limiting the
equalization to less than 1 kHz is probably a good idea. Conservative combination method with several measurements is
safer method and with that it should be safer to try to increase the limit up from 1 kHz. For example
`--specific_limit=5000 --generic_limit=2000` would ensure that room correction won't adjust frequency response of BRIR
above 5 kHz for any speaker-ear pairs and above 2 kHz for speaker-ear pairs that don't have specific room measurements.

Room measurements can be calibrated with the measurement microphone calibration file called `room-mic-calibration.txt`
or `room-mic-calibration.csv`. This must be a CSV file where the first column contains frequencies and the second one
amplitude data. Data is expected to be calibration data and not equalization data. This means that the calibration data
is subtracted from the room frequency responses. An alternative way of passing in the measurement microphone calibration
file is with a command line argument `--room_mic_calibration` and it takes a path to the file eg.
`--room_mic_calibration="data/umik-1_90deg.txt"`

Room frequency response target is read from a file called `room-target.txt` or `room-target.csv`. Head related impulse
responses will be equalized with the difference between room response measurements and room response target. An
alternative way to pass in the target file is with a command line argument `--room_target` eg.
`--room_target="data/harman-in-room-loudspeaker-target.csv"`.

Room correction can be skipped by adding a command line argument `--no_room_correction` without any value.

#### Headphone Compensation
Earprint will compensate for the headphone frequency response using headphone sine sweep recording if the folder
contains file called `headphones.wav`. If you have the file but would like not to have headphone compensation, you can
simply rename the file for example as `headphones.wav.bak` and run the command again. 

Headphone equalization can be baked into the produced BRIR file by having a file called `eq.csv` in the folder. The eq 
file must be an AutoEQ produced result CSV file. Separate equalizations for left and right channels are supported with
files `eq-left.csv` and `eq-right.csv`. Headphone equalization is useful for in-ear monitors because it's not possible
to do headphone compensation with IEMs. When using IEMS you still need an around ear headphone for the headphone
compensation. **eq.wav is no longer supported!**

Earprint will bake the frequency response transformation from the CSV file into the BRIR and you can enjoy speaker
sound with your IEMs. You can generate this filter with [AutoEQ](https://github.com/jaakkopasanen/AutoEq); see usage
instructions for [using sound signatures](https://github.com/jaakkopasanen/AutoEq#using-sound-signatures) to learn how 
to transfer one headphone into another. In this case the input directory needs to point to the IEM, compensation curve
is the curve of the measurement system used to measure the IEM and the sound signature needs point to the existing
result of the headphone which was used to make the headphone compensation recording.

For example if the headphone compensation recording was made with Sennheiser HD 650 and you want to enjoy Earprint
produced BRIR with Campfire Andromeda, you should run:
```bash
python -m autoeq --input-file="measurements/oratory1990/data/in-ear/Campfire Audio Andromeda.csv" --output-dir="my-results/Andromeda (HD 650)" --target="targets/AutoEq in-ear.csv" --sound-signature="results/oratory1990/over-ear/Sennheiser HD 650/Sennheiser HD 650.csv" --equalize --bass-boost=8 --max-gain=12
```
and then copy `AutoEq/my_results/Andromeda (HD 650)/Campfire Audio Andromeda.csv` to `Earprint/data/my_hrir/eq.csv`.

See how the Harman over-ear target is used for IEM in this case. This is because the goal is to make Andromeda sound as
similar as possible to HD 650, which is an over-ear headphone. Normally with AutoEQ you would use Harman in-ear target
for IEMs but not in this case.

Headphone compensation can be skipped by adding a command line argument `--no_headphone_compensation` without any value.

#### Diffuse-Field Compensation
Add `--diffuse_field_compensation` to enable diffuse-field equalization of the HRIR. By default this processing is disabled.

#### X-Curve Compensation
Cinema playback often uses the SMPTE X-Curve. Two common variants are provided:
`minus3db_oct` (about -3 dB per octave) and `minus1p5db_oct` (about -1.5 dB per octave).
Use `--apply_x_curve` to apply one of these responses or `--remove_x_curve` to flatten a capture that already
includes it. Add `--x_curve_in_capture` when your recordings were made with the curve so that
the chosen action is applied correctly. Select the variant with `--x_curve_type=<name>`.

#### Sampling Rate
Outputs with different sampling rates than the recording sampling rate can be produced with `--fs` parameter. This
parameter takes a sampling rate in Hertz as value and will then resample the output BRIR to the desired sampling rate if
the recording and output sampling rates differ. For example `--fs=44100`.

#### Plotting Graphs
Various graphs can be produced by providing `--plot` parameter to Earprint. These can be helpful in figuring out what
went wrong if the produced BRIR doesn't sound right. Producing the plots will take some time.

- **pre** plots are the unprocessed BRIR measurement
- **room** plots are room measurements done with measurement microphone
- **post** plots are the final results after all processing

The GUI's **Visualization** tab scans the `plots` subdirectory of the selected
measurement directory. Click **Refresh** and choose a plot from the list to view
it.

#### Channel Balance Correction
Channel balance can be corrected with `--channel_balance` parameter. In ideal case this would not be needed and the
natural channel balance after headphone equalization and room correction would be perfect but this is not always the
case since there are multiple factors which affect that like placement of the binaural microphones. There are six
different strategies available for channel balance correction.

The Processing Options tab of the GUI includes a **Preview…** button which lets you audition channel balance changes
with any audio file. Move the slider to adjust right channel gain in real time and apply the chosen value directly to
the channel balance option. The drop-down list now exposes all strategies (`avg`, `min`, `left`, `right`, `mids`, and
`trend`) along with any numeric values added through the preview dialog.

Setting `--channel_balance=trend` will equalize right side by the difference trend of left and right sides. This is a
very smooth difference curve over the entire spectrum. Trend will not affect small deviations and therefore doesn't
warp the frequency response which could lead to uncanny sensations. Bass, mids and treble are all centered when using
trend. Trend is probably the best choice in most situations.

Setting `--channel_balance=mids` will find a gain level for right side which makes the mid frequencies (100, 3000)
average level match that of the left side. This is essentially an automatic guess for the numeric strategy value.

Setting `--channel_balance=1.4` or any numerical value will amplify right side IRs by that number of decibels.
Positive values will boost right side and negative values will attenuate right side. You can find the correct value by
trial and error either with Earprint or your virtualization software and running Earprint again with the best value.
Typically vocals or speech is good reference for finding the right side gain value because these are most often mixed
in the center and therefore are the most important aspect of channel balance.

Setting `--channel_balance=avg` will equalize both left and right sides to the their average frequency response and
`--channel_balance=min` will equalize them to the minimum of the left and right side frequency response curves. Using
minimum instead of average will be better for avoiding narrow spikes in the equalization curve but which is better in
the end varies case by case. These strategies might cause uncanny sensation because of frequency response warping.

`--channel_balance=left` will equalize right side IRs to have the same frequency response as left side IRs and
`--channel_balance=right` will do the same in reverse. These strategies might cause uncanny sensation because of
frequency response warping.

#### Level Adjustment
Output BRIR level can be adjusted with `--target_level` parameter which will normalize the BRIR gain to the given
numeric value. The level is calculated from all frequencies excluding lowest bass frequencies and highest treble
frequencies and then the level is adjusted to the target level. Setting `--target_level=0` will ensure that BRIR
average gain is about 0 dB. Keep in mind that there often is large variance in the gain of different frequencies so
target level of 0 dB will not mean that the BRIR would not produce clipping. Typically the desired level is several dB
negative such as `--target_level=-12.5`. Target level is a tool for having same level for different BRIRs for easier
comparison.

#### Decay Time Management
The room decay time (reverb time) captured in the binaural room impulse responses can be shortened with `--decay`
parameter. The value is a time it should take for the sound to decay by 60 dB in milliseconds. When the natural decay
time is longer than the given target, the impulse response tails will be shortened with a slope to achieve the desired
decay velocity. Decay times are not increased if the target is longer than the natural one. The decay time management
can be a powerful tool for controlling ringing in the room without having to do any physical room treatments.

### Customizing Speaker Layouts in the GUI

The Setup tab now features a **Speaker Layout** selector. Choose any of the
presets from `constants.FORMAT_PRESETS` &mdash; now including **5.1.2**, **5.1.4**,
**7.1.2**, **7.1.6**, **9.1.4** and a four channel **Ambisonics** option &mdash; or select **Custom…** to load a
comma-separated or JSON list of speaker names. Loaded layouts are used when
mapping playback channels in the **Map Channels** dialog. Custom layouts can be
saved as presets in JSON format via the **Save Layout…** button so they appear in
the selector next time the application starts.
Use **Auto Map** on the Setup tab to assign playback and recording channels automatically.

### Layout Preparation Tool

`generate_layout.py` sets up a new capture folder by writing the expected file
names for a speaker layout. Placeholder sweep files are copied for each
recording so you can verify the channel order before doing real measurements.
Run it again with `--verify` to check that all required WAV files exist and to
list any extras. The selected groups can be saved as a JSON preset with
`--save_preset layout.json`. Use `--list` to show all layouts or
`--preset_file processing-presets.json` to load custom presets.

The GUI exposes the same functionality via the **Layout Wizard** button on the
Setup tab. The wizard prompts for a layout and target directory then runs the
helper behind the scenes.

```bash
python generate_layout.py --layout=9.1.6 --dir=data/test_capture
python generate_layout.py --layout=9.1.6 --dir=data/test_capture --verify
python generate_layout.py --layout=9.1.6 --save_preset my_layout.json
```

### Capture Wizard

`capture_wizard.py` guides you through recording each speaker group. It opens
with a headphone capture, then plays the correct sweep for every group you
defined when preparing the layout. Use the `--input_device` and `--output_device`
options to select the recording interface. Alternative sweep files can be
specified with `--stereo_sweep` and `--mono_sweep`.

```bash
python capture_wizard.py --layout=9.1.6 --dir=data/my_hrir
```

Follow the prompts to position yourself and start each capture.

You can also launch this helper from the **Execution** tab of the GUI via the
*Capture Wizard* button. It uses the same prompts but displays them inside a
dialog window.

After running the processing pipeline the **Export Hesuvi Preset** button on the
Execution tab copies `hesuvi.wav` to a location of your choice. Use this to
quickly drop the file into Equalizer APO's `Hesuvi` folder or another virtual
speaker tool.


For a deeper walkthrough of these helpers, see
[docs/TOOLS.md](docs/TOOLS.md).


### Distance-Based Speaker Delays (Advanced)

Pass `--interactive_delays` to `earprint.py` to enter the angle and distance
for each speaker before processing. The helper computes timing offsets using
`utils.versus_distance()` and temporarily overrides the default zero-delay table
so non-uniform setups remain in sync.

Alternatively use `--delay-file=delays.json` to load a table of delays without
interacting. The file can be JSON or CSV with values in milliseconds:

```json
{ "FL": 0, "FR": 0, "SL": 5 }
```

```csv
speaker,delay_ms
FL,0
FR,0
SL,5
```


## Tests

Simple test scripts validate the processing pipeline. If you have real HRIR
recordings, set `EARPRINT_TEST_CAPTURE_DIR` to their directory. Otherwise the
tests automatically generate a tiny synthetic dataset.

Run them directly with Python:

```bash
python test_earprint.py       # 9.1.6 layout
python test_earprint_714.py   # 7.1.4 layout
```

## Real-Time Convolution Engine

The `realtime_convolution.py` module offers low-latency binaural rendering.
It loads the BRIRs produced by Earprint and processes any multichannel
signal using efficient FFT overlap-add convolution. The engine can stream
audio in real time with `sounddevice` or process files offline. When the
optional `pyfftw` package is installed, the convolver uses FFTW for
significantly faster transforms.

Example converting a multichannel WAV file:

```bash
python -m realtime_convolution input_multichannel.wav output_stereo.wav
```

When running on macOS, pass `host_api="Core Audio"` to force the low-latency
Core Audio backend:

```python
engine = RealTimeConvolver(hrir)
engine.start(host_api="Core Audio")
```


When enabled, the engine outputs two loudspeaker channels that preserve the
original binaural cues, closing part of the gap toward Smyth Realiser style
virtualization.