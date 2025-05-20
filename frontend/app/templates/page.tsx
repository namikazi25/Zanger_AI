"use client"

import { useState } from "react"
import Link from "next/link"
import Image from "next/image"
import { File, Edit, Eye, Plus, Search, X } from "lucide-react"
import EditTemplateModal from "@/components/EditTemplateModal"
import type { Template, TemplateCategory } from "@/types"

// Sample data
const initialCategories: TemplateCategory[] = [
  {
    id: "copyright-commission",
    name: "Copyright and Commission Templates",
    templates: [
      {
        id: "copyright-assignment",
        title: "Copyright Assignment",
        status: "active",
        description: "Non-disclosure agreement for Client A covering project details and proprietary information.",
      },
      {
        id: "commission-agreement",
        title: "Commission Agreement",
        status: "active",
        description: "Non-disclosure agreement for Vendor B covering service specifications and trade secrets.",
      },
    ],
  },
  {
    id: "consultancy",
    name: "Consultancy Agreement",
    templates: [
      {
        id: "consultancy-standard",
        title: "Standard Consultancy",
        status: "active",
        description: "Standard consultancy agreement for professional services.",
      },
    ],
  },
  {
    id: "consultancy-terms",
    name: "Consultancy Terms",
    templates: [
      {
        id: "terms-conditions",
        title: "Terms & Conditions",
        status: "draft",
        description: "Standard terms and conditions for consultancy services.",
      },
    ],
  },
  {
    id: "distribution",
    name: "Distribution Agreement",
    templates: [
      {
        id: "distribution-standard",
        title: "Distribution Standard",
        status: "active",
        description: "Standard distribution agreement for product distribution.",
      },
    ],
  },
  {
    id: "foreign-nda",
    name: "Foreign and NDA",
    templates: [
      {
        id: "nda-standard",
        title: "Standard NDA",
        status: "active",
        description: "Standard non-disclosure agreement for international clients.",
      },
    ],
  },
]

