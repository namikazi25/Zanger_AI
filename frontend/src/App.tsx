"use client";

import type React from "react";

import { useState } from "react";
import { MessageSquare, FileText, Send } from "lucide-react";

// Define message type
type Message = {
  id: number;
  text: string;
  sender: "user" | "assistant";
  timestamp: Date;
};

function App() {
  // State for messages and current input
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "How do I file a small claims case?",
      sender: "user",
      timestamp: new Date(Date.now() - 60000),
    },
  ]);
  const [inputValue, setInputValue] = useState("");

  // Handle sending a new message
  const handleSendMessage = () => {
    if (inputValue.trim() === "") return;

    // Add user message
    const newMessage: Message = {
      id: Date.now(),
      text: inputValue,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages([...messages, newMessage]);
    setInputValue("");

    // Simulate assistant response (in a real app, this would be an API call)
    setTimeout(() => {
      const assistantMessage: Message = {
        id: Date.now() + 1,
        text: "I'll help you with that. Please provide more details about your case.",
        sender: "assistant",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    }, 1000);
  };

  // Handle key press (Enter to send)
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSendMessage();
    }
  };

  return (
    <div className="max-w-3xl mx-auto border rounded-lg shadow-sm my-8">
      {/* Header */}
      <div className="flex justify-between items-center p-4 border-b">
        <div className="flex items-center gap-2">
          <div className="relative w-10 h-10">
            <svg
              viewBox="0 0 24 24"
              className="w-full h-full"
              fill="currentColor"
            >
              <path d="M12 2L6 5v3c0 0.4 0.2 0.7 0.5 0.9L12 12l-5.5 3.1C6.2 15.3 6 15.6 6 16v3l6 3 6-3v-3c0-0.4-0.2-0.7-0.5-0.9L12 12l5.5-3.1c0.3-0.2 0.5-0.5 0.5-0.9V5l-6-3zm0 2.2L15.7 6 12 7.8 8.3 6 12 4.2zm-5 3.5l5 2.8v5l-5-2.8v-5zm10 0v5l-5 2.8v-5l5-2.8z" />
            </svg>
          </div>
          <h1 className="text-2xl font-bold tracking-wider">ZANGER</h1>
        </div>
        <button className="bg-white text-black border hover:bg-gray-100 rounded-full px-6 py-2">
          Create document
        </button>
      </div>

      {/* Chat Messages */}
      <div className="p-6 overflow-y-auto max-h-[calc(100vh-200px)]">
        {/* Step by Step Guidance */}
        <div className="mb-8">
          <div className="flex items-start gap-3 mb-4">
            <MessageSquare className="mt-1 w-6 h-6" />
            <h2 className="text-2xl font-bold">Step-by-step guidance</h2>
          </div>

          <ul className="list-disc pl-12 space-y-3 text-lg">
            <li>Identify the claim type and amount</li>
            <li>Try resolving the issue directly</li>
            <li>Prepare your evidence</li>
            <li>
              Complete online via{" "}
              <a href="#" className="text-blue-600 hover:underline">
                Money Claim Online
              </a>{" "}
              or by post
            </li>
            <li>Pay the court fee</li>
          </ul>
        </div>

        {/* Complete Form Section */}
        <div className="mb-8">
          <div className="flex items-start gap-3 mb-4">
            <FileText className="mt-1 w-6 h-6" />
            <h2 className="text-2xl font-bold">Complete Form N1</h2>
          </div>
          <p className="pl-12 mb-4 text-lg">
            Includes filing instructions & deadlines
          </p>

          <div className="pl-12 flex gap-4">
            <button className="bg-white text-black border hover:bg-gray-100 rounded-full px-6 py-5 text-lg">
              Complete Form N1
            </button>
            <button className="bg-white text-black border hover:bg-gray-100 rounded-full px-6 py-5 text-lg">
              Request lawyer assistance
            </button>
          </div>
        </div>

        {/* References */}
        <div className="mb-8 pl-12">
          <h3 className="text-xl font-bold mb-3">References:</h3>
          <ul className="list-disc pl-6 space-y-2 text-lg">
            <li>GOV.UK Small Claims Guidance</li>
            <li>Civil Procedure Rules Part 27</li>
          </ul>
        </div>

        {/* Message History */}
        <div className="space-y-4 mb-6">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`${
                  message.sender === "user"
                    ? "bg-gray-100 rounded-full py-3 px-6 inline-block"
                    : "bg-white border rounded-lg p-4 max-w-[80%]"
                }`}
              >
                <p className="text-lg">{message.text}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Message Input */}
      <div className="p-4 border-t">
        <div className="relative">
          <input
            type="text"
            placeholder="Type a message..."
            className="w-full p-4 pr-12 rounded-full border focus:outline-none focus:ring-2 focus:ring-gray-200"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <button
            className="absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-full hover:bg-gray-100"
            onClick={handleSendMessage}
            disabled={inputValue.trim() === ""}
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
