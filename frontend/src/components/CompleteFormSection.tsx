import type React from "react"
import { FileText } from "lucide-react"

const CompleteFormSection: React.FC = () => {
  return (
    <div className="mb-8">
      <div className="flex items-start gap-3 mb-4">
        <FileText className="mt-1 w-6 h-6" />
        <h2 className="text-2xl font-bold">Complete Form N1</h2>
      </div>
      <p className="pl-12 mb-4 text-lg">Includes filing instructions & deadlines</p>

      <div className="pl-12 flex gap-4">
        <button className="bg-white text-black border hover:bg-gray-100 rounded-full px-6 py-5 text-lg">
          Complete Form N1
        </button>
        <button className="bg-white text-black border hover:bg-gray-100 rounded-full px-6 py-5 text-lg">
          Request lawyer assistance
        </button>
      </div>
    </div>
  )
}

export default CompleteFormSection
