from flask import Flask, render_template, request
from nltk.tokenize import word_tokenize
import nltk
import random

# Initialize NLTK tokenizer and download necessary data
nltk.download('punkt')

# Define responses for the bot
responses = {
    "greetings": [
        "Hello! How can I assist you today?",
        "Hi there! What can I help you with?",
        "Hey, good to see you! What's your question?"
    ],
    "name": [
        "I'm your assistant. You can call me RadarBot.",
        "People usually call me RadarBot."
    ],
    "age": [
        "I don't have an age in the human sense. I'm here to help you."
    ],
    "default": [
        "I'm sorry, I didn't quite catch that. Could you ask again?",
        "I'm not sure I understand. Could you rephrase that?",
        "Could you please provide more details?"
    ],
    "fmcw": {
        "radar": "Frequency-Modulated Continuous Wave radar (FMCW radar) is a special type of radar sensor. Unlike simple continuous wave radar (CW radar), FMCW radar modulates its operating frequency during measurement. This modulation allows FMCW radar to accurately measure distance and velocity of targets.",
        "full form": "FMCW radar (Frequency-Modulated Continuous Wave radar)",
        "advantages": "FMCW radar can change operating frequency during measurement, enabling accurate range measurements through frequency or phase modulation.",
        "disadvantages of cw": "Simple CW radar lacks timing marks to accurately measure transmit-receive cycles and determine range, unlike FMCW radar.",
        "range measurement": "Uses frequency modulation to generate a time reference for measuring stationary object distances. The delay Δt caused by frequency change in the echo signal is measured.",
        "comparison pulse radar": "In pulse radar, runtime is directly measured, whereas FMCW radar measures differences in phase or frequency between transmitted and received signals.",
        "small ranges": "Can measure very small distances to the target, with the minimal measured range comparable to the transmitted wavelength.",
        "range velocity": "Capable of measuring both the target's range (distance) and its relative velocity simultaneously.",
        "accuracy of fmcw": "Provides very high accuracy in determining the distance to the target.",
        "low frequency processing": "Signal processing after mixing is done at a low frequency range, which simplifies the implementation of processing circuits.",
        "safety advantages": "Does not emit pulses with high peak power, offering safety benefits compared to pulse radar systems.",
        "frequency based measurement": "Distance is determined by comparing the frequency of the received signal to the reference (usually the transmission signal).",
        "long transmitted waveform duration": "The duration T of the transmitted waveform is much longer than the required receiving time for the desired distance measurement range.",
        "distance calculation relation": "The distance R to the reflecting object is determined using the formula R = c0 * Δt / (2 * Δf), where c0 is the speed of light, Δt is the delay time, and Δf is the measured frequency difference.",
        "linear frequency change": "If frequency change is linear over a wide range, distance can be determined by simple frequency comparison, proportional to Δf.",
        "doppler effect": "If the reflecting object has radial speed relative to the antenna, the echo signal includes a Doppler frequency fD. The radar measures both Δf (distance information carrier) and fD (velocity information carrier), adjusting for movement direction and modulation.",
        "measurement during sawtooth": "During a falling edge of a sawtooth modulation, fD is subtracted from the runtime frequency change. If the object moves away, the Doppler frequency further reduces the echo signal frequency.",
        "frequency deviation resolution": "By choosing the frequency deviation per unit of time (d(f)/d(t)), the radar resolution (ΔfFFT) can be determined. This relates to the smallest measurable frequency difference, crucial for range resolution.",
        "duration frequency increase": "The duration of the increasing frequency (longer edge of the red sawtooth in Figure 1) determines the maximum non-ambiguous range. It ensures temporal overlap of delayed received signals with transmitted signals.",
        "maximum frequency shift steepness": "Maximum frequency shift and steepness of the edge can be adjusted based on technological capabilities, affecting both range resolution and maximum range.",
        "maximum unambiguous range": "Maximum unambiguous range is determined by the necessary temporal overlap of delayed received signals with transmitted signals, typically exceeding energetic range limitations due to free space loss.",
        "bandwidth influence resolution": "Range resolution in FMCW radar is influenced by the bandwidth (BW) of the transmitted signal, akin to chirp radar. Fast Fourier Transform (FFT) capabilities determine resolution based on the duration of the sawtooth (Τ).",
        "example scenario": "For instance, with a linear frequency shift over 1 ms, theoretically achieving a maximum unambiguous range of under 150 km is possible. Practical limitations such as transmitter power affect achievable ranges.",
        "frequency shift effect range resolution": "A frequency shift of 250 MHz, with a 4 ns delay, results in a 1 kHz frequency difference, corresponding to a range resolution of 0.6 m. FMCW radar's ability to measure such frequencies in the audio range simplifies technical complexity compared to pulse radar.",
        "angular resolution antenna beamwidth": "As with any radar system, FMCW radar's angular resolution in detecting objects is influenced by the antenna beamwidth alongside the allocated bandwidth.",
        "sawtooth modulation": "Used for large range measurements with minimal influence from Doppler frequency. Commonly used in applications like maritime navigation radar.",
        "triangular modulation": "Enables easy separation of the difference frequency Δf from the Doppler frequency fD. Useful for applications requiring clear distinction between range and velocity measurements.",
        "square wave modulation": "Provides precise distance measurement at close range by phase comparison of echo signal frequencies. However, it cannot easily separate echo signals from multiple targets and offers a limited unambiguous range.",
        "stepped modulation": "Used in interferometric measurements to extend the unambiguous measuring range. Allows for more complex distance measurements.",
        "sinusoidal modulation": "Historically used, realized by rotating a capacitor plate in the transmitter oscillator's resonance chamber. Utilizes the linear part of the sine function near zero crossing for specific radar applications.",
        "linear sawtooth frequency changing": "In FMCW radar, linear sawtooth frequency changing involves modulating the radar signal with a linear increase or decrease in frequency over time. This modulation creates a time delay in the echo signal, known as the beat frequency, which correlates with the distance to the reflecting object.",
        "delay effect on echo signal": "The delay caused by linear sawtooth frequency changing shifts the echo signal in time, resulting in a measurable frequency difference between the transmitted and received signals.",
        "beat frequency": "The frequency difference between the actual transmitted frequency and the delayed echo signal in FMCW radar, used to determine the distance to the reflecting object.",
        "Doppler frequency and modulation": "Linear sawtooth frequency modulation in FMCW radar can be affected by Doppler frequency shifts, where movement of the reflecting object alters the frequency of the echo signal. However, FMCW radar may not always distinguish between beat and Doppler frequencies, leading to potential measurement errors.",
        "optimal frequency sweep": "Choosing an optimal frequency sweep in FMCW radar considers minimizing expected Doppler frequencies to ensure accurate distance measurement and minimize measurement errors.",
        "maritime navigation radar example": "In maritime navigation radar applications, FMCW radar operates in frequency bands like X-band, where expected Doppler frequencies due to boat speeds are relatively small (e.g., up to 666 Hz). This ensures minimal measurement error, even with boats moving at speeds up to 10 meters per second relative to each other.",
        "triangular frequency changing": "In FMCW radar, triangular frequency changing involves modulating the radar signal with a triangular-shaped frequency pattern. This pattern allows distance measurements to be conducted both during the rising and falling edges of the waveform.",
        "distance measurement on rising and falling edges": "Triangular frequency modulation in FMCW radar enables distance measurement by comparing the transmitted and received signals during both the rising and falling edges of the triangular waveform.",
        "effect of Doppler frequency": "Doppler frequency in triangular frequency changing shifts the echo signal vertically (as shown in Figure 3). The frequency difference during the rising edge includes the sum of Δf (beat frequency) and fD (Doppler frequency), while during the falling edge, it reflects the difference between these two frequencies.",
        "accuracy of distance determination": "Despite Doppler frequency effects, triangular frequency changing allows for accurate distance determination by averaging measurements from both edges of the triangular pattern. The difference between the two frequency differences provides twice the Doppler frequency, which can be precisely determined through digital signal processing.",
        "digital signal processing for Doppler frequency": "To accurately determine Doppler frequency in FMCW radar using triangular modulation, digital signal processing is essential. This involves storing and comparing the measured frequency differences from the rising and falling edges of the triangular waveform.",
        "Doppler frequency-adjusted frequency for distance determination": "In FMCW radar, the frequency f(R) used for distance determination is adjusted for Doppler frequency fD, which measures the speed of a moving target. Δf1 and Δf2 represent the frequency differences at the rising and falling edges of the radar signal, respectively. Formula (1) calculates the exact distance using these parameters.",
        "limitations of Doppler frequency measurement with multiple reflective objects": "A drawback of using Doppler frequency in FMCW radar is the inability to uniquely associate measured Doppler frequencies with specific targets when multiple reflective objects are present. This can lead to ghost targets, where incorrect Doppler frequencies are erroneously assigned to distances, creating misleading target positions.",
        "resolution with different slope steepness": "To mitigate the issue of ghost targets in FMCW radar, measuring cycles with varying modulation slope steepness can be employed. By ensuring that target coordinates align consistently across different modulation cycles, only genuine targets are displayed, reducing the likelihood of ghost targets.",
        "Frequency Shift Keying (FSK)": "FSK in FMCW radar involves switching between two transmission frequencies using a rectangular control voltage. Two methods are used to process the transceiver output signals: measuring the duration of frequency changes and comparing phase angles of echo signals.",
        "measurement of frequency change duration": "One approach in FSK is to measure the duration of frequency changes, where the envelope of the output signal represents a pulse width used to determine distance. However, this method is prone to inaccuracies and technological complexity similar to pulse radar methods.",
        "phase comparison for distance measurement": "Another method in FSK is to compare phase angles of echo signals from different transmission frequencies. This method uses the phase difference between echo signals, detected as a DC voltage at the output of the mixer, to measure distance. Digital storage of voltage values is necessary due to the sequential nature of echo signal measurement.",
        "limitations of phase difference measurement": "Due to the periodicity of sine waves, phase difference measurement in FSK has a limited unambiguous measurement range. For instance, a 20 MHz frequency difference results in an unambiguous range of 15 meters. Multiple targets at close range cannot be resolved individually, as the phase angle measurement only reflects the strongest target.",
        "integration of time and phase analysis": "To enhance distance determination accuracy, FMCW radar can integrate both time-dependent and phase-based analysis methods. Time-dependent measurement provides rough evaluations, while phase analysis offers detailed distance results. This approach mitigates the limitations of phase difference measurement and extends the maximum unambiguous range of distance measurement.",
        "advantages of stepped frequency modulation": "Stepped frequency modulation in FMCW radar offers similar advantages to square-wave modulation. It operates by sequentially transmitting multiple frequencies, allowing phase angle measurement of echo signals at each frequency. This method significantly extends the unambiguous measurement range compared to single-frequency approaches.",
        "disadvantages of stepped frequency modulation": "Similar to square-wave modulation, stepped frequency modulation in FMCW radar shares its limitations. It requires accurate phase relationship measurements across multiple frequencies to avoid ambiguities in distance determination.",
        "application of interferometry in stepped frequency modulation": "A notable application of stepped frequency modulation in FMCW radar is interferometry. By observing resonances at irregularities of reflective objects across different component frequencies, interferometric measurements can be performed. This technique enhances the resolution and accuracy of distance measurements in radar applications.",
        "components of an FMCW radar sensor": "An FMCW radar sensor consists of a transceiver module and a control unit with a microprocessor. The transceiver module includes a voltage controlled oscillator (VCO) that generates the high frequency signal for transmission. This signal is fed to a transmitting antenna, and a portion of it is also sent to a mixer for down-conversion of received echo signals to baseband.",
        "role of microprocessor in FMCW radar": "The control unit houses a microprocessor that manages the transceiver operations and converts received echo signals into a digital format. It typically interfaces with external devices like personal computers via USB for further processing and analysis.",
        "antenna configuration in FMCW radar": "In FMCW radar, patch antennas are commonly used, often with separate arrays for transmitting and receiving. These antennas are placed on a common substrate, with their polarization directions often rotated 180 degrees to minimize crosstalk. Ferrite circulators or shielding plates help separate transmit and receive signals when using a single antenna configuration.",
        "signal processing requirements in FMCW radar": "Unlike pure CW radar, FMCW radar processes the entire frequency shift of the transmitter, which can range up to 250 MHz. This necessitates higher bandwidth amplifiers and analog-to-digital converters (ADCs) in the signal processing board, making it more expensive compared to CW radar systems.",
        "integration of FMCW radar modules": "Modern FMCW radar sensors or modules integrate the entire transceiver front-end, including patch antenna arrays and MMIC modules like the TRX_024_xx from Silicon Radar. These modules operate in the K-band (24.0 – 24.25 GHz) and are suitable for applications requiring speed and distance measurements.",
        "operation of Broadband Radar™": "The Broadband Radar™ operates similarly to FMCW radar but with a unique feature of stopping the frequency sweep after reaching the maximum measurement range. This results in a transmission signal that resembles pulse radar signals with intrapulse modulation. Despite this intermittent operation, it remains classified as an FMCW radar due to its fundamental frequency comparison method.",
        "data transmission and buffer usage": "Due to the intermittent nature of the frequency sweep, measured data are buffered and transmitted losslessly through narrowband lines to the display unit. This ensures that all relevant data points are available for processing and display.",
        "imaging radar requirements": "In imaging radar applications, each point on the display requires a distance measurement, with range resolution dependent on screen pixel size and signal processing speed. High-resolution screens are necessary, ensuring that each range difference corresponds to at least two pixels for accurate target depiction.",
        "range and frequency characteristics": "With a frequency shift of 65 MHz per millisecond, the Broadband Radar™ achieves precise measurements. It offers a maximum measurable range of 75 km with an unambiguous runtime measurement of up to 500 µs. This frequency deviation equates to a range resolution of approximately 2 meters.",
        "technical specifications": "The radar can resolve frequency differences up to 2 MHz, achievable with a single-chip microcomputer. This capability allows distance measurements of up to 4000 meters without the need for complex parallel filter arrangements.",
        "comparison with pulsed radar": "Compared to pulsed radar, which requires high bandwidth transmitters and fast signal digitization (around 80 MHz and 166 MHz sampling rate, respectively, for nanosecond-level time measurements), FMCW radar achieves comparable spatial resolution with simpler technical requirements.",
        "measurement presentation": "The measurement results of the FMCW radar can be presented either as a numeric value on a pointer instrument or as alpha-numeric data displayed on a screen. This flexibility allows for varied usage scenarios in different applications.",
        "accuracy and object detection": "The radar can accurately measure a single dominant object with high precision, down to the centimeter range. This capability makes it suitable for applications requiring precise distance determination, such as aircraft radio altimeters.",
        "use in aircraft radio altimeters": "In aircraft applications, FMCW radar serves as a radio altimeter, providing reliable altitude measurements. The method offers high accuracy and is capable of detecting terrain features with precision, critical for safe aircraft operations.",
        "analog pointer instrument": "Even with analog instrumentation, such as a moving coil meter (see Figure 9), FMCW radar can be integrated. The meter's inductive impedance varies with frequency, providing a value indicative of the measured distance. However, this relationship may not be linear and requires calibration for accurate distance readings.",
        "instrumentation characteristics": "The use of an analog pointer instrument highlights the adaptability of FMCW radar to traditional display methods. This approach retains reliability and simplicity, particularly beneficial in environments where digital displays may be impractical or less reliable.",
        "data transmission and buffer usage": "Due to the intermittent nature of the frequency sweep, measured data are buffered and transmitted losslessly through narrowband lines to the display unit. This ensures that all relevant data points are available for processing and display.",
        "imaging radar requirements": "In imaging radar applications, each point on the display requires a distance measurement, with range resolution dependent on screen pixel size and signal processing speed. High-resolution screens are necessary, ensuring that each range difference corresponds to at least two pixels for accurate target depiction.",
        "range and frequency characteristics": "With a frequency shift of 65 MHz per millisecond, the Broadband Radar™ achieves precise measurements. It offers a maximum measurable range of 75 km with an unambiguous runtime measurement of up to 500 µs. This frequency deviation equates to a range resolution of approximately 2 meters.",
        "technical specifications": "The radar can resolve frequency differences up to 2 MHz, achievable with a single-chip microcomputer. This capability allows distance measurements of up to 4000 meters without the need for complex parallel filter arrangements.",
        "comparison with pulsed radar": "Compared to pulsed radar, which requires high bandwidth transmitters and fast signal digitization (around 80 MHz and 166 MHz sampling rate, respectively, for nanosecond-level time measurements), FMCW radar achieves comparable spatial resolution with simpler technical requirements.",
        "measurement presentation": "The measurement results of the FMCW radar can be presented either as a numeric value on a pointer instrument or as alphanumeric data displayed on a screen. This flexibility allows for varied usage scenarios in different applications.",
        "accuracy and object detection": "The radar can accurately measure a single dominant object with high precision, down to the centimeter range. This capability makes it suitable for applications requiring precise distance determination, such as aircraft radio altimeters.",
        "use in aircraft radio altimeters": "In aircraft applications, FMCW radar serves as a radio altimeter, providing reliable altitude measurements. The method offers high accuracy and is capable of detecting terrain features with precision, critical for safe aircraft operations.",
        "analog pointer instrument": "Even with analog instrumentation, such as a moving coil meter (see Figure 9), FMCW radar can be integrated. The meter's inductive impedance varies with frequency, providing a value indicative of the measured distance. However, this relationship may not be linear and requires calibration for accurate distance readings.",
        "instrumentation characteristics": "The use of an analog pointer instrument highlights the adaptability of FMCW radar to traditional display methods. This approach retains reliability and simplicity, particularly beneficial in environments where digital displays may be impractical or less reliable."

        
    }
}


