"use client";

import { useState } from "react";
import { MessageCircle, Sparkles, FileText, BookOpen } from "lucide-react";
import StepByStepGuidance from "@/components/StepByStepGuidance";
import CompleteFormSection from "@/components/CompleteFormSection";
import References from "@/components/References";
import MessageHistory from "@/components/MessageHistory";
import MessageInput from "@/components/MessageInput";
import type { Message } from "@/types";

export default function ChatInterface() {
  // State for messages
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "How do I file a small claims case?",
      sender: "user",
      timestamp: new Date(Date.now() - 60000),
    },
    {
      id: 2,
      text: "I'll help you file a small claims case. To get started, I need to understand your situation better. Could you please tell me:\n\n1. What is the nature of your dispute?\n2. What is the approximate amount you're seeking?\n3. Have you attempted to resolve this matter outside of court?\n\nThis information will help me provide you with the most accurate guidance for your specific case.",
      sender: "assistant",
      timestamp: new Date(Date.now() - 30000),
    },
  ]);

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
        text: "Thank you for providing that information. Let me analyze your case and provide you with the appropriate guidance and forms.",
        sender: "assistant",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-primary-50 to-accent-50">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-primary-200 p-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary-100 rounded-lg">
            <MessageCircle className="w-6 h-6 text-primary-600" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-primary-900">
              Legal Assistant Chat
            </h1>
            <p className="text-sm text-primary-700 mt-1">
              Get personalized legal guidance and document assistance
            </p>
          </div>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col">
          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto p-6">
            <MessageHistory messages={messages} />
          </div>

          {/* Message Input */}
          <MessageInput onSendMessage={handleSendMessage} />
        </div>

        {/* Sidebar with Additional Features */}
        <div className="w-80 bg-white/60 backdrop-blur-sm border-l border-primary-200 overflow-y-auto">
          <div className="p-6 space-y-6">
            {/* Quick Actions */}
            <div>
              <h3 className="text-lg font-semibold text-primary-900 mb-4 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-primary-600" />
                Quick Actions
              </h3>
              <div className="space-y-3">
                <button className="w-full text-left p-3 bg-primary-50 hover:bg-primary-100 rounded-lg border border-primary-200 transition-colors">
                  <div className="font-medium text-primary-900">
                    File Small Claims
                  </div>
                  <div className="text-sm text-primary-700">
                    Get step-by-step guidance
                  </div>
                </button>
                <button className="w-full text-left p-3 bg-accent-50 hover:bg-accent-100 rounded-lg border border-accent-200 transition-colors">
                  <div className="font-medium text-primary-900">
                    Contract Review
                  </div>
                  <div className="text-sm text-primary-700">
                    Analyze legal documents
                  </div>
                </button>
                <button className="w-full text-left p-3 bg-primary-50 hover:bg-primary-100 rounded-lg border border-primary-200 transition-colors">
                  <div className="font-medium text-primary-900">
                    Legal Research
                  </div>
                  <div className="text-sm text-primary-700">
                    Find relevant laws & cases
                  </div>
                </button>
              </div>
            </div>

            {/* Step by Step Guidance */}
            <div>
              <h3 className="text-lg font-semibold text-primary-900 mb-4 flex items-center gap-2">
                <FileText className="w-5 h-5 text-primary-600" />
                Current Process
              </h3>
              <StepByStepGuidance />
            </div>

            {/* Complete Form Section */}
            <CompleteFormSection />

            {/* References */}
            <div>
              <h3 className="text-lg font-semibold text-primary-900 mb-4 flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-primary-600" />
                References
              </h3>
              <References />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
