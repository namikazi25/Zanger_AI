import { redirect } from "next/navigation"
import { createServerClient } from "@/lib/supabase-server"

export default async function Home() {
  const supabase = createServerClient()
  const {
    data: { session },
  } = await supabase.auth.getSession()

  // If user is not logged in, redirect to login page
  if (!session) {
    redirect("/auth/login")
  }

  // If user is logged in, redirect to dashboard
  redirect("/dashboard")
}
