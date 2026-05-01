import { useState, useRef, useEffect } from 'react';
import { sendMessage } from './services/api';
import ReactMarkdown from 'react-markdown';

const LANGUAGES = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'es', name: 'Español', flag: '🇪🇸' },
  { code: 'hi', name: 'हिन्दी', flag: '🇮🇳' },
  { code: 'zh', name: '中文', flag: '🇨🇳' },
];

const QUICK_PROMPTS = [
  "🗳️ How do I register to vote?",
  "📋 Steps in a general election",
  "🏛️ Explain the Electoral College",
  "📅 Key election deadlines",
];

export default function App() {
  const [input, setInput] = useState('');
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState('en');
  const [image, setImage] = useState(null);
  const sessionId = useRef(`session_${Date.now()}`).current;
  const bottomRef = useRef(null);
  const inputRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chat, loading]);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64String = reader.result.split(',')[1];
        setImage({ file, preview: URL.createObjectURL(file), base64: base64String });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSend = async (promptText) => {
    const msg = promptText || input;
    if (!msg.trim() && !image) return;

    const userMsg = msg.trim() || "Please analyze this document.";

    setChat(prev => [...prev, {
      role: 'user',
      content: userMsg,
      imagePreview: image?.preview
    }]);

    const currentBase64 = image?.base64;
    setInput('');
    setImage(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
    setLoading(true);

    try {
      const cleanMsg = userMsg.replace(/^[\u{1F000}-\u{1FFFF}]\s*/u, '');
      const res = await sendMessage(cleanMsg, sessionId, language, currentBase64);
      setChat(prev => [...prev, { role: 'bot', content: res.reply }]);
    } catch (error) {
      setChat(prev => [...prev, { role: 'error', content: 'Unable to connect. Make sure the backend server is running.' }]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    handleSend();
  };

  const currentLang = LANGUAGES.find(l => l.code === language);

  return (
    <div className="app-shell" role="main" aria-label="Election Assistant Interface">
      {/* Header */}
      <header className="app-header">
        <div className="header-top">
          <div className="logo-row">
            <span className="logo-icon">🗳️</span>
            <h1 tabIndex="0">Election Education Assistant</h1>
          </div>
          <div className="lang-select-wrap">
            <span className="lang-flag">{currentLang?.flag}</span>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="lang-select"
              aria-label="Select language"
            >
              {LANGUAGES.map(lang => (
                <option key={lang.code} value={lang.code}>{lang.flag} {lang.name}</option>
              ))}
            </select>
          </div>
        </div>
        <p className="subtitle">Your impartial guide to understanding democracy</p>
        <div className="header-divider" />
      </header>

      {/* Chat area */}
      <div className="chat-scroll" role="log" aria-live="polite" aria-label="Chat History">
        {chat.length === 0 && !loading && (
          <div className="welcome">
            <div className="welcome-emoji">🏛️</div>
            <h2>Welcome, Citizen!</h2>
            <p>I can help you understand elections, voting procedures, and how democracy works. Upload documents for analysis or switch languages for multilingual support.</p>
            <div className="quick-chips">
              {QUICK_PROMPTS.map((prompt, i) => (
                <button
                  key={i}
                  className="quick-chip"
                  onClick={() => handleSend(prompt)}
                  disabled={loading}
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        )}

        {chat.map((msg, i) => (
          <div key={i} className={`msg-row ${msg.role}`}>
            <div className={`msg-avatar ${msg.role === 'user' ? 'user-av' : 'bot-av'}`}>
              {msg.role === 'user' ? '👤' : msg.role === 'error' ? '⚠️' : '🤖'}
            </div>
            <div className={`msg-bubble ${msg.role}-bub`}>
              <span className="sr-only">{msg.role === 'user' ? 'You said: ' : 'Assistant said: '}</span>
              {msg.imagePreview && (
                <img src={msg.imagePreview} alt="Uploaded document" className="msg-image" />
              )}
              {msg.role === 'user' ? (
                msg.content
              ) : (
                <div className="markdown-body">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="typing-row" aria-live="assertive">
            <div className="msg-avatar bot-av">🤖</div>
            <div className="typing-bubble">
              <div className="dot" />
              <div className="dot" />
              <div className="dot" />
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="input-bar">
        {chat.length > 0 && (
          <div className="prompts-row">
            {QUICK_PROMPTS.map((prompt, i) => (
              <button
                key={i}
                className="quick-chip"
                onClick={() => handleSend(prompt)}
                disabled={loading}
              >
                {prompt}
              </button>
            ))}
          </div>
        )}

        {/* Image preview */}
        {image && (
          <div className="image-preview-bar">
            <img src={image.preview} alt="Preview" className="image-thumbnail" />
            <span className="image-name">📎 {image.file.name}</span>
            <button className="image-remove" onClick={() => { setImage(null); if (fileInputRef.current) fileInputRef.current.value = ''; }}>✕</button>
          </div>
        )}

        <form onSubmit={handleSubmit} className="input-glass" aria-label="Message input form">
          <input
            type="file"
            accept="image/*"
            ref={fileInputRef}
            onChange={handleImageUpload}
            className="hidden-file"
          />
          <button
            type="button"
            className="btn-upload"
            onClick={() => fileInputRef.current?.click()}
            title="Upload document image"
            aria-label="Upload document image"
          >
            📷
          </button>
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about elections or upload a document..."
            aria-label="Type your message here"
            disabled={loading}
          />
          <button
            type="submit"
            className="btn-send"
            aria-label="Send message"
            disabled={loading || (!input.trim() && !image)}
          >
            ➤
          </button>
        </form>
      </div>
    </div>
  );
}
