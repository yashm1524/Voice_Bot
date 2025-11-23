import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, Play, Pause, BarChart2, User, Bot, Send } from 'lucide-react';
import axios from 'axios';
import { motion } from 'framer-motion';
import AudioRecorderPolyfill from 'audio-recorder-polyfill';

// Polyfill setup with safety check
try {
  window.MediaRecorder = AudioRecorderPolyfill;
} catch (e) {
  console.warn("Polyfill error (safe to ignore in modern browsers):", e);
}

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const API_URL = `${BASE_URL}/api/process-audio`;
const TEXT_API_URL = `${BASE_URL}/api/process-text`;

function App() {
  const [messages, setMessages] = useState([
    { role: 'bot', text: "Hello! I'm your intelligent voice assistant. How can I help you today?", audioUrl: null }
  ]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showDashboard, setShowDashboard] = useState(false);
  const [metrics, setMetrics] = useState({ queries: 0, avgResponseTime: 0 });
  const [isRecording, setIsRecording] = useState(false);
  const [inputText, setInputText] = useState("");
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (showDashboard) {
      axios.get('http://localhost:8000/api/stats')
        .then(res => setMetrics(res.data))
        .catch(err => console.error("Error fetching stats:", err));
    }
  }, [showDashboard]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream, { mimeType: 'audio/wav' });
      chunksRef.current = [];

      mediaRecorderRef.current.addEventListener('dataavailable', event => {
        if (event.data.size > 0) chunksRef.current.push(event.data);
      });

      mediaRecorderRef.current.addEventListener('stop', () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/wav' });
        handleStop(blob);
        stream.getTracks().forEach(track => track.stop());
      });

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Microphone error:", err);
      alert("Could not access microphone. Please allow permissions.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleStop = async (blob) => {
    setIsProcessing(true);
    const file = new File([blob], "recording.wav", { type: "audio/wav" });
    const formData = new FormData();
    formData.append("file", file);

    const startTime = Date.now();

    try {
      const response = await axios.post(API_URL, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      const { user_text, bot_response, audio_url } = response.data;
      const endTime = Date.now();

      updateMetrics(startTime, endTime);
      addMessage('user', user_text);
      addMessage('bot', bot_response, audio_url);

      if (audio_url) playAudio(audio_url);

    } catch (error) {
      handleError(error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleTextSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim() || isProcessing) return;

    const text = inputText;
    setInputText("");
    setIsProcessing(true);
    addMessage('user', text);

    const startTime = Date.now();

    try {
      const response = await axios.post(TEXT_API_URL, { text });
      const { bot_response, audio_url } = response.data;
      const endTime = Date.now();

      updateMetrics(startTime, endTime);
      addMessage('bot', bot_response, audio_url);

      if (audio_url) playAudio(audio_url);

    } catch (error) {
      handleError(error);
    } finally {
      setIsProcessing(false);
    }
  };

  const updateMetrics = (startTime, endTime) => {
    setMetrics(prev => ({
      queries: prev.queries + 1,
      avgResponseTime: Math.round(((prev.avgResponseTime * prev.queries) + (endTime - startTime)) / (prev.queries + 1))
    }));
  };

  const addMessage = (role, text, audioUrl = null) => {
    setMessages(prev => [
      ...prev,
      { role, text, audioUrl: audioUrl ? `${BASE_URL}${audioUrl}` : null }
    ]);
  };

  const playAudio = (url) => {
    new Audio(`${BASE_URL}${url}`).play().catch(e => console.log("Audio play error:", e));
  };

  const handleError = (error) => {
    console.error("Backend error:", error);
    let msg = "Sorry, I encountered an error connecting to the backend.";
    if (error.code === "ERR_NETWORK") msg = "Network error: Is the backend running on port 8000?";
    addMessage('bot', msg);
  };

  return (
    <div className="min-h-screen bg-dark text-white flex flex-col font-sans h-full w-full">
      <header className="p-4 border-b border-surface flex justify-between items-center bg-dark/50 backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-br from-primary to-secondary rounded-full flex items-center justify-center">
            <Bot size={20} className="text-white" />
          </div>
          <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
            VoiceBot AI
          </h1>
        </div>
        <button
          onClick={() => setShowDashboard(!showDashboard)}
          className="p-2 hover:bg-surface rounded-full transition-colors"
          title="Analytics Dashboard"
        >
          <BarChart2 size={20} className={showDashboard ? "text-primary" : "text-gray-400"} />
        </button>
      </header>

      <main className="flex-1 flex flex-col max-w-3xl w-full mx-auto p-4 relative h-full">
        {showDashboard ? (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h2 className="text-2xl font-bold">Analytics Dashboard</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-surface p-6 rounded-2xl border border-white/5">
                <h3 className="text-gray-400 text-sm mb-2">Total Queries</h3>
                <p className="text-4xl font-bold text-white">{metrics.queries}</p>
              </div>
              <div className="bg-surface p-6 rounded-2xl border border-white/5">
                <h3 className="text-gray-400 text-sm mb-2">Avg Response Time</h3>
                <p className="text-4xl font-bold text-white">{metrics.avgResponseTime}ms</p>
              </div>
            </div>
          </div>
        ) : (
          <>
            <div className="flex-1 overflow-y-auto space-y-6 pb-32 min-h-0">
              {messages.map((msg, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                >
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-surface' : 'bg-primary'}`}>
                    {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                  </div>
                  <div className={`max-w-[80%] p-4 rounded-2xl ${msg.role === 'user' ? 'bg-surface rounded-tr-none' : 'bg-gradient-to-br from-primary/20 to-secondary/20 border border-primary/20 rounded-tl-none'}`}>
                    <p className="leading-relaxed">{msg.text}</p>
                    {msg.audioUrl && (
                      <button onClick={() => new Audio(msg.audioUrl).play()} className="mt-2 text-sm text-blue-300 flex items-center gap-2">
                        <Play size={14} /> Play Audio
                      </button>
                    )}
                  </div>
                </motion.div>
              ))}
              {isProcessing && (
                <div className="flex gap-4">
                  <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center shrink-0">
                    <Bot size={16} />
                  </div>
                  <div className="bg-surface/50 p-4 rounded-2xl rounded-tl-none flex items-center gap-2">
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-100" />
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-200" />
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>

            <div className="fixed bottom-8 left-0 right-0 flex justify-center px-4 pointer-events-none">
              <div className="bg-surface/80 backdrop-blur-lg border border-white/10 p-2 rounded-full shadow-2xl flex items-center gap-4 pl-4 pr-2 pointer-events-auto w-full max-w-2xl">

                <form onSubmit={handleTextSubmit} className="flex-1 flex items-center gap-2">
                  <input
                    type="text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder={isRecording ? "Listening..." : "Type a message..."}
                    disabled={isRecording || isProcessing}
                    className="flex-1 bg-transparent border-none outline-none text-white placeholder-gray-400 h-full py-3"
                  />
                  <button
                    type="submit"
                    disabled={!inputText.trim() || isProcessing || isRecording}
                    className="p-2 text-primary hover:text-white disabled:opacity-50 transition-colors"
                  >
                    <Send size={20} />
                  </button>
                </form>

                <div className="h-8 w-[1px] bg-white/10 mx-2"></div>

                <button
                  onClick={isRecording ? stopRecording : startRecording}
                  className={`w-10 h-10 rounded-full flex items-center justify-center transition-all duration-300 ${isRecording
                    ? 'bg-red-500 shadow-[0_0_20px_rgba(239,68,68,0.5)] scale-110'
                    : 'bg-primary hover:bg-primary/90'
                    }`}
                >
                  {isRecording ? <Square size={18} fill="currentColor" /> : <Mic size={20} />}
                </button>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
