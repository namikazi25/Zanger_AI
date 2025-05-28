"use client";

import { useState } from "react";
import { File, Edit, Eye, Plus, Search, X, FolderOpen } from "lucide-react";
import EditTemplateModal from "@/components/EditTemplateModal";
import type { Template, TemplateCategory } from "@/types";

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
        description:
          "Non-disclosure agreement for Client A covering project details and proprietary information.",
      },
      {
        id: "commission-agreement",
        title: "Commission Agreement",
        status: "active",
        description:
          "Non-disclosure agreement for Vendor B covering service specifications and trade secrets.",
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
        description:
          "Standard consultancy agreement for professional services.",
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
        description:
          "Standard distribution agreement for product distribution.",
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
        description:
          "Standard non-disclosure agreement for international clients.",
      },
    ],
  },
];

export default function TemplatesContent() {
  const [categories, setCategories] =
    useState<TemplateCategory[]>(initialCategories);
  const [selectedCategory, setSelectedCategory] = useState<string>(
    categories[0].id
  );
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [editingTemplate, setEditingTemplate] = useState<Template | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Get the selected category
  const currentCategory =
    categories.find((cat) => cat.id === selectedCategory) || categories[0];

  // Filter templates based on search query
  const filteredTemplates = currentCategory.templates.filter(
    (template) =>
      template.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      template.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Handle opening the edit modal
  const handleEditClick = (template: Template) => {
    setEditingTemplate(template);
    setIsEditModalOpen(true);
  };

  // Handle saving template changes
  const handleSaveTemplate = (updatedTemplate: Template) => {
    // Update the template in the categories state
    const updatedCategories = categories.map((category) => {
      if (category.id === selectedCategory) {
        return {
          ...category,
          templates: category.templates.map((template) =>
            template.id === updatedTemplate.id ? updatedTemplate : template
          ),
        };
      }
      return category;
    });

    setCategories(updatedCategories);
    setSuccessMessage(
      `Template "${updatedTemplate.title}" updated successfully`
    );

    // Clear success message after 3 seconds
    setTimeout(() => {
      setSuccessMessage(null);
    }, 3000);
  };

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-primary-50 to-accent-50">
      {/* Header Section */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-primary-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary-100 rounded-lg">
              <FolderOpen className="w-6 h-6 text-primary-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-primary-900">Templates</h1>
              <p className="text-sm text-primary-700 mt-1">
                Organize and manage your legal document templates
              </p>
            </div>
          </div>
          <button className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-xl flex items-center gap-2 transition-colors shadow-sm">
            <Plus className="w-4 h-4" />
            <span className="font-medium">New Template</span>
          </button>
        </div>

        {/* Template Categories - Horizontal Layout */}
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-4">
            <h2 className="text-lg font-semibold text-primary-900">
              Categories
            </h2>
            <span className="text-sm text-primary-600">
              ({categories.length} categories)
            </span>
          </div>

          <div className="flex flex-wrap gap-3">
            {categories.map((category) => {
              const isSelected = selectedCategory === category.id;
              const templateCount = category.templates.length;

              return (
                <button
                  key={category.id}
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 border-2 ${
                    isSelected
                      ? "bg-primary-100 border-primary-300 text-primary-900 shadow-sm"
                      : "bg-white/70 border-primary-200 text-primary-700 hover:bg-primary-50 hover:border-primary-300"
                  }`}
                  onClick={() => setSelectedCategory(category.id)}
                >
                  <div
                    className={`p-1.5 rounded-lg ${
                      isSelected ? "bg-primary-200" : "bg-primary-100"
                    }`}
                  >
                    <File
                      className={`w-4 h-4 ${
                        isSelected ? "text-primary-700" : "text-primary-600"
                      }`}
                    />
                  </div>
                  <div className="text-left">
                    <div
                      className={`font-medium text-sm ${
                        isSelected ? "text-primary-900" : "text-primary-800"
                      }`}
                    >
                      {category.name}
                    </div>
                    <div
                      className={`text-xs ${
                        isSelected ? "text-primary-700" : "text-primary-600"
                      }`}
                    >
                      {templateCount} template{templateCount !== 1 ? "s" : ""}
                    </div>
                  </div>
                </button>
              );
            })}

            {/* Add Category Button */}
            <button className="flex items-center gap-3 px-4 py-3 border-2 border-dashed border-primary-300 rounded-xl text-primary-700 hover:border-primary-400 hover:bg-primary-50 hover:text-primary-800 transition-all duration-200">
              <div className="p-1.5 bg-primary-100 rounded-lg">
                <Plus className="w-4 h-4" />
              </div>
              <div className="text-left">
                <div className="font-medium text-sm">Add Category</div>
                <div className="text-xs text-primary-600">Create new</div>
              </div>
            </button>
          </div>
        </div>

        {/* Search and Current Category Info */}
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-semibold text-primary-900">
              {currentCategory.name}
            </h3>
            <p className="text-sm text-primary-700 mt-1">
              {filteredTemplates.length} template
              {filteredTemplates.length !== 1 ? "s" : ""} available
            </p>
          </div>

          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-primary-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Search templates..."
              className="w-80 pl-11 pr-4 py-3 bg-white/70 border border-primary-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>
      </div>

      {/* Success Message */}
      {successMessage && (
        <div className="mx-6 mt-4">
          <div className="p-4 bg-success-50 border border-success-200 text-success-800 rounded-xl flex justify-between items-center">
            <span className="font-medium">{successMessage}</span>
            <button
              onClick={() => setSuccessMessage(null)}
              className="text-success-600 hover:text-success-800 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Templates Grid */}
      <div className="flex-1 overflow-y-auto p-6">
        {filteredTemplates.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {filteredTemplates.map((template) => (
              <div
                key={template.id}
                className="bg-white/80 backdrop-blur-sm rounded-2xl border border-primary-200 overflow-hidden hover:shadow-lg hover:border-primary-300 transition-all duration-200 group"
              >
                <div className="p-6">
                  {/* Template Header */}
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex items-start gap-3">
                      <div className="p-2 bg-primary-50 rounded-lg group-hover:bg-primary-100 transition-colors">
                        <File className="w-5 h-5 text-primary-600 group-hover:text-primary-700" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-primary-900 text-lg leading-6">
                          {template.title}
                        </h3>
                        <span
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium mt-2 ${
                            template.status === "active"
                              ? "bg-success-100 text-success-800"
                              : template.status === "draft"
                              ? "bg-warning-100 text-warning-800"
                              : "bg-neutral-100 text-neutral-800"
                          }`}
                        >
                          {template.status.charAt(0).toUpperCase() +
                            template.status.slice(1)}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Template Description */}
                  <p className="text-primary-700 text-sm leading-relaxed mb-6 line-clamp-3">
                    {template.description}
                  </p>

                  {/* Template Actions */}
                  <div className="flex gap-2">
                    <button
                      className="flex-1 flex items-center justify-center gap-2 text-primary-700 hover:text-primary-800 hover:bg-primary-50 text-sm px-4 py-2.5 rounded-lg transition-all border border-primary-200 hover:border-primary-300"
                      onClick={() => handleEditClick(template)}
                    >
                      <Edit className="w-4 h-4" />
                      <span className="font-medium">Edit</span>
                    </button>
                    <button className="flex-1 flex items-center justify-center gap-2 text-accent-700 hover:text-accent-800 hover:bg-accent-50 text-sm px-4 py-2.5 rounded-lg transition-all border border-accent-200 hover:border-accent-300">
                      <Eye className="w-4 h-4" />
                      <span className="font-medium">View</span>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          /* Empty State */
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div className="w-20 h-20 bg-primary-100 rounded-2xl flex items-center justify-center mb-6">
              <File className="w-8 h-8 text-primary-400" />
            </div>
            <h3 className="text-xl font-semibold text-primary-900 mb-2">
              No templates found
            </h3>
            <p className="text-primary-700 mb-8 max-w-md">
              {searchQuery
                ? `No templates match "${searchQuery}". Try adjusting your search terms.`
                : "This category doesn't have any templates yet. Create your first template to get started."}
            </p>
            <button className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-xl flex items-center gap-2 transition-colors shadow-sm">
              <Plus className="w-4 h-4" />
              <span className="font-medium">Create Template</span>
            </button>
          </div>
        )}
      </div>

      {/* Edit Template Modal */}
      <EditTemplateModal
        isOpen={isEditModalOpen}
        template={editingTemplate}
        onClose={() => {
          setIsEditModalOpen(false);
          setEditingTemplate(null);
        }}
        onSave={handleSaveTemplate}
      />
    </div>
  );
}
