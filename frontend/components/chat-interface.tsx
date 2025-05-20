"use client"

import { useState } from "react"
import StepByStepGuidance from "@/components/StepByStepGuidance"
import CompleteFormSection from "@/components/CompleteFormSection"
import References from "@/components/References"
import MessageHistory from "@/components/MessageHistory"
import MessageInput from "@/components/MessageInput"
import type { Message } from "@/types"

export default function ChatInterface() {
  // State for messages
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "How do I file a small claims case?",
      sender: "user",
      timestamp: new Date(Date.now() - 60000),
    },
  ])

  // Handle sending a new message
  const handleSendMessage = (text: string) => {
    // Add user message
    const newMessage: Message = {
      id: Date.now(),
      text,
      sender: "user",
      timestamp: new Date(),
    }

    setMessages([...messages, newMessage])

    // Simulate assistant response (in a real app, this would be an API call)
    setTimeout(() => {
      const assistantMessage: Message = {
        id: Date.now() + 1,
        text: "I'll help you with that. Please provide more details about your case.",
        sender: "assistant",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, assistantMessage])
    }, 1000)
  }

  return (
    <div className="border rounded-lg shadow-sm bg-white">
      {/* Main Content */}
      <div className="p-6 overflow-y-auto max-h-[calc(100vh-300px)]">
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
  )
}
