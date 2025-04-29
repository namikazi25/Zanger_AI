import Link from "next/link"
import { MessageSquare, FileText } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function Home() {
  return (
    <div className="max-w-3xl mx-auto border rounded-lg shadow-sm my-8">
      {/* Header */}
      <div className="flex justify-between items-center p-4 border-b">
        <div className="flex items-center gap-2">
          <div className="relative w-10 h-10">
            <svg viewBox="0 0 24 24" className="w-full h-full" fill="currentColor">
              <path d="M12 2L6 5v3c0 0.4 0.2 0.7 0.5 0.9L12 12l-5.5 3.1C6.2 15.3 6 15.6 6 16v3l6 3 6-3v-3c0-0.4-0.2-0.7-0.5-0.9L12 12l5.5-3.1c0.3-0.2 0.5-0.5 0.5-0.9V5l-6-3zm0 2.2L15.7 6 12 7.8 8.3 6 12 4.2zm-5 3.5l5 2.8v5l-5-2.8v-5zm10 0v5l-5 2.8v-5l5-2.8z" />
            </svg>
          </div>
          <h1 className="text-2xl font-bold tracking-wider">ZANGER</h1>
        </div>
        <Button className="bg-white text-black border hover:bg-gray-100 rounded-full px-6">Create document</Button>
      </div>

      {/* Main Content */}
      <div className="p-6">
        {/* Search Query */}
        <div className="bg-gray-100 rounded-full py-3 px-6 mb-8 inline-block">
          <p className="text-lg">How do I file a small claims case?</p>
        </div>

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
              <Link href="#" className="text-blue-600 hover:underline">
                Money Claim Online
              </Link>{" "}
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
          <p className="pl-12 mb-4 text-lg">Includes filing instructions & deadlines</p>

          <div className="pl-12 flex gap-4">
            <Button className="bg-white text-black border hover:bg-gray-100 rounded-full px-6 py-5 text-lg">
              Complete Form N1
            </Button>
            <Button className="bg-white text-black border hover:bg-gray-100 rounded-full px-6 py-5 text-lg">
              Request lawyer assistance
            </Button>
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
      </div>

      {/* Message Input */}
      <div className="p-4 border-t">
        <input
          type="text"
          placeholder="Type a message..."
          className="w-full p-4 rounded-full border focus:outline-none focus:ring-2 focus:ring-gray-200"
        />
      </div>
    </div>
  )
}
