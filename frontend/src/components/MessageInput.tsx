"use client"

import type React from "react"
import { useState } from "react"
import { Send } from "lucide-react"

interface MessageInputProps {
  onSendMessage: (message: string) => void
}

const MessageInput: React.FC<MessageInputProps> = ({ onSendMessage }) => {
  const [inputValue, setInputValue] = useState("")

  const handleSendMessage = () => {
    if (inputValue.trim() === "") return
    onSendMessage(inputValue)
    setInputValue("")
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSendMessage()
    }
  }

  return (
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
  )
}

export default MessageInput
