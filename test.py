

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import spacy
from flask import Flask, render_template, request

nlp = spacy.load('en')

app = Flask(__name__)

bot = ChatBot(
    "RadarBot",
    read_only=False,
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response' : "Sorry I don't have an answer for that. If you have anymore questions regarding FMCW radars please let me know" ,
            'maximum_similarity_threshold' : 0.5 ,
            'statement_comparison_function': 'chatterbot.comparisons.SpacySimilarity',
            'tagger_language': nlp
        }
    ]
)


list_to_train = [
    #greetings
    "hi",
    "Hello there! How can I be of assistance?",
    "hello",
    "Hello there! How can I be of assistance?",
    "howdy",
    "Hello there! How can I be of assistance?",
    "greetings",
    "Hello there! How can I be of assistance?",
    "yo",
    "Hello there! How can I be of assistance?",
    "hiya",
    "Hello there! How can I be of assistance?",
    "good day",
    "Hello there! How can I be of assistance?",
    "whats up",
    "Hello there! How can I be of assistance?",
    "hi there"
    "Hello there! How can I be of assistance?",
    #name
    "what's your name?",
    "My name is RadarBot",
    "what are you called",
    "My name is RadarBot",
    "how should i address",
    "My name is RadarBot",
    "what is your designation",
    "My name is RadarBot",
    "who are you",
    "My name is RadarBot",
    #age
    "how old are you",
    "I am ageless, but I was made in July 2024",
    "whats your age",
    "I am ageless, but I was made in July 2024",
    "what year were you made",
    "I am ageless, but I was made in July 2024",
    #FMCW 
    "what does FMCW stand for in FMCW radar",
    "FMCW stands for Frequency-Modulated Continuous Wave.",
    "how does FMCW radar differ from a continuos radar (CW)",
    "Unlike CW radar, FMCW radar can change its operating frequency during measurement.This modulation in frequency or phase allows it to perform range measurements, which CW radar cannot do due to its inability to provide accurate timing for the transmit and receive cycle",
    "What technical feature enables FMCW radar to measure the range of targets?",
    "FMCW radar can measure the range of targets by modulating the transmission signal in frequency or phase, creating a time reference for distance measurement through the frequency modulation of the transmitted signal.",
    "Why can't simple continuous wave radar devices determine target range?",
    "Simple continuous wave radar devices cannot determine target range because they lack the timing mark necessary to accurately time the transmit and receive cycle, which is needed to convert this timing into range.",
    "How does frequency modulation help in measuring the distance of stationary objects in FMCW radar?",
    "In FMCW radar, a signal is transmitted that periodically increases or decreases in frequency. When an echo signal is received, the change in frequency experiences a delay (Δt) due to the runtime shift, similar to pulse radar. The distance measurement is then based on the differences in phase or frequency between the transmitted and received signals.",
    "What is the primary difference in measurement techniques between pulse radar and FMCW radar?",
    "In pulse radar, the runtime of the signal must be measured directly to determine the range. In contrast, FMCW radar measures the differences in phase or frequency between the transmitted and received signals to determine the range.",
    "What is the purpose of modulating the transmission signal in FMCW radar?",
    "The purpose of modulating the transmission signal in FMCW radar is to create a time reference for measuring the distance of targets. This modulation enables the radar to determine the range by analyzing the frequency or phase differences between the transmitted and received signals.",
    "What is the advantage of using FMCW radar over CW radar?",
    "The advantage of using FMCW radar over CW radar is its ability to perform range measurements accurately by modulating the frequency or phase of the transmission signal, whereas CW radar cannot measure range due to the lack of timing reference.",
    "How does the echo signal in FMCW radar relate to the transmitted signal?",
    "In FMCW radar, the echo signal experiences a frequency change with a delay (Δt) due to the runtime shift. This delayed frequency change allows the radar to determine the range by comparing the phase or frequency difference between the transmitted and received signals.",
    "Can FMCW radar measure the distance of moving objects?",
    "Yes, FMCW radar can measure the distance of moving objects by analyzing the frequency shift caused by the Doppler effect, in addition to the frequency or phase modulation used for stationary objects.",
    "What are the basic features of FMCW radar?",
    "The basic features of FMCW radar are: ability to measure very small ranges to the target (the minimal measured range is comparable to the transmitted wavelength), ability to measure simultaneously the target range and its relative velocity, very high accuracy of range measurement, signal processing after mixing is performed at a low frequency range, considerably simplifying the realization of the processing circuits, and safety from the absence of the pulse radiation with a high peak power.",
    "What is one advantage of FMCW radar in terms of range measurement?",
    "FMCW radar offers very high accuracy in range measurement.",
    "How does FMCW radar simplify signal processing compared to other radar types?",
    "Signal processing in FMCW radar is performed at a low frequency range after mixing, which simplifies the design of processing circuits.",
    "What safety advantage does FMCW radar have over pulse radar?",
    "FMCW radar is safe from the absence of pulse radiation with high peak power, which reduces electromagnetic interference concerns.",
    "What range can FMCW radar measure?",
    "FMCW radar can measure very small ranges to the target, comparable to the transmitted wavelength.",
    "Besides range, what other parameter can FMCW radar measure simultaneously?",
    "FMCW radar can measure the target's relative velocity along with its range.",
    "How does the accuracy of FMCW radar compare to other radar technologies?",
    "FMCW radar boasts very high accuracy in range measurement, making it suitable for precise applications.",
    "Why is signal processing in FMCW radar advantageous?",
    "Signal processing in FMCW radar occurs at a low frequency range post-mixing, simplifying the realization of processing circuits.",
    "What technical advantage does FMCW radar offer in terms of system design?",
    "FMCW radar's operation without pulse radiation and high peak power reduces system complexity and electromagnetic interference risks.",
    "How is distance measurement achieved in FMCW radar?",
    "The distance measurement in FMCW radar is accomplished by comparing the frequency of the received signal to a reference, usually directly the transmission signal.",
    "What is a key characteristic of the transmitted waveform in FMCW radar?",
    "The duration of the transmitted waveform T in FMCW radar is substantially greater than the required receiving time for the installed distance measuring range.",
    "What is the distance formula for FMCW radar?",
    "R = c0 * Δt / 2 = c0 * Δf / (2 * df/dt), where: R is the distance between the antenna and the reflecting object (ground) in meters (m), c0 is the speed of light, approximately 3 × 10^8 meters per second (m/s), Δt is the delay time in seconds (s),Δf is the measured frequency difference in Hertz (Hz), df/dt is the frequency shift per unit of time for distance in the FMCW radar.",
    "What determines the radar resolution in FMCW radar?",
    "The radar resolution in FMCW radar is determined by the suitable choice of the frequency deviation per unit of time, which affects the bandwidth BW of the transmitted signal, similar to chirp radar.",
    "How is the maximum non-ambiguous range determined in FMCW radar?",
    "The maximum non-ambiguous range in FMCW radar is determined by the choice of the duration of the frequency increase (the longer edge of the red sawtooth in Figure 1). This duration ensures the necessary temporal overlap of the received signal with the transmitted signal.",
    "What factors can be varied to adjust the maximum frequency shift and steepness of the edge in FMCW radar?",
    "The maximum frequency shift and steepness of the edge in FMCW radar can be varied depending on the capabilities of the technology implemented circuit.",
    "How does the maximum unambiguous range relate to the energetic range in FMCW radar?",
    "The maximum unambiguous range in FMCW radar is usually much larger than the energetic range, which is limited by free space loss.",
    "What is crucial for the range resolution of an FMCW radar?",
    "The range resolution of an FMCW radar is crucially determined by the bandwidth BW of the transmitted signal, similar to chirp radar.",
    "How do technical limitations affect the resolution of FMCW radar?",
    "The resolution of FMCW radar is limited by the technical possibilities of Fast Fourier Transformation in time, constrained by the duration of the sawtooth Τ used in the radar."
   

]


list_trainer = ListTrainer(bot)
list_trainer.train(list_to_train)

@app.route("/")
def main():
    return render_template("index.html")


# while True:
#     user_response = input("users: ")
#     print("RadarBot:" +str( bot.get_response(user_response)))


@app.route("/get")
def get_chatbox_response():
    userText = request.args.get('userMessage')
    return str(bot.get_response(userText))



if __name__  == "__main__":
    app.run(debug=True)


     