# Initialize Flask application
app = Flask(__name__)

# Define a function to process user input and return a response
import random

def check_number_of_matches(user_input):
    keywords = list(responses["fmcw"].keys())
    keyword_counts = [0] * len(keywords)

    for i, keyword in enumerate(keywords):
        words_in_keyword = keyword.split()
        for word in words_in_keyword:
            if word in user_input.lower().split():
                keyword_counts[i] += 1

    max_count = max(keyword_counts)
    if max_count == 0:
        return "No matches found."

    max_index = keyword_counts.index(max_count)
    return responses["fmcw"][keywords[max_index]]

def get_bot_response(user_text):
    tokens = word_tokenize(user_text.lower())
    
    if any(word in tokens for word in ["hi", "hello", "hey", "greetings"]):
        return random.choice(responses["greetings"])
    elif any(word in tokens for word in ["name", "called", "designation"]):
        return random.choice(responses["name"])
    elif any(word in tokens for word in ["age", "old", "year"]):
        return random.choice(responses["age"])
    elif any(word in tokens for word in ["fmcw", "radar"]):
        # Check for specific queries related to FMCW radar
        return check_number_of_matches(user_text)
    else:
        return random.choice(responses["default"])
    


# Define routes for the Flask application
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_bot_response_route():
    user_text = request.args.get('userMessage')
    bot_response = get_bot_response(user_text)
    return bot_response

if __name__ == "__main__":
    app.run(debug=True)