export default function TemplatesPage() {
  const [categories, setCategories] = useState<TemplateCategory[]>(initialCategories)
  const [selectedCategory, setSelectedCategory] = useState<string>(categories[0].id)
  const [searchQuery, setSearchQuery] = useState<string>("")
  const [editingTemplate, setEditingTemplate] = useState<Template | null>(null)
  const [isEditModalOpen, setIsEditModalOpen] = useState(false)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)

  // Get the selected category
  const currentCategory = categories.find((cat) => cat.id === selectedCategory) || categories[0]

  // Filter templates based on search query
  const filteredTemplates = currentCategory.templates.filter(
    (template) =>
      template.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      template.description.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  // Handle opening the edit modal
  const handleEditClick = (template: Template) => {
    setEditingTemplate(template)
    setIsEditModalOpen(true)
  }

  // Handle saving template changes
  const handleSaveTemplate = (updatedTemplate: Template) => {
    // Update the template in the categories state
    const updatedCategories = categories.map((category) => {
      if (category.id === selectedCategory) {
        return {
          ...category,
          templates: category.templates.map((template) =>
            template.id === updatedTemplate.id ? updatedTemplate : template,
          ),
        }
      }
      return category
    })

    setCategories(updatedCategories)
    setSuccessMessage(`Template "${updatedTemplate.title}" updated successfully`)

    // Clear success message after 3 seconds
    setTimeout(() => {
      setSuccessMessage(null)
    }, 3000)
  }

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <header className="bg-white border-b px-6 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="relative w-8 h-8">
              <svg viewBox="0 0 24 24" className="w-full h-full" fill="currentColor">
                <path d="M12 2L6 5v3c0 0.4 0.2 0.7 0.5 0.9L12 12l-5.5 3.1C6.2 15.3 6 15.6 6 16v3l6 3 6-3v-3c0-0.4-0.2-0.7-0.5-0.9L12 12l5.5-3.1c0.3-0.2 0.5-0.5 0.5-0.9V5l-6-3zm0 2.2L15.7 6 12 7.8 8.3 6 12 4.2zm-5 3.5l5 2.8v5l-5-2.8v-5zm10 0v5l-5 2.8v-5l5-2.8z" />
              </svg>
            </div>
            <h1 className="text-xl font-bold tracking-wider">ZANGER</h1>
          </div>

          <nav className="hidden md:flex items-center space-x-6">
            <Link href="/" className="text-gray-500 hover:text-gray-900">
              Home
            </Link>
            <Link href="#" className="text-gray-500 hover:text-gray-900">
              My Notes
            </Link>
            <Link href="#" className="text-gray-500 hover:text-gray-900">
              Clients
            </Link>
            <Link href="/templates" className="text-gray-900 font-medium">
              Templates
            </Link>
            <Link href="#" className="text-gray-500 hover:text-gray-900">
              Calendar
            </Link>
          </nav>

          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden">
              <Image src="/abstract-profile.png" alt="User" width={32} height={32} className="object-cover" />
            </div>
            <span className="hidden md:inline text-sm font-medium">Alan Gioielli</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar */}
        <div className="w-64 border-r bg-gray-50 overflow-y-auto">
          <div className="p-4">
            <h2 className="text-2xl font-bold mb-4">Templates</h2>

            <div className="space-y-1">
              {categories.map((category) => (
                <button
                  key={category.id}
                  className={`flex items-center gap-2 w-full text-left px-3 py-2 rounded-lg transition-colors ${
                    selectedCategory === category.id ? "bg-gray-200 text-gray-900" : "text-gray-700 hover:bg-gray-100"
                  }`}
                  onClick={() => setSelectedCategory(category.id)}
                >
                  <File size={18} />
                  <span className="text-sm">{category.name}</span>
                </button>
              ))}
            </div>

            <button className="mt-6 flex items-center gap-2 text-sm text-blue-600 hover:text-blue-800">
              <Plus size={16} />
              <span>Add new template category</span>
            </button>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="flex-1 overflow-y-auto bg-gray-100">
          <div className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-2xl font-bold">{currentCategory.name}</h1>

              <div className="flex items-center gap-3">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
                  <input
                    type="text"
                    placeholder="Search templates..."
                    className="pl-10 pr-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                </div>

                <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors">
                  <Plus size={18} />
                  <span>New Template</span>
                </button>
              </div>
            </div>

            {/* Success Message */}
            {successMessage && (
              <div className="mb-6 p-3 bg-green-50 text-green-700 rounded-lg flex justify-between items-center">
                <span>{successMessage}</span>
                <button onClick={() => setSuccessMessage(null)} className="text-green-700 hover:text-green-900">
                  <X size={16} />
                </button>
              </div>
            )}

            {/* Templates Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {filteredTemplates.map((template) => (
                <div
                  key={template.id}
                  className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
                >
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="text-lg font-semibold">{template.title}</h3>
                      <span
                        className={`px-2 py-1 text-xs rounded-full ${
                          template.status === "active"
                            ? "bg-green-100 text-green-800"
                            : template.status === "draft"
                              ? "bg-yellow-100 text-yellow-800"
                              : "bg-gray-100 text-gray-800"
                        }`}
                      >
                        {template.status.charAt(0).toUpperCase() + template.status.slice(1)}
                      </span>
                    </div>

                    <p className="text-gray-600 text-sm mb-6">{template.description}</p>

                    <div className="flex justify-end gap-3">
                      <button
                        className="flex items-center gap-1 text-gray-600 hover:text-gray-900 text-sm px-3 py-1 rounded hover:bg-gray-100 transition-colors"
                        onClick={() => handleEditClick(template)}
                      >
                        <Edit size={16} />
                        <span>Edit</span>
                      </button>
                      <button className="flex items-center gap-1 text-gray-600 hover:text-gray-900 text-sm px-3 py-1 rounded hover:bg-gray-100 transition-colors">
                        <Eye size={16} />
                        <span>View</span>
                      </button>
                    </div>
                  </div>
                </div>
              ))}

              {/* Empty state */}
              {filteredTemplates.length === 0 && (
                <div className="col-span-2 flex flex-col items-center justify-center py-12 text-center">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                    <File size={24} className="text-gray-400" />
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-1">No templates found</h3>
                  <p className="text-gray-500 mb-4">
                    {searchQuery
                      ? `No templates match "${searchQuery}"`
                      : "This category doesn't have any templates yet"}
                  </p>
                  <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors">
                    <Plus size={18} />
                    <span>Create Template</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Edit Template Modal */}
      <EditTemplateModal
        isOpen={isEditModalOpen}
        template={editingTemplate}
        onClose={() => {
          setIsEditModalOpen(false)
          setEditingTemplate(null)
        }}
        onSave={handleSaveTemplate}
      />
    </div>
  )
}
