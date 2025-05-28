"use client";

import type React from "react";

import { useState } from "react";
import { Send, Paperclip, Mic } from "lucide-react";

interface MessageInputProps {
  onSendMessage: (message: string) => void;
}

export default function MessageInput({ onSendMessage }: MessageInputProps) {
  const [inputValue, setInputValue] = useState("");

  const handleSendMessage = () => {
    if (inputValue.trim() === "") return;
    onSendMessage(inputValue);
    setInputValue("");
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="p-4 bg-white/80 backdrop-blur-sm border-t border-primary-200">
      <div className="flex items-end gap-3">
        {/* Attachment Button */}
        <button className="flex-shrink-0 p-2 text-primary-600 hover:text-primary-700 hover:bg-primary-50 rounded-lg transition-colors">
          <Paperclip className="w-5 h-5" />
        </button>

        {/* Message Input */}
        <div className="flex-1 relative">
          <textarea
            placeholder="Type your legal question..."
            className="w-full p-3 pr-12 bg-white border border-primary-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 resize-none min-h-[44px] max-h-32 transition-all"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            rows={1}
            style={{
              height: "auto",
              minHeight: "44px",
            }}
            onInput={(e) => {
              const target = e.target as HTMLTextAreaElement;
              target.style.height = "auto";
              target.style.height = Math.min(target.scrollHeight, 128) + "px";
            }}
          />

          {/* Send Button */}
          <button
            className={`absolute right-2 bottom-2 p-2 rounded-lg transition-all ${
              inputValue.trim()
                ? "bg-primary-600 text-white hover:bg-primary-700 shadow-sm"
                : "text-primary-400 hover:text-primary-600"
            }`}
            onClick={handleSendMessage}
            disabled={inputValue.trim() === ""}
          >
            <Send className="w-4 h-4" />
          </button>
        </div>

        {/* Voice Input Button */}
        <button className="flex-shrink-0 p-2 text-primary-600 hover:text-primary-700 hover:bg-primary-50 rounded-lg transition-colors">
          <Mic className="w-5 h-5" />
        </button>
      </div>

      {/* Helper Text */}
      <div className="mt-2 text-xs text-primary-600 flex items-center justify-between">
        <span>Press Enter to send, Shift+Enter for new line</span>
        <span className="text-primary-500">Powered by ZANGER AI</span>
      </div>
    </div>
  );
}
