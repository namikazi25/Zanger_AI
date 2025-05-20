import { redirect } from "next/navigation"
import { createServerClient } from "@/lib/supabase-server"
import DashboardLayout from "@/components/layouts/dashboard-layout"
import ChatInterface from "@/components/chat-interface"

export default async function DashboardPage() {
  const supabase = createServerClient()
  const {
    data: { session },
  } = await supabase.auth.getSession()

  // If user is not logged in, redirect to login page
  if (!session) {
    redirect("/auth/login")
  }

  // Fetch user profile
  const { data: profile } = await supabase.from("profiles").select("*").eq("id", session.user.id).single()

  return (
    <DashboardLayout>
      <div className="py-6">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 md:px-8">
          <h1 className="text-2xl font-semibold text-gray-900 mb-6">Legal Assistant</h1>
          <ChatInterface />
        </div>
      </div>
    </DashboardLayout>
  )
}
