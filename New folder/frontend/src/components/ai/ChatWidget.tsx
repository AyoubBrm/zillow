import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, Sparkles, Bot, User } from 'lucide-react';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const suggestedQuestions = [
  'How much did I spend on software?',
  'What are my biggest expenses?',
  'Show my revenue trend',
  'Any unusual transactions?',
];

const aiResponses: Record<string, string> = {
  software: "Based on your transactions, you've spent **$4,847** on Software & SaaS subscriptions this quarter. Your top software expenses are:\n\n• Adobe Creative Cloud: $599/yr\n• Slack: $162/mo\n• Google Workspace: $144/mo\n• Figma: $75/mo\n• Notion: $40/mo\n\nThis is **12% lower** than last quarter. 📉",
  expenses: "Your **top 5 expense categories** this quarter:\n\n1. 💰 Payroll — $52,000 (33.2%)\n2. 📢 Marketing — $22,400 (14.3%)\n3. ☁️ Cloud & Hosting — $18,500 (11.8%)\n4. 🏢 Office & Rent — $16,500 (10.5%)\n5. ✈️ Travel — $14,200 (9.1%)\n\nPayroll remains your largest expense. Consider reviewing your marketing spend — it increased 18% from last quarter.",
  revenue: "Your revenue has been on a **strong upward trend** 📈\n\n• Last 3 months average: **$31,367/mo**\n• Previous 3 months average: $25,167/mo\n• **Growth rate: +24.6%**\n\nJune 2026 was your best month yet at $33,500. Your top clients (Acme Corp, Stark Industries, Wayne Enterprises) account for 68% of revenue.",
  unusual: "I found **3 potentially unusual transactions** 🔍:\n\n1. **Delta Airlines** — $2,847 on May 15 (3x your typical travel expense)\n2. **Office Depot** — $1,234 on Apr 22 (first purchase in 4 months)\n3. **Unknown vendor** — $567 on Mar 8 (needs categorization)\n\nWould you like me to help categorize or flag any of these?",
  default: "I can help you with financial insights! Try asking me about:\n\n• Your spending in specific categories\n• Revenue trends and projections\n• Unusual or large transactions\n• Budget recommendations\n• Tax preparation tips\n\nWhat would you like to know? 💡",
};

function getAiResponse(message: string): string {
  const lower = message.toLowerCase();
  if (lower.includes('software') || lower.includes('saas') || lower.includes('subscription')) return aiResponses.software;
  if (lower.includes('expense') || lower.includes('spend') || lower.includes('biggest')) return aiResponses.expenses;
  if (lower.includes('revenue') || lower.includes('income') || lower.includes('trend') || lower.includes('earning')) return aiResponses.revenue;
  if (lower.includes('unusual') || lower.includes('anomal') || lower.includes('suspicious') || lower.includes('flag')) return aiResponses.unusual;
  return aiResponses.default;
}

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: "Hi! I'm your AI financial assistant. I can help you understand your finances, find transactions, and provide insights. What would you like to know?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (isOpen) inputRef.current?.focus();
  }, [isOpen]);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMsg: ChatMessage = {
      id: `msg-${Date.now()}`,
      role: 'user',
      content: text.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    // Simulate AI thinking
    await new Promise((resolve) => setTimeout(resolve, 1000 + Math.random() * 1000));

    const aiMsg: ChatMessage = {
      id: `msg-${Date.now()}-ai`,
      role: 'assistant',
      content: getAiResponse(text),
      timestamp: new Date(),
    };

    setIsTyping(false);
    setMessages((prev) => [...prev, aiMsg]);
  };

  return (
    <>
      {/* Chat Panel */}
      {isOpen && (
        <div
          className="fixed bottom-20 right-4 sm:right-6 z-50 w-[380px] max-w-[calc(100vw-32px)] h-[520px] bg-slate-900/95 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl shadow-black/50 flex flex-col animate-scaleIn origin-bottom-right"
          id="chat-panel"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-white/5">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="text-sm font-semibold text-white">AI Assistant</h3>
                <p className="text-xs text-emerald-400 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full" />
                  Online
                </p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors"
              id="chat-close-btn"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex gap-2.5 ${msg.role === 'user' ? 'flex-row-reverse' : ''} animate-slideUp`}
              >
                <div
                  className={`w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0 ${
                    msg.role === 'assistant'
                      ? 'bg-gradient-to-br from-violet-500/20 to-indigo-500/20 border border-violet-500/20'
                      : 'bg-slate-700'
                  }`}
                >
                  {msg.role === 'assistant' ? (
                    <Bot className="w-4 h-4 text-violet-400" />
                  ) : (
                    <User className="w-4 h-4 text-slate-300" />
                  )}
                </div>
                <div
                  className={`max-w-[80%] rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed ${
                    msg.role === 'assistant'
                      ? 'bg-slate-800/50 text-slate-200 rounded-tl-md'
                      : 'bg-gradient-to-r from-violet-600 to-indigo-600 text-white rounded-tr-md'
                  }`}
                >
                  <div className="whitespace-pre-wrap">{msg.content}</div>
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="flex gap-2.5 animate-slideUp">
                <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-violet-500/20 to-indigo-500/20 border border-violet-500/20 flex items-center justify-center flex-shrink-0">
                  <Bot className="w-4 h-4 text-violet-400" />
                </div>
                <div className="bg-slate-800/50 rounded-2xl rounded-tl-md px-4 py-3">
                  <div className="flex gap-1.5">
                    <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Suggested questions */}
          {messages.length <= 1 && (
            <div className="px-4 pb-2 flex flex-wrap gap-1.5">
              {suggestedQuestions.map((q) => (
                <button
                  key={q}
                  onClick={() => sendMessage(q)}
                  className="text-xs px-3 py-1.5 rounded-full bg-violet-500/10 text-violet-400 border border-violet-500/20 hover:bg-violet-500/20 transition-colors"
                >
                  {q}
                </button>
              ))}
            </div>
          )}

          {/* Input */}
          <div className="p-3 border-t border-white/5">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                sendMessage(input);
              }}
              className="flex items-center gap-2"
            >
              <input
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about your finances..."
                className="flex-1 bg-slate-800/50 border border-slate-700/30 rounded-xl px-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-violet-500/40 focus:ring-1 focus:ring-violet-500/20 transition-all"
                id="chat-input"
              />
              <button
                type="submit"
                disabled={!input.trim()}
                className="p-2.5 rounded-xl bg-gradient-to-r from-violet-600 to-indigo-600 text-white hover:from-violet-500 hover:to-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-lg shadow-violet-500/20"
                id="chat-send-btn"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`
          fixed bottom-4 right-4 sm:right-6 z-50
          w-14 h-14 rounded-2xl
          bg-gradient-to-r from-violet-600 to-indigo-600
          text-white shadow-xl shadow-violet-500/30
          flex items-center justify-center
          hover:from-violet-500 hover:to-indigo-500
          hover:shadow-violet-500/50 hover:scale-105
          active:scale-95
          transition-all duration-200
          ${!isOpen ? 'animate-pulse-glow' : ''}
        `}
        id="chat-toggle-btn"
      >
        {isOpen ? <X className="w-6 h-6" /> : <MessageCircle className="w-6 h-6" />}
      </button>
    </>
  );
};

export default ChatWidget;
