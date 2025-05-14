"use client";

import { useState } from "react";
import StepByStepGuidance from "./components/StepByStepGuidance";
import CompleteFormSection from "./components/CompleteFormSection";
import References from "./components/References";
import MessageHistory from "./components/MessageHistory";
import MessageInput from "./components/MessageInput";
import Templates from "./pages/Templates";
import type { Message } from "./components/ChatMessage";

function App() {
  // State for messages and current page
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "How do I file a small claims case?",
      sender: "user",
      timestamp: new Date(Date.now() - 60000),
    },
  ]);
  const [currentPage, setCurrentPage] = useState<"chat" | "templates">("chat");

  // Handle sending a new message
  const handleSendMessage = (text: string) => {
    // Add user message
    const newMessage: Message = {
      id: Date.now(),
      text,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages([...messages, newMessage]);

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

  return (
    <div className="min-h-screen bg-gray-50">
      {currentPage === "chat" ? (
        <div className="max-w-3xl mx-auto border rounded-lg shadow-sm my-8 bg-white">
          {/* Header with navigation */}
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
            <div className="flex gap-4">
              <button
                className="bg-white text-black border hover:bg-gray-100 rounded-full px-4 py-2"
                onClick={() => setCurrentPage("templates")}
              >
                Templates
              </button>
              <button className="bg-white text-black border hover:bg-gray-100 rounded-full px-6 py-2">
                Create document
              </button>
            </div>
          </div>

          {/* Main Content */}
          <div className="p-6 overflow-y-auto max-h-[calc(100vh-200px)]">
            {/* Step by Step Guidance */}
            <StepByStepGuidance />

            {/* Complete Form Section */}
            <CompleteFormSection />

            {/* References */}
            <References />

            {/* Message History - Now after References */}
            <MessageHistory messages={messages} />
          </div>

          {/* Message Input */}
          <MessageInput onSendMessage={handleSendMessage} />
        </div>
      ) : (
        <Templates />
      )}
    </div>
  );
}

export default App;
