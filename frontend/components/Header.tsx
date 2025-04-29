import type React from "react"

const Header: React.FC = () => {
  return (
    <div className="flex justify-between items-center p-4 border-b">
      <div className="flex items-center gap-2">
        <div className="relative w-10 h-10">
          <svg viewBox="0 0 24 24" className="w-full h-full" fill="currentColor">
            <path d="M12 2L6 5v3c0 0.4 0.2 0.7 0.5 0.9L12 12l-5.5 3.1C6.2 15.3 6 15.6 6 16v3l6 3 6-3v-3c0-0.4-0.2-0.7-0.5-0.9L12 12l5.5-3.1c0.3-0.2 0.5-0.5 0.5-0.9V5l-6-3zm0 2.2L15.7 6 12 7.8 8.3 6 12 4.2zm-5 3.5l5 2.8v5l-5-2.8v-5zm10 0v5l-5 2.8v-5l5-2.8z" />
          </svg>
        </div>
        <h1 className="text-2xl font-bold tracking-wider">ZANGER</h1>
      </div>
      <button className="bg-white text-black border hover:bg-gray-100 rounded-full px-6 py-2">Create document</button>
    </div>
  )
}

export default Header